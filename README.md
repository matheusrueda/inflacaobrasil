# 📊 Painel Histórico de Inflação (IPCA)

Um dashboard interativo e dinâmico que analisa a inflação oficial do Brasil (IPCA) de **2016 a 2025**. O objetivo é traduzir índices econômicos complexos em um impacto compreensível no dia a dia, demonstrando a corrosão do poder de compra no bolso do brasileiro ao longo dos últimos 10 anos.

---

## 💡 O que o painel responde?
* **O custo de vida aumentou quanto?** Veja o cálculo do fator de inflação acumulada e composta no período que você escolher.
* **Qual foi o pico da inflação?** Identifique os anos mais críticos (como os impactos globais de 2021 e 2022).
* **Como isso afeta meu bolso?** Utilize o **Simulador de Poder de Compra** para ver quanto custa hoje um item básico do passado (como um cafezinho ou uma cesta básica).

---

## 🏗️ Como o projeto foi construído
Para garantir performance e manter a interface rápida, separamos o processamento dos dados da visualização final (arquitetura desacoplada):

* **Extração (`src/extracao_ibge.py`):** Conecta à API SIDRA do IBGE para buscar os dados mensais brutos (Tabela 1737). Possui um teste de conectividade rápido (3s) com fallback local automático se a API estiver fora do ar.
* **Transformação (`src/transformacao.py`):** Processa os dados brutos usando Pandas, calculando os acumulados anuais e os fatores de multiplicação.
* **Interface (`app.py`):** Dashboard construído com Streamlit, utilizando Plotly para gráficos fluidos e interativos.

---

## 🚀 Como Executar Localmente

### Pré-requisito
Ter o Python 3.8+ instalado em sua máquina.

### Passo a Passo

```bash
# 1. Obter o repositório
git clone https://github.com/matheusrueda/projeto-cd-ed.git
cd projeto-cd-ed

# 2. Criar e ativar o ambiente virtual (Recomendado)
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar o pipeline ETL (baixa e trata os dados)
python src/extracao_ibge.py
python src/transformacao.py

# 5. Iniciar o dashboard no navegador
streamlit run app.py
```

---

## 🛠️ Tecnologias Utilizadas
* **Python 3:** Linguagem base com tipagem estática nos scripts.
* **Streamlit:** Interface web rápida e intuitiva.
* **Pandas:** Manipulação matemática e agrupamento de dados.
* **Plotly:** Gráficos interativos responsivos.
* **sidrapy:** Cliente Python oficial para a API do IBGE.
* **orjson:** Serialização JSON acelerada para renderização instantânea dos gráficos.

---

## 👥 Equipe
* **Matheus** 
* **Luis** 
* **Henrique** 
* **Guilherme** 
* **João**

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Dados-IBGE%2FSIDRA-009c3b?style=flat-square" alt="IBGE">
  <img src="https://img.shields.io/badge/Status-Concluído-brightgreen?style=flat-square" alt="Status">
</p>
