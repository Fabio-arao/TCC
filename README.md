# Projeto TCC: Robô de Web Scraping para Consórcio e Financiamento Imobiliário

Este projeto consiste em um robô desenvolvido em Python para baixar dados do mercado de consórcio e financiamento de imóveis a partir do site do [Banco Central do Brasil (Bacen)](https://www.bcb.gov.br/). Além disso, inclui um Jupyter Notebook com análises dos dados utilizando métodos de séries temporais, clustering (com K-means) e Data Wrangling.

## Funcionalidades
- Coleta automática de dados do Bacen usando [Selenium](https://www.selenium.dev/).
- Tratamento dos dados coletados com [pandas](https://pandas.pydata.org/) e exportação para arquivos `.xlsx`.
- Análise dos dados no Jupyter Notebook utilizando:
  - Séries temporais para detectar padrões e tendências nos dados.
  - K-means para definir a quantidade ideal de clusters.
  - Análise de clusters para comparar o comportamento dos mercados de consórcio e financiamento imobiliário.
- Data Wrangling para limpar e organizar os dados.

## Requisitos de Sistema
- [Python 3.10](https://www.python.org/downloads/release/python-3100/) ou superior
- [Google Chrome](https://www.google.com/intl/pt-BR/chrome/) (para utilização com o Selenium)

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/seu-repositorio.git
   cd seu-repositorio
   
2. **Crie um ambiente virtual**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   
3. **Instale as dependências: Certifique-se de que o pip esteja atualizado e execute**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

 4. **Configure o Selenium: O Selenium utiliza o navegador Chrome para automatizar o download de dados do Bacen. Certifique-se de que o ChromeDriver seja compatível com a versão instalada do Google Chrome.**

## Executando o Robô

1. **Com o ambiente virtual ativado e as dependências instaladas, ou o contêiner Selenium rodando, execute o robô**:
   ```bash
   python main.py
**O script irá acessar o site do Bacen, coletar os dados e salvá-los em arquivos .xlsx.**

## Estrutura do Projeto
- **`main.py`**: Script principal que executa o robô de coleta de dados.
- **`notebook.ipynb`**: Jupyter Notebook com as análises de dados, incluindo séries temporais e clustering.
- **`requirements.txt`**: Arquivo contendo as dependências do projeto.
- **`.sheets/`**: Pasta onde os arquivos `.xlsx` gerados pelo robô serão salvos.

## Análises Incluídas
- **Séries Temporais**: Utilizadas para detectar padrões sazonais e tendências nos dados de consórcio e financiamento.
- **K-means Clustering**: Determinação da quantidade ideal de clusters.
- **Análise de Clusters**: Comparação dos mercados de consórcio e financiamento através de clusters.

## Dependências Principais
- **[Selenium](https://www.selenium.dev/)**: Para automação do navegador e coleta de dados.
- **[Pandas](https://pandas.pydata.org/)**: Para manipulação e tratamento dos dados.
- **[Matplotlib](https://matplotlib.org/)/[Seaborn](https://seaborn.pydata.org/)**: Para visualizações gráficas.
- **[Scikit-learn](https://scikit-learn.org/stable/)**: Para a aplicação de algoritmos de clustering (K-means).
- **[Jupyter Notebook](https://jupyter.org/)**: Para desenvolvimento e visualização das análises.

## Data Wrangling
A técnica de Data Wrangling é aplicada para:
- Limpeza dos dados coletados.
- Tratamento de datas e valores numéricos.
- Formatação e preparação para as análises.

## Contribuindo
Pull requests são bem-vindos. Para grandes mudanças, por favor, abra uma issue primeiro para discutir o que você gostaria de alterar.

## Licença
Este projeto está licenciado sob os termos da licença [MIT](https://opensource.org/licenses/MIT).



