# ⚙️ Documentação do Módulo de Interatividade (Callbacks)

## 📝 Descrição

Este código Python é o cérebro do Dashboard. Ele lida com o carregamento dos dados, o pré-processamento necessário e define um callback (uma função reativa) do Dash.

O objetivo principal é: quando um autor é selecionado no dropdown (seletor), o código filtra os dados, calcula as estatísticas e gera os componentes visuais de saída (total de citações, nuvem de tags e lista detalhada de citações).Trechos-chave do Processamento:

1. Carregamento de Dados:

```Python

df = pd.read_csv('../documents/dados.csv')
# ...
autores_unicos = df['autor'].unique()

```

2. Definição do Callback: O update_dashboard é a função central que dispara todas as atualizações na tela.

```python
@callback(
    Output('total-citacoes', 'children'),
    Output('wordcloud-img', 'src'),
    Output('lista-citacoes', 'children'),
    Input('dropdown-autor', 'value')
)
def update_dashboard(selected_autor):
    # ... lógica de atualização

```

## ✨ Funcionalidades

Este código implementa as funcionalidades de processamento de dados e atualização dinâmica do dashboard:

1. Carregamento e Preparação Inicial de Dados:

    * Lê o arquivo dados.csv usando o Pandas.
    * Extrai a lista de autores únicos (autores_unicos) que é usada para popular o dropdown no arquivo de layout.

2. Função de Callback (update_dashboard):

    * Recebe o valor do autor selecionado (Input('dropdown-autor', 'value')).
    * Filtra o DataFrame (df) para incluir apenas as citações do autor escolhido.

3. Cálculo e Exibição do Total de Citações (Output 1):

    * Conta o número de linhas no DataFrame filtrado (len(df_autor)).
    * Retorna uma string formatada para o componente total-citacoes.

4. Geração da Nuvem de Tags (Wordcloud - Output 2):

    * Combina todas as tags do autor em uma única string.
    * Usa a biblioteca WordCloud para criar a imagem da nuvem.
    * Converte a imagem gerada para o formato Base64 (usando BytesIO e base64) para que ela possa ser exibida no html.Img do Dash.

```Python
wordcloud = WordCloud(...).generate(all_tags)
# ... conversão para base64 e retorno de image_src
```

5. Criação da Lista Detalhada de Citações (Output 3):

    * Itera sobre cada citação do autor.
    * Para cada citação, cria um dmc.Card.
    * Transforma as tags da citação em componentes visuais dmc.Badge.
    * Se existir um campo 'pagina', cria um dmc.Anchor (link) para tornar a citação clicável.
    * Retorna a lista de componentes dmc.Card para o lista-citacoes.

## 🧩 Dependências

Este código depende de bibliotecas do Dash, bibliotecas de manipulação de dados e de geração visual:


* ast (Necessário para converter strings que parecem listas na coluna 'tags' em listas reais de Python, usando ast.literal_eval)

* dash, dash.dependencies (Framework do Dashboard. Importa callback, Input e Output para definir a reatividade)

* dash_mantine_components (dmc) (Usado para criar os componentes visuais de saída, como dmc.Text, dmc.Card, dmc.Group e dmc.Badge.)

* pandas (pd) (Manipulação de Dados. Essencial para carregar o CSV (pd.read_csv), filtrar o DataFrame e realizar contagens/preparação de dados)

* wordcloud (Biblioteca específica usada para gerar a imagem da nuvem de tags)

* base64, io.BytesIO (Usados em conjunto para codificar a imagem gerada pela WordCloud em um formato que o Dash/HTML possa exibir diretamente (base64))

## 🏗️ Estrutura do Código

A estrutura divide-se em três partes principais: inicialização, carregamento de dados e a função de callback.

1. Imports

```Python
import ast
from dash import callback
import dash_mantine_components as dmc
import pandas as pd
from dash.dependencies import Input, Output
from wordcloud import WordCloud
import base64
from io import BytesIO
```

2. Carregamento e Inicialização dos Dados

Esta seção garante que os dados estejam prontos antes que o servidor Dash comece.

```Python
# Tenta carregar o DataFrame (df)
try:
    df = pd.read_csv('../documents/dados.csv')
except FileNotFoundError:
    # ... tratamento de erro
    exit()

# Prepara a lista inicial de autores
autores_unicos = df['autor'].unique()
```

3. Função de Callback Principal (update_dashboard)

Esta é a função que é chamada automaticamente sempre que o valor do dropdown-autor muda.

```Python
@callback(
    # Três saídas (total, imagem da nuvem, lista de citações)
    Output('total-citacoes', 'children'),
    Output('wordcloud-img', 'src'),
    Output('lista-citacoes', 'children'),
    # Uma entrada (valor do seletor de autor)
    Input('dropdown-autor', 'value')
)
def update_dashboard(selected_autor):
    # 1. Filtro dos Dados
    df_autor = df[df['autor'] == selected_autor]    
    
    # 2. Pré-processamento de Tags
    df_autor['tags'] = df_autor['tags'].apply(ast.literal_eval)
    df_autor['tags'] = df_autor['tags'].apply(lambda x: ', '.join(x)) 
    
    # 3. Cálculos e Geração da WordCloud
    # ... lógica da wordcloud e base64 ...
    
    # 4. Geração da Lista de Componentes Visuais
    # ... loop que cria dmc.Card para cada citação ...

    return total_citacoes_text, image_src, lista_citacoes_ui
```