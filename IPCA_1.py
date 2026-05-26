import os
import sidrapy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as streamlit_app

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ==============================================================================
streamlit_app.set_page_config(page_title="Dashboard IPCA - IBGE", layout="wide")
sns.set_theme(style="whitegrid")

# Nome do arquivo de dados local
ARQUIVO_CSV = "ipca_consolidado.csv"

# ==============================================================================
# MOTOR DE EXECUÇÃO: FUNÇÃO DE EXTRAÇÃO E PROCESSAMENTO
# ==============================================================================
def executar_motor_ibge():
    """Busca os dados na API do IBGE, processa e salva em um arquivo CSV formatado para o Excel."""
    try:
        # Puxa os últimos 144 meses da variação mensal do IPCA (Tabela 1737, Variável 63)
        dados_raw = sidrapy.get_table(
            table_code="1737",
            variable="63",            
            period="last144",        
            territorial_level="1",
            ibge_territorial_code="all"
        )
        
        # Tratamento dos dados brutos
        df = dados_raw.copy()
        df.columns = df.iloc[0]  # Define a primeira linha como cabeçalho
        df = df.iloc[1:]         

        df = df[['Mês (Código)', 'Valor']].copy()
        df.columns = ['Codigo_Mes', 'Inflacao_Mensal']

        df['Inflacao_Mensal'] = pd.to_numeric(df['Inflacao_Mensal'], errors='coerce')
        df['Data'] = pd.to_datetime(df['Codigo_Mes'], format='%Y%m')
        df['Ano'] = df['Data'].dt.year

        # Ordena cronologicamente para garantir cálculos matemáticos exatos
        df = df.sort_values('Data').reset_index(drop=True)
        df['Fator'] = 1 + (df['Inflacao_Mensal'] / 100)

        # Consolidação anual
        resumo_anual = []
        for ano, group in df.groupby('Ano'):
            if len(group) < 12:
                continue # Ignora anos incompletos na base de dados
                
            media_mensal_ano = group['Inflacao_Mensal'].mean()
            acumulado_ano = (group['Fator'].prod() - 1) * 100
            
            resumo_anual.append({
                'Ano': int(ano),
                'Média Mensal': round(media_mensal_ano, 2),
                'Acumulado do Ano': round(acumulado_ano, 2)
            })

        df_resumo = pd.DataFrame(resumo_anual)
        
        if df_resumo.empty:
            return {"sucesso": False, "mensagem": "Nenhum ano completo (com 12 meses) foi encontrado nos dados."}
            
        # Filtra estritamente os últimos 10 anos cheios disponíveis
        df_resumo = df_resumo.tail(10)
        
        # CORREÇÃO EXCEL: sep=";" separa as colunas e utf-8-sig corrige a acentuação no Excel brasileiro
        df_resumo.to_csv(ARQUIVO_CSV, index=False, sep=";", encoding="utf-8-sig")
        
        return {"sucesso": True, "mensagem": "Dados atualizados com sucesso diretamente do IBGE!"}

    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro crítico no motor de dados: {e}"}


# ==============================================================================
# PAINEL LATERAL (CONTROLE DO MOTOR DE DADOS)
# ==============================================================================
streamlit_app.sidebar.title("⚙️ Painel de Controle")
streamlit_app.sidebar.markdown("""
Este painel separa o **motor de busca** da **interface**. 
O app carrega os dados salvos localmente em CSV para máxima velocidade e compatibilidade com o Excel.
""")

# Botão para forçar a execução do motor de dados
if streamlit_app.sidebar.button("🔄 Atualizar Dados via API IBGE"):
    with streamlit_app.spinner("Conectando ao SIDRA/IBGE e processando dados..."):
        resultado = executar_motor_ibge()
        if resultado["sucesso"]:
            streamlit_app.sidebar.success(resultado["mensagem"])
        else:
            streamlit_app.sidebar.error(resultado["mensagem"])


# ==============================================================================
# CAMADA DE APRESENTAÇÃO (INTERFACE DO DASHBOARD)
# ==============================================================================
streamlit_app.title("📊 Painel Histórico de Inflação: IPCA (IBGE)")

# Se o arquivo CSV não existir (primeira execução), roda o motor automaticamente
if not os.path.exists(ARQUIVO_CSV):
    with streamlit_app.spinner("⚠️ Primeira execução detectada. Criando base de dados local..."):
        executar_motor_ibge()

# Carrega os dados do CSV se ele existir após a verificação/criação acima
if os.path.exists(ARQUIVO_CSV):
    try:
        # CORREÇÃO EXCEL: Adicionado o parâmetro sep=";" para conseguir ler o formato novo corretamente
        df_resumo = pd.read_csv(ARQUIVO_CSV, sep=";")
        anos_str = df_resumo['Ano'].astype(str)

        # Cálculo da inflação acumulada total baseada no período do CSV
        fator_total = (1 + (df_resumo['Acumulado do Ano'] / 100)).prod()
        inflacao_acumulada_periodo = (fator_total - 1) * 100

        # Exibe o indicador chave do período acumulado da década
        streamlit_app.metric(
            label="Inflação Total Acumulada no Período (Últimos 10 anos cheios do CSV)", 
            value=f"{inflacao_acumulada_periodo:.2f}%"
        )
        
        streamlit_app.write("---")

        # ==============================================================================
        # GRÁFICO 1: ACUMULADO REAL
        # ==============================================================================
        streamlit_app.subheader("📈 IPCA Fechado Ano a Ano")
        
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        bars = ax1.bar(anos_str, df_resumo['Acumulado do Ano'], color='#2b5c8f', width=0.5, label='IPCA Real (IBGE)', zorder=3)
        ax1.axhline(0, color='gray', linestyle='-', linewidth=0.8)

        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.15 if height >= 0 else height - 0.4,
                     f'{height:.2f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax1.set_ylabel('Variação Acumulada Anual (%)', fontsize=11)
        plt.tight_layout()
        streamlit_app.pyplot(fig1)

        streamlit_app.write("---")

        # ==============================================================================
        # GRÁFICO 2: LINHA DE TENDÊNCIA
        # ==============================================================================
        streamlit_app.subheader("📉 Linha de Tendência e Direção da Inflação na Década")
        
        fig2, ax2 = plt.subplots(figsize=(12, 4))
        ax2.plot(anos_str, df_resumo['Acumulado do Ano'], color='#e377c2', marker='o', linewidth=2.5, label='Trajetória Anual do IPCA')
        
        media_periodo = df_resumo['Acumulado do Ano'].mean()
        ax2.axhline(media_periodo, color='gray', linestyle='--', linewidth=1, label=f'Média do Período ({media_periodo:.2f}%)')
        
        for x, y in zip(anos_str, df_resumo['Acumulado do Ano']):
            ax2.text(x, y + 0.2, f'{y:.1f}%', ha='center', va='bottom', fontsize=9, color='#e377c2', fontweight='bold')

        ax2.set_ylabel('Inflação Fechada (%)', fontsize=11)
        ax2.set_xlabel('Ano', fontsize=11)
        ax2.legend(loc='upper right')
        plt.tight_layout()
        streamlit_app.pyplot(fig2)

        streamlit_app.write("---")

        # ==============================================================================
        # TEXTO EXPLICATIVO DOS ANOS ACIMA DO ESPERADO
        # ==============================================================================
        streamlit_app.subheader("🔍 Análise Histórica: Anos com Inflação Acima do Esperado")
        streamlit_app.markdown("""
        Ao analisar a trajetória do IPCA na última década, destacam-se **três momentos principais** em que a inflação rompeu a normalidade e ficou significativamente acima das expectativas econômicas do mercado e do Banco Central:

        * **🔥 Ano de 2015 (10,67%):** Foi o maior pico inflacionário do período recente. O estouro foi provocado por uma combinação severa de **crise econômica interna**, forte desvalorização do Real frente ao Dólar e, principalmente, pelo represamento e posterior liberação súbita dos **preços administrados** (como tarifas de energia elétrica e combustíveis) que vinham sendo controlados artificialmente nos anos anteriores.
        * **📦 Ano de 2021 (10,06%):** A inflação voltou a atingir os dois dígitos devido aos reflexos globais da pandemia de Covid-19. O fechamento de indústrias gerou uma **crise na cadeia global de suprimentos** (falta de matérias-primas e componentes), o que disparou o custo do frete internacional. No Brasil, o cenário foi agravado pela alta global das *commodities* (como o petróleo) e por uma severa crise hídrica que encareceu a conta de luz.
        * **🌾 Ano de 2022 (5,79%):** Embora o número final pareça menor que o de 2021, a inflação do primeiro semestre rodou bem acima do teto esperado, sendo impulsionada pelo início da **Guerra entre Rússia e Ucrânia**, que causou um choque mundial nos preços de alimentos (como trigo e fertilizantes) e combustíveis. O índice anual só não fechou mais alto devido a desonerações fiscais emergenciais feitas no segundo semestre sobre combustíveis e energia.

        Nos demais anos da série, a inflação comportou-se de forma muito mais próxima ou abaixo da média histórica, reflecting momentos de atividade econômica mais fraca ou de taxas de juros (Selic) elevadas para conter o consumo.
        """)

        streamlit_app.write("---")
        
        # ==============================================================================
        # TABELA DE DADOS CONSOLIDADOS
        # ==============================================================================
        streamlit_app.subheader("📋 Tabela Comparativa de Dados Consolidados")
        
        df_formatado = df_resumo.copy()
        df_formatado['Ano'] = df_formatado['Ano'].astype(str)
        df_formatado['Média Mensal'] = df_formatado['Média Mensal'].map('{:,.2f}%'.format)
        df_formatado['Acumulado do Ano'] = df_formatado['Acumulado do Ano'].map('{:,.2f}%'.format)
        
        streamlit_app.dataframe(df_formatado, use_container_width=True, hide_index=True)

    except Exception as e_processamento:
        streamlit_app.error("❌ Ocorreu um erro ao carregar ou formatar os dados salvos localmente.")
        streamlit_app.info(f"Detalhes do erro: {e_processamento}")
else:
    streamlit_app.warning("⚠️ Não foi possível renderizar o dashboard porque a base de dados local não existe e a API do IBGE falhou ao gerá-la.")
# streamlit run IPCA_1.py