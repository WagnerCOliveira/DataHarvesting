from dotenv import load_dotenv

# Framework para API
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from components.agent import *

load_dotenv()

app = FastAPI(
    title='API de Análise de Autores com RAG',
    description='Use esta API para fazer perguntas sobre a base de autores e suas descrições do Web Site https://quotes.toscrape.com.',
    version='1.0.0'
)

# Modelo de dados para a requisição da API
class PerguntaRequest(BaseModel):
    pergunta: str

@app.post('/responder', summary='Responde a uma pergunta com base no Autores do Web Site https://quotes.toscrape.com')
async def responder_pergunta(request: PerguntaRequest):
    '''
    Recebe uma pergunta e retorna uma resposta gerada pelo sistema RAG.
    '''
    print(f'Recebida pergunta: {request.pergunta}')
    resposta = cadeia_rag.invoke(request.pergunta)
    print(f'Resposta gerada: {resposta}')
    return {'resposta': resposta}


if __name__ == '__main__':
    print('Iniciando servidor da API...')    
    uvicorn.run(app, host='0.0.0.0', port=8000)

