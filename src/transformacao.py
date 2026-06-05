import os
import sys
import logging
import pandas as pd

# Configura o logging para acompanhar o processo
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def processar_dados_ipca(
    caminho_bruto: str = "data/ipca_bruto.csv",
    caminho_limpo: str = "data/ipca_limpo.csv"
) -> None:
    """
    Lê os dados brutos de IPCA, realiza o processamento e limpeza, calcula as métricas 
    anuais acumuladas e o fator composto, e salva o arquivo final limpo.

    Args:
        caminho_bruto (str): Caminho para o arquivo CSV bruto (padrão: "data/ipca_bruto.csv").
        caminho_limpo (str): Caminho onde os dados limpos e consolidados serão salvos (padrão: "data/ipca_limpo.csv").

    Raises:
        FileNotFoundError: Se o arquivo de dados brutos não for encontrado.
        KeyError: Se as colunas necessárias não estiverem no DataFrame.
        ValueError: Se houver problemas com os valores durante o processamento.
        RuntimeError: Para erros gerais durante o pipeline de transformação.
    """
    try:
        logger.info(f"Carregando dados brutos de: {caminho_bruto}")
        if not os.path.exists(caminho_bruto):
            raise FileNotFoundError(f"Arquivo de dados brutos não encontrado em: {caminho_bruto}")

        # Lê os dados brutos
        df_raw = pd.read_csv(caminho_bruto, dtype=str)
        
        # Ajusta cabeçalho (a primeira linha contém a descrição amigável das colunas)
        df = df_raw.copy()
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)

        logger.info("Filtrando e renomeando colunas relevantes...")
        # Verifica se as colunas esperadas estão presentes
        colunas_necessarias = {"Mês (Código)", "Valor"}
        if not colunas_necessarias.issubset(df.columns):
            raise KeyError(
                f"As colunas necessárias {colunas_necessarias} não foram encontradas no arquivo bruto. "
                f"Colunas encontradas: {list(df.columns)}"
            )

        df = df[["Mês (Código)", "Valor"]].copy()
        df.columns = ["Codigo_Mes", "Inflacao_Mensal"]

        # Conversão de tipos e tratamento de valores nulos
        df["Inflacao_Mensal"] = pd.to_numeric(df["Inflacao_Mensal"].str.replace(",", "."), errors="coerce")
        # Se houver algum nulo na inflação, removemos a linha correspondente
        if df["Inflacao_Mensal"].isnull().any():
            nulos_count = df["Inflacao_Mensal"].isnull().sum()
            logger.warning(f"Encontrados {nulos_count} valores nulos na coluna Inflacao_Mensal. Removendo-os.")
            df = df.dropna(subset=["Inflacao_Mensal"])

        # Trata datas e anos
        df["Data"] = pd.to_datetime(df["Codigo_Mes"], format="%Y%m", errors="coerce")
        if df["Data"].isnull().any():
            logger.warning("Linhas com datas inválidas foram encontradas e serão removidas.")
            df = df.dropna(subset=["Data"])

        df["Ano"] = df["Data"].dt.year

        # Ordenação cronológica rigorosa para cálculos compostos acumulados
        df = df.sort_values("Data").reset_index(drop=True)
        
        # Fator de inflação: (1 + variação_mensal / 100)
        df["Fator"] = 1 + (df["Inflacao_Mensal"] / 100)

        logger.info("Realizando consolidação anual e cálculo de fatores compostos...")
        resumo_anual = []
        for ano, group in df.groupby("Ano"):
            # Ignora anos incompletos na base de dados (precisa de exatamente 12 meses)
            if len(group) < 12:
                logger.info(f"Ignorando o ano {ano} por conter apenas {len(group)} meses.")
                continue
                
            media_mensal_ano = group["Inflacao_Mensal"].mean()
            acumulado_ano = (group["Fator"].prod() - 1) * 100
            
            resumo_anual.append({
                "Ano": int(ano),
                "Media_Mensal": round(media_mensal_ano, 4),
                "Acumulado_Ano": round(acumulado_ano, 4)
            })

        df_resumo = pd.DataFrame(resumo_anual)
        
        if df_resumo.empty:
            raise ValueError("Nenhum ano completo (com 12 meses) foi encontrado para processamento.")

        # Ordena por ano
        df_resumo = df_resumo.sort_values("Ano").reset_index(drop=True)
        
        # Filtra estritamente os últimos 10 anos cheios disponíveis
        df_resumo = df_resumo.tail(10).reset_index(drop=True)

        # Cálculo do fator composto acumulado ao longo da série de 10 anos (inflação composta acumulada ano a ano)
        # Fator anual correspondente: 1 + (Acumulado_Ano / 100)
        df_resumo["Fator_Anual"] = 1 + (df_resumo["Acumulado_Ano"] / 100)
        
        # Multiplicação acumulada dos fatores anuais para obter a trajetória da inflação composta
        df_resumo["Fator_Composto_Acumulado"] = df_resumo["Fator_Anual"].cumprod()
        # Inflação composta acumulada em percentual a partir do início da série
        df_resumo["Inflacao_Composta_Acumulada_Perc"] = (df_resumo["Fator_Composto_Acumulado"] - 1) * 100

        # Arredondamentos finais para gravação limpa no CSV
        df_resumo["Media_Mensal"] = df_resumo["Media_Mensal"].round(2)
        df_resumo["Acumulado_Ano"] = df_resumo["Acumulado_Ano"].round(2)
        df_resumo["Fator_Composto_Acumulado"] = df_resumo["Fator_Composto_Acumulado"].round(4)
        df_resumo["Inflacao_Composta_Acumulada_Perc"] = df_resumo["Inflacao_Composta_Acumulada_Perc"].round(2)

        # Remove a coluna auxiliar do fator anual antes de salvar
        df_resumo = df_resumo.drop(columns=["Fator_Anual"])

        # Salvar o CSV limpo de forma compatível com Excel brasileiro e sistemas gerais (delimitador ";", utf-8-sig)
        os.makedirs(os.path.dirname(caminho_limpo), exist_ok=True)
        df_resumo.to_csv(caminho_limpo, index=False, sep=";", encoding="utf-8-sig")
        logger.info(f"Dados limpos salvos com sucesso em: {caminho_limpo}")

    except (FileNotFoundError, KeyError, ValueError) as e:
        logger.error(f"Erro de validação ou leitura nos dados do IPCA: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro crítico e inesperado no processamento de dados do IPCA: {e}")
        raise RuntimeError(f"Falha na transformação de dados: {e}") from e

if __name__ == "__main__":
    try:
        processar_dados_ipca()
        sys.exit(0)
    except Exception as erro:
        logger.error(f"Execução do pipeline de transformação falhou: {erro}")
        sys.exit(1)
