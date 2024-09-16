# INFNET 
## TP 3 - Frontend com Streamlit
### Aluno: Rodrigo Moreira Avila

---

### Aviso ao professor:
Os dados do DataRIO estava em formato .xls, portanto o upload será feito através do arquivo .xls disponibilizado pelo portal e se encontra no diretório ```./data/01_raw```.

Escolhi fazer um plot de mapa na competência de plot complexos, pois é o que mais fazia sentido para os meus dados.


### Sobre o projeto:
Aplicação para resolver uma série de exercícios com o framework ```Streamlit```, criando visualizações informativas e interativas usando diversas bibliotecas em Python, para explorar e analisar dados epidemiológicos complexos

Será utilizado [dados de turismo no Rio de Janeiro](https://www.data.rio/search?groupIds=729990e9fbc04c6ebf81715ab438cae8) para a resolução dos exercícios.

Base de dados escolhida: [Chegada mensal de turistas pelo Rio de Janeiro, por via Aérea, segundo continentes e países de residência permanente, entre 2006-2019](https://www.data.rio/documents/a6c6c3ff7d1947a99648494e0745046d/about)


### Estrutura do projeto:
```./README.md``` - Este arquivo.

```./notebook/*``` - Contém o notebook utilizado análise exploratória dos dados.

```./src/*``` - Contém o código fonte da aplicação.

```./data/*``` - Contém os arquivos com os dados.

```./requirements.txt``` - Contém as dependências do projeto.


### Como rodar o projeto streamlit:
1. Configurando versão do python:
```bash
pyenv local 3.11.8
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:
```bash
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
streamlit run src/app.py
```

### Como rodar o notebook:

1. Execute o Jupyter Notebook:
```bash
jupyter notebook
```
