import dash
import dash_mantine_components as dmc

from callbaks import *
from layout import layout_children

# Inicializa o aplicativo Dash
# Adicionando os stylesheets externos para garantir que os componentes Mantine funcionem
app = dash.Dash(__name__, external_stylesheets=[
    "https://unpkg.com/@mantine/dates@7.10.1/styles.css",
    "https://unpkg.com/@mantine/core@7.10.1/styles.css",
])

# --- Layout do Dashboard ---
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=layout_children()
)

# Executa o aplicativo
if __name__ == '__main__':
    app.run(debug=True)