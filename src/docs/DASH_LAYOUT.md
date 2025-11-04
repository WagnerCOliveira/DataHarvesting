# 📄 Documentação do Layout do Dashboard de Citações por Autor

## 📝 Descrição

Este código Python define o layout visual (a "cara") de um Dashboard de Citações por Autor, utilizando as bibliotecas Dash, dash-mantine-components (dmc) e Plotly Express (px).

A função principal, layout_children(), cria toda a estrutura HTML e de componentes visuais que será exibida ao usuário. Ele organiza o conteúdo em um Container principal, usando um sistema de Grid para dividir a tela em duas colunas principais:

* Coluna da Esquerda (Pequena): Para seleção de um autor.
* Coluna da Direita (Grande): Para exibir informações e gráficos relacionados ao autor selecionado.

Trecho-chave da estrutura:
```Python

def layout_children():
    # ...
    children=[
        dmc.Container(
            fluid=True,
            # ...
            children=[
                dmc.Title("Dashboard de Citações por Autor", order=1, ta="center", mb=30),
                dmc.Grid( # Início do Grid principal
                    children=[
                        # Coluna da esquerda (span=3)
                        dmc.GridCol(span=3, children=[...]), 
                        # Coluna da direita (span=9)
                        dmc.GridCol(span=9, children=[...])
                    ]
                )
            ]
        )
    ]
    return children
```

## ✨ Funcionalidades

O código implementa a estrutura base que permite as seguintes funcionalidades no dashboard:

1. Seleção de Autor: Permite ao usuário escolher um autor em uma lista suspensa.

* O componente usado é o dmc.Select com o id='dropdown-autor'.
* Os dados iniciais são preenchidos pela variável autores_unicos, importada de callbaks.

```Python

dmc.Select(
    id='dropdown-autor',
    data=[{'label': i, 'value': i} for i in autores_unicos],
    # ...
)
```
2. Exibição de Informações do Autor: Cria espaços reservados para mostrar dados dinâmicos após a seleção.

    * Um dmc.Text com id='total-citacoes' para exibir o total de citações.

```Python
dmc.Text(id='total-citacoes'),
```

3. Visualização de Nuvem de Tags (Wordcloud): Cria um espaço para exibir uma imagem de nuvem de tags.

    * É usado um html.Img (componente básico do Dash) com o id='wordcloud-img'.

```Python

html.Img(id='wordcloud-img', style={'width': '100%'})

```
4. Listagem de Citações: Prepara um Grid Simples (uma área) para listar as citações do autor escolhido.

    * O dmc.SimpleGrid com id='lista-citacoes' será preenchido dinamicamente (geralmente por um callback).

``` Python

dmc.SimpleGrid(
    id='lista-citacoes',
    cols=1, spacing="lg"
)
```

## 🧩 Dependências

Este código depende de bibliotecas externas e de um módulo local para funcionar corretamente:


* dash (Necessário para usar o html.Img e outras funções base do Dash. É o framework principal do dashboard)

* dash_mantine_components (Essencial. É a biblioteca que fornece a maioria dos componentes visuais usados (dmc.Container, dmc.Grid, dmc.Select, dmc.Card, etc.), dando o estilo moderno ao layout)

* plotly.express (Embora não seja usado diretamente na função layout_children(), a importação indica que o dashboard utilizará essa biblioteca para criar gráficos (ela é um padrão em aplicações Dash))

* callbaks (Módulo Local. É crucial, pois a variável autores_unicos é usada para preencher a lista de opções (data) do seletor de autor (dmc.Select))

## 🏗️ Estrutura do Código

O código é estruturado em uma única função, layout_children(), que retorna uma lista de componentes do Dash (ou dmc).

1. Imports e Variáveis Iniciais

```Python

from dash import html
import dash_mantine_components as dmc
import plotly.express as px
from callbaks import autores_unicos # Importa a lista de autores

def layout_children():
    # Início da função de layout
```

2. Container Principal e Título

Todo o conteúdo é agrupado em um dmc.Container para centralizar e limitar a largura (embora fluid=True o faça usar a largura máxima).

```Python    

    children=[
        dmc.Container(
            fluid=True,
            p=20,
            children=[
                dmc.Title("Dashboard de Citações por Autor", order=1, ta="center", mb=30), # Título do Dashboard
                dmc.Grid( # Início da divisão em colunas
                    children=[
                        # ...
```

3. Coluna de Seleção (Esquerda - span=3)

É um dmc.GridCol que ocupa 3/12 da largura total. Contém um dmc.Card para agrupar o título e o seletor.

```Python                        
                    dmc.GridCol(  
                            span=3, # Ocupa 3 colunas (pequena)
                            children=[
                                dmc.Card( # Cartão para o seletor
                                    children=[
                                        # Título da seção (Selecione um Autor)
                                        # ...
                                        dmc.Select( # O componente de seleção
                                            id='dropdown-autor',
                                            # ...
                                        )
                                    ]
                                )
                            ]
                        ),
```

4. Coluna de Informações (Direita - span=9)

É um dmc.GridCol que ocupa 9/12 da largura total. Contém um dmc.Card que organiza as informações em uma pilha (dmc.Stack).

```Python
                        dmc.GridCol(
                            span=9, # Ocupa 9 colunas (grande)
                            children=[
                                dmc.Card( # Cartão para as informações
                                    children=[
                                        # ...
                                        dmc.Stack( # Organiza os elementos verticalmente
                                            gap="lg",
                                            children=[
                                                dmc.Text(id='total-citacoes'), # Espaço para o total
                                                # ... Nuvem de Tags (html.Img com id='wordcloud-img')
                                                dmc.Divider(my="md"),
                                                dmc.Text("Citações", fw=700, size="lg"),
                                                dmc.SimpleGrid( # Espaço para a lista de citações
                                                    id='lista-citacoes',
                                                    cols=1, spacing="lg"
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
```

