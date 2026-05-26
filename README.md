# 📊 Painel Histórico de Inflação Brasileira (IPCA)
### Dashboard Interativo · Ciência de Dados · Python · Streamlit · API IBGE

> **Status do Projeto:** Concluído ✅ &nbsp;|&nbsp; **Linguagem:** Python 3 &nbsp;|&nbsp; **Interface:** Streamlit &nbsp;|&nbsp; **Dados:** IBGE/SIDRA API

---

## 📌 Sobre o Projeto

Dashboard interativo desenvolvido como **projeto acadêmico de Ciência de Dados** que analisa a trajetória da inflação brasileira (IPCA) entre **2016 e 2025**, calculando tanto as variações anuais quanto o **fator de inflação composta acumulada** ao longo da última década.

O projeto implementa um pipeline **ETL completo** com consumo da **API SIDRA do IBGE**, transformação dos dados com **Pandas** e visualização interativa com **Plotly** e **Streamlit**. Um mecanismo de fallback offline garante resiliência mesmo sem acesso à rede.

---

## 🎯 Objetivos e Perguntas-Chave

1. **Choque Inflacionário Anual** — Quais anos registraram os maiores desvios da meta e quais fatores (cadeias de suprimentos, reajustes tarifários) explicaram esses picos?
2. **Perda Acumulada de Poder de Compra** — Qual foi a desvalorização real do Real brasileiro ao longo dos 10 anos analisados?
3. **Padrão Mensal de Crise** — Qual a média inflacionária em anos de inflação controlada versus anos de dois dígitos?

---

## 💾 Fonte de Dados

| Campo | Detalhe |
|---|---|
| **API** | [SIDRA/IBGE](https://apisidra.ibge.gov.br/) — Sistema IBGE de Recuperação Automática |
| **Tabela** | 1737 — IPCA Série Histórica de Variação Mensal |
| **Variável** | 63 — Variação Mensal (%) |
| **Cobertura** | Últimos 144 meses · Brasil · Mensal |
| **Biblioteca** | `sidrapy` |

---

## 🏗️ Arquitetura do Pipeline (ETL)

```
┌─────────────────────────────────────────────────────┐
│                  Pipeline de Dados                   │
├──────────────┬──────────────────┬───────────────────┤
│  Extração    │  Transformação   │  Visualização     │
│  (IBGE API)  │  (Pandas/Cálculo)│  (Streamlit/Plot.)│
│              │                  │                   │
│ sidrapy  ──► │ ipca_bruto.csv   │ ipca_limpo.csv ──►│
│ fallback CSV │ fator composto   │ Dashboard UI      │
└──────────────┴──────────────────┴───────────────────┘
```

1. **`src/extracao_ibge.py`** — Conecta à API SIDRA, baixa os dados brutos; aciona fallback CSV se a API estiver indisponível → `data/ipca_bruto.csv`
2. **`src/transformacao.py`** — Filtra, converte tipos, ordena cronologicamente e calcula o fator de inflação composta anual → `data/ipca_limpo.csv`
3. **`app.py`** — Interface Streamlit que consome somente os dados tratados, com plotagem interativa e filtragem instantânea

---

## 💻 Stack Tecnológico

| Tecnologia | Uso |
|---|---|
| **Python 3** | Linguagem principal (PEP 484 type hints · PEP 257 docstrings) |
| **Streamlit** | Dashboard interativo e interface SaaS |
| **Pandas** | Manipulação e vetorização matemática dos dados |
| **Plotly** | Gráficos interativos e responsivos |
| **sidrapy** | Consumo da API SIDRA/IBGE |

---

## 📂 Estrutura do Repositório

```
projeto-cd-ed/
├── data/
│   ├── ipca_bruto.csv           # Backup da API / Fallback offline
│   └── ipca_limpo.csv           # Dados transformados prontos para o dashboard
├── src/
│   ├── extracao_ibge.py         # ETL — Extração via API SIDRA
│   └── transformacao.py         # ETL — Limpeza e cálculo do fator composto
├── .streamlit/
│   └── config.toml              # Configurações do Streamlit
├── app.py                       # Dashboard Streamlit principal
├── requirements.txt             # Dependências Python
└── README.md                    # Documentação do projeto
```

---

## 🚀 Como Executar Localmente

**Pré-requisitos:** Python 3.8+

```bash
# 1. Clone o repositório
git clone https://github.com/matheusrueda/projeto-cd-ed.git
cd projeto-cd-ed

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate          # Linux/Mac
# .\venv\Scripts\Activate.ps1    # Windows (PowerShell)

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o pipeline ETL
python src/extracao_ibge.py
python src/transformacao.py

# 5. Inicie o dashboard
streamlit run app.py
# Acesse: http://localhost:8501
```

---

## 👥 Equipe

| Nome | Papel |
|---|---|
| **Matheus** | Arquitetura do pipeline, ETL, Dashboard UI |
| **Luis** | Análise de dados e transformações |
| **Henrique** | Extração da API e fallback |
| **Guilherme** | Visualização e Plotly |
| **João** | Documentação e testes |

---

## 📄 Licença

Projeto acadêmico — uso educacional. Consulte os membros da equipe para outros usos.

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Dados-IBGE%2FSIDRA-009c3b?style=flat-square" alt="IBGE">
  <img src="https://img.shields.io/badge/Status-Concluído-brightgreen?style=flat-square" alt="Status">
</p>
