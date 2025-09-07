from dash import html
import dash_mantine_components as dmc

import plotly.express as px

from callbaks import autores_unicos


def layout_children():

    children=[
            dmc.Container(
                fluid=True,
                p=20,
                children=[
                    dmc.Title("Dashboard de Citações por Autor", order=1, ta="center", mb=30),
                    dmc.Grid(
                        children=[
                            # Seção de seleção de autor
                            dmc.GridCol(  
                                span=3,
                                children=[
                                    dmc.Card(
                                        children=[
                                            dmc.CardSection(
                                                dmc.Text(
                                                    "Selecione um Autor", 
                                                    fw=700, 
                                                    size="lg"
                                                ),
                                                withBorder=True, 
                                                inheritPadding=True, 
                                                py="xs"
                                            ),
                                            dmc.Select(
                                                id='dropdown-autor',
                                                data=[{'label': i, 'value': i} for i in autores_unicos],
                                                value=autores_unicos[0] if len(autores_unicos) > 0 else None,
                                                placeholder="Selecione um autor...",
                                                clearable=False,
                                                style={'marginTop': '10px'}
                                            )
                                        ],
                                        withBorder=True, shadow="sm", radius="md", p="xl"
                                    )
                                ]
                            ),
                            # Seção de informações e gráficos
                            dmc.GridCol(
                                span=9,
                                children=[
                                    dmc.Card(
                                        children=[
                                            dmc.CardSection(
                                                dmc.Text("Informações do Autor", fw=700, size="lg"),
                                                withBorder=True, inheritPadding=True, py="xs"
                                            ),
                                            dmc.Stack(
                                                gap="lg",
                                                children=[
                                                    dmc.Text(id='total-citacoes'),
                                                    # Alteração: removido o dcc.Graph
                                                    dmc.Paper(
                                                        id='nuvem-tags',
                                                        withBorder=True,
                                                        p="lg",
                                                        children=[
                                                            dmc.Text("Nuvem de Tags", ta="center", fw=700),
                                                            html.Img(id='wordcloud-img', style={'width': '100%'})
                                                        ]
                                                    ),
                                                    dmc.Divider(my="md"),
                                                    dmc.Text("Citações", fw=700, size="lg"),
                                                    dmc.SimpleGrid(
                                                        id='lista-citacoes',
                                                        cols=1, spacing="lg"
                                                    )
                                                ]
                                            )
                                        ],
                                        withBorder=True, shadow="sm", radius="md", p="xl"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    
    return children