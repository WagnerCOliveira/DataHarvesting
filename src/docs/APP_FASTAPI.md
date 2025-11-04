# 📚 Documentação da API de Análise de Autores com RAG

Este documento descreve a estrutura e o funcionamento de um código Python que implementa uma API para um sistema de Geração Aumentada por Recuperação (RAG - Retrieval-Augmented Generation), focado na análise de autores.

## 📝 Descrição

O código principal configura e executa uma API RESTful utilizando o framework FastAPI. Seu objetivo é fornecer um endpoint que permite aos usuários fazerem perguntas sobre uma base de conhecimento, especificamente informações de autores do Web Site https://quotes.toscrape.com.

### O fluxo de trabalho principal é:

1. Carregar variáveis de ambiente.

2. Inicializar a aplicação FastAPI com metadados.

3. Definir um modelo de dados para a requisição de pergunta.

4. Expor o endpoint de resposta que utiliza uma cadeia RAG (cadeia_rag) para processar a pergunta e retornar a resposta.

```python

app = FastAPI(
    title='API de Análise de Autores com RAG',
    description='Use esta API para fazer perguntas sobre a base de autores e suas descrições do Web Site [https://quotes.toscrape.com](https://quotes.toscrape.com).',
    version='1.0.0'
)
```

## ⚙️ Funcionalidades

A API possui uma funcionalidade principal:

### Resposta a Perguntas (Endpoint /responder)

Este endpoint aceita requisições HTTP POST e é responsável por interagir com a lógica RAG para gerar uma resposta informada.

* Método: POST

* Path: /responder

* Corpo da Requisição (Input): Um objeto JSON que deve conter o campo pergunta.

Modelo de Requisição:

```python
class PerguntaRequest(BaseModel):
    pergunta: str
```

### Lógica de Processamento:

O endpoint recebe a pergunta e a envia para o componente cadeia_rag, que é o motor do sistema RAG (não detalhado neste arquivo). A resposta processada é então retornada ao usuário.

```python
@app.post('/responder', summary='Responde a uma pergunta...')
async def responder_pergunta(request: PerguntaRequest):
    resposta = cadeia_rag.invoke(request.pergunta)
    return {'resposta': resposta}
```

## 📦 Dependências

O código utiliza as seguintes bibliotecas e componentes:

* FastAPI (Framework principal para construção da API)

* uvicorn (Servidor ASGI de alta performance para executar a aplicação FastAPI)

* pydantic (Utilizado para definir o modelo de dados de entrada (PerguntaRequest) e garantir a validação da requisição)

* python-dotenv (Carrega variáveis de ambiente de um arquivo .env (ex: chaves de API))

* Componente RAG (Módulo externo que deve conter a implementação do sistema RAG, acessado através da variável cadeia_rag)

## 💻 Estrutura do Código

O código é organizado nas seguintes etapas sequenciais:

1. Imports: Importação de todas as bibliotecas e módulos necessários.

```python
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
# ...
from components.agent import *
```

2. Configuração de Ambiente: Carregamento de variáveis de ambiente do arquivo .env.

```python
load_dotenv()
```

3. Inicialização da Aplicação: Criação da instância principal da aplicação FastAPI.

```python
app = FastAPI(
    # ... metadados
)
```

4. Modelo de Requisição: Definição do formato de dados esperado para o input.

```python
class PerguntaRequest(BaseModel):
    pergunta: str
```

5. Endpoint de Resposta: Implementação da função assíncrona que lida com a requisição POST e invoca a cadeia RAG.

```python
@app.post('/responder', ...)
async def responder_pergunta(request: PerguntaRequest):
    # ... lógica
```

6. Execução do Servidor: Bloco condicional que inicia o servidor Uvicorn ao executar o script diretamente.

```python
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
```

Este documento cobre a estrutura externa da API, assumindo que a complexa lógica de recuperação e geração de texto está contida e funcional dentro do módulo **components.agent**.