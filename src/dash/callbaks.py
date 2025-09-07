import ast
from dash import callback
import dash_mantine_components as dmc
import pandas as pd
from dash.dependencies import Input, Output
from wordcloud import WordCloud
import base64
from io import BytesIO

# Carrega os dados do arquivo CSV
try:
    df = pd.read_csv('../documents/dados.csv')
except FileNotFoundError:
    print("Erro: O arquivo 'dados.csv' não foi encontrado. Verifique o caminho.")
    exit()

# Obtém a lista de autores únicos para o seletor
autores_unicos = df['autor'].unique()

# --- Callbacks para interatividade ---
@callback(
    Output('total-citacoes', 'children'),
    Output('wordcloud-img', 'src'),
    Output('lista-citacoes', 'children'),
    Input('dropdown-autor', 'value')
)
def update_dashboard(selected_autor):
    if not selected_autor:
        return (
            dmc.Text("Nenhum autor selecionado."),
            {},
            []
        )

    # Filtra o DataFrame pelo autor selecionado
    df_autor = df[df['autor'] == selected_autor]    
    
    # Convertendo a coluna 'tags' de lista para string
    df_autor['tags'] = df_autor['tags'].apply(ast.literal_eval)
    df_autor['tags'] = df_autor['tags'].apply(lambda x: ', '.join(x))    

    # 1. Total de Citações
    total_citacoes = len(df_autor)
    total_citacoes_text = f"Total de citações de {selected_autor}: {total_citacoes}"

    # 2. Análise de Tags
    all_tags = ' '.join(df_autor['tags'].dropna().str.replace(',', ' '))
    #print(all_tags, type(all_tags))
    tags_count = pd.Series(all_tags).str.strip().value_counts().reset_index()
    tags_count.columns = ['tag', 'count']
        
    if all_tags:
        wordcloud = WordCloud(
            width=600,
            height=150,
            background_color='white',
            colormap='viridis',
            min_font_size=10
        ).generate(all_tags)

        # Converte a nuvem de palavras em uma imagem codificada em base64
        img_buffer = BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        encoded_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        image_src = f"data:image/png;base64,{encoded_image}"
    else:
        # Se não houver tags, retorna uma imagem vazia
        image_src = ""

    # 3. Lista de Citações e Tags
    lista_citacoes_ui = []
    for _, row in df_autor.iterrows():
        # Transforma a string de tags em uma lista de badges
        if pd.isna(row['tags']):
            badges_tags = []
        else:
            badges_tags = [
                dmc.Badge(tag.strip(), variant="light", color="blue", radius="xl")
                for tag in row['tags'].split(',')
            ]
        
        # Adicionar o link à citação
        citacao_text_component = dmc.Text(f"“{row['citacao']}”", style={'fontStyle': 'italic'}, size="md", fw=500)
        
        # Verifica se o link existe e adiciona o componente de link
        if 'pagina' in row and pd.notna(row['pagina']):
            citacao_component = dmc.Anchor(
                citacao_text_component,
                href=row['pagina'],
                target="_blank",  # Abre o link em uma nova aba
                underline=False # Remove o sublinhado do link
            )
        else:
            citacao_component = citacao_text_component
        
        lista_citacoes_ui.append(
            dmc.Card(
                children=[
                    citacao_component,
                    dmc.Group(badges_tags, gap="xs", mt="sm"),
                ],
                withBorder=True, shadow="sm", radius="md", p="sm", style={'marginBottom': '10px'}
            )
        )

    return total_citacoes_text, image_src, lista_citacoes_ui