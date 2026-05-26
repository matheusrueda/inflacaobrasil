# 📊 Painel Histórico de Inflação Brasileira (IPCA)
### Projeto Acadêmico de Ciência de Dados & Estrutura de Dados

> **Status do Projeto:** Concluído✅

---

## 🎯 Tema do Projeto e Justificativa

**Tema:** Análise da Trajetória Composta e Variação Anual da Inflação Brasileira (IPCA) entre 2016 e 2025.

**Justificativa:** 
A inflação é um indicador macroeconômico essencial para medir a estabilidade monetária de um país e a variação do custo de vida. Compreender o comportamento do Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado pelo IBGE, é crucial para análises econômicas acadêmicas e de mercado. 

Este projeto propõe uma abordagem científica para visualizar e calcular não apenas as variações pontuais anuais da inflação, mas também o **fator composto acumulado** ao longo da última década. Esse cálculo permite avaliar o efeito cumulativo de corrosão do poder de compra da moeda brasileira (Real) de forma interativa e visualmente polida.

---

## 💾 Fonte de Dados (API) e Descrição

**Fonte dos Dados (API):** API SIDRA do IBGE (Sistema IBGE de Recuperação Automática).
- **Tabela:** 1737 (IPCA - Série histórica de variação mensal)
- **Variável:** 63 (IPCA - Variação mensal)
- **Frequência:** Mensal, últimos 144 meses (12 anos)
- **Nível Territorial:** Brasil

**Descrição do Pipeline:**
O projeto implementa uma arquitetura desacoplada e escalável (ETL - Extração, Transformação e Carga):
1. **Extração (`src/extracao_ibge.py`):** Conecta-se à API do IBGE via biblioteca `sidrapy` e realiza o download dos dados brutos. Se a API estiver fora do ar ou apresentar instabilidade, um **mecanismo de fallback off-line** com a base histórica consolidada é acionado de forma resiliente, gerando `data/ipca_bruto.csv`.
2. **Transformação (`src/transformacao.py`):** Consome os dados brutos, filtra e converte tipos, ordena cronologicamente e computa o fator de inflação anual composto (multiplicação acumulada) de 10 anos completos, salvando em `data/ipca_limpo.csv`.
3. **Visualização (`app.py`):** Interface Streamlit otimizada que consome unicamente os dados tratados e limpos, permitindo plotagem interativa e filtragem instantânea sem requisições de rede redundantes.

---

## ❓ Perguntas-Chave (Insights Acadêmicos)

1. **Choque Inflacionário Anual:** Quais anos registraram os maiores desvios da meta de inflação e quais fatores (como desorganizações de cadeias globais de suprimentos ou reajustes tarifários) explicaram esses picos?
2. **Perda Acumulada de Valor:** De quanto foi a perda acumulada real do poder de compra ao longo dos 10 anos analisados (fator de inflação composta acumulada)?
3. **Padrão Mensal de Crise:** Qual foi a média inflacionária mensal em anos de inflação controlada versus anos que registraram dois dígitos de inflação?

---

## 💻 Tecnologias e Ferramentas Utilizadas

Este projeto atende a todos os requisitos acadêmicos propostos utilizando as seguintes tecnologias:
- **Linguagem:** Python 3 (PEP 484 type hints e PEP 257 docstrings)
- **Interface e Dashboard:** Streamlit (Layout SaaS Premium com CSS sutil)
- **Manipulação de Dados:** Pandas (Vetorização matemática)
- **Visualização de Dados:** Plotly (Gráficos interativos responsivos)
- **Consumo de API:** `sidrapy` (Interface com SIDRA/IBGE)

---

## 📂 Estrutura do Repositório

```
projeto_ipca_brasil/
├── .agent/
│   ├── rules/
│   │   └── prompt.md            # Regras do agente de IA
│   └── skills/
│       └── SKILL.md             # Definição e diretrizes das skills integradas
├── data/
│   ├── ipca_bruto.csv           # Backup exato do retorno da API / Fallback
│   └── ipca_limpo.csv           # Dados consolidados prontos para leitura na UI
├── src/
│   ├── extracao_ibge.py         # Script ETL de Extração da API SIDRA
│   └── transformacao.py         # Script ETL de Limpeza e Cálculo de Fator Composto
├── .gitignore                   # Arquivos ignorados no Git
├── app.py                       # Interface Streamlit de Visualização SaaS Premium
├── README.md                    # Manual do projeto e documentação acadêmica
└── requirements.txt             # Dependências de execução
```

---

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o dashboard na sua máquina:

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/matheusrueda/projeto-cd-ed.git
   cd projeto-cd-ed
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o pipeline de dados (ETL):**
   ```bash
   # Executa a extração
   python src/extracao_ibge.py
   
   # Executa o processamento
   python src/transformacao.py
   ```

5. **Inicie a interface Streamlit:**
   ```bash
   streamlit run app.py
   ```
   *O painel abrirá automaticamente no navegador em `http://localhost:8501`.*

---

## 👥 Equipe Desenvolvedora

O grupo é formado por:
- **Matheus**
- **Luis**
- **Henrique**
- **Guilherme**
- **João**