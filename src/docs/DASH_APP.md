# 🚀 Documentação do Arquivo Principal do Dash

## 📝 Descrição

Este arquivo é o ponto de entrada (ou arquivo principal) do aplicativo web interativo, construído com o framework Dash.

Ele é responsável por:

1. Inicializar a aplicação Dash.
2. Importar o layout visual (layout_children) e a lógica de interatividade (funções de callback).
3. Definir o layout final do aplicativo, envolvendo-o com o tema visual Mantine.
4. Executar o servidor web para que o dashboard possa ser acessado pelo navegador.

## ✨ Funcionalidades

O código implementa três funcionalidades críticas para o funcionamento do dashboard:

1. Inicialização do Aplicativo Dash:

    * Cria uma instância do aplicativo (app = dash.Dash(__name__, ...)) e carrega as folhas de estilo externas do Mantine, garantindo que os componentes visuais importados funcionem corretamente.
    
```Python
app = dash.Dash(__name__, external_stylesheets=[
    "https://unpkg.com/@mantine/dates@7.10.1/styles.css",
    "https://unpkg.com/@mantine/core@7.10.1/styles.css",
])
```

2. Configuração do Layout e Tema:

    * Define a estrutura visual (layout_children()) do dashboard como o layout principal do aplicativo (app.layout).
    * Envolve o layout em um dmc.MantineProvider para aplicar um tema visual global (colorScheme: "light"), garantindo consistência no design.

```Python

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=layout_children()
)
```
3. Execução do Servidor:

    * Usa o bloco padrão if __name__ == '__main__': para garantir que o aplicativo seja executado apenas se o arquivo for iniciado diretamente.
    * O método app.run(debug=True) inicia o servidor web e habilita o modo debug, que permite atualizações automáticas do código durante o desenvolvimento.

## 🧩 Dependências

Este arquivo utiliza dependências para o framework e para os módulos locais que contêm a lógica e o layout:

* dash (Framework Principal. Essencial para criar e executar o aplicativo web interativo)

* dash_mantine_components (Usado para o componente dmc.MantineProvider, que aplica o tema visual do Mantine a todo o dashboard)

* callbaks (Módulo Local. Importa toda a lógica de interatividade e processamento de dados (a função update_dashboard e autores_unicos) que conecta o layout aos dados.)

* layout (Módulo Local. Importa a função que define a estrutura HTML e visual do dashboard.)

## 🏗️ Estrutura do Código

A estrutura é sequencial e segue a ordem típica de inicialização de um aplicativo Dash:

1. Imports

Importa as bibliotecas necessárias e os módulos locais que definem o comportamento e o visual do app.

```Python

import dash
import dash_mantine_components as dmc

from callbaks import * # Importa toda a lógica
from layout import layout_children # Importa a estrutura visual
```

2. Inicialização do AppCria a instância do Dash, incluindo as folhas de estilo externas do Mantine nos external_stylesheets.

```Python

app = dash.Dash(__name__, external_stylesheets=[
    "https://unpkg.com/@mantine/dates@7.10.1/styles.css",
    "https://unpkg.com/@mantine/core@7.10.1/styles.css",
])
```

3. Definição do Layout

Aplica o componente dmc.MantineProvider ao layout principal do aplicativo, utilizando a função layout_children() para construir a interface.

```Python
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=layout_children()
)
```

4. Execução do Servidor

Inicia o servidor web, permitindo que o aplicativo seja executado.

```Python

if __name__ == '__main__':
    app.run(debug=True)

```

