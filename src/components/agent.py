import csv
import logging
import os
import getpass

# Modelos e Componentes do LangChain
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)    

if not os.getenv('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Enter your Google API key: ')

# --- PROCESSAMENTO E PREPARAÇÃO DOS DADOS CSV ---
def processar_csv_author_preparar_chunks(file_path_csv):
    '''
    Converte os dados brutos de arquivos csv em Documentos do LangChain e os divide em chunks.
    '''
    logger.info('Iniciando processamento e chunking dos documentos...')    
    documentos_langchain = []

    with open(file_path_csv, 'r', newline='', encoding='utf-8') as file_csv:
        dados_brutos = csv.DictReader(file_csv)

        for item in dados_brutos:            
            # Combinamos pergunta e resposta em um único texto para cada author author,data nascimento,local nascimento,descricao,
            conteudo = f'author: {item['author']}\n data nascimento: {item['data nascimento']}\n local nascimento: {item['local nascimento']} \n descricao: {item['descricao']}'
            documento = Document(
                page_content=conteudo,
                metadata={
                    'author': item['author'],
                    'data nascimento': item['data nascimento'],
                    'local nascimento': item['local nascimento'],
                    'descricao': item['descricao'],
                    }
            )
            documentos_langchain.append(documento)
    
    # Text Splitter: Divide os documentos em pedaços menores (chunks)
    # Ideal para textos longos, garantindo que o contexto não se perca.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documentos_langchain)
    
    logger.info(f'{len(chunks)} chunks criados a partir de {len(documentos_langchain)} documentos.')
    return chunks


# --- CRIAÇÃO DA BASE DE CONHECIMENTO VETORIAL ---
def criar_base_vetorial(chunks):
    '''
    Cria a base de dados de vetores usando ChromaDB e embeddings do Gemini AI.
    '''
    logger.info('Criando a base de dados vetorial (Vector Store)...')
    # Modelo de Embeddings: Transforma texto em vetores numéricos
    embeddings = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')

    # ChromaDB que roda em memória.
       
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    logger.info('Base de dados vetorial criada com sucesso!')
    return vectorstore


# --- LÓGICA PRINCIPAL DE ORQUESTRAÇÃO ---
# Definindo o caminho do arquivo CSV
file_author_csv = './documents/author_sem_duplicatas.csv'
chunks_processados_csv_author = processar_csv_author_preparar_chunks(file_author_csv)
vectorstore = criar_base_vetorial(chunks_processados_csv_author)

# --- CONSTRUÇÃO DO PIPELINE DE RAG ---
logger.info('Configurando o pipeline de RAG...')

# O Retriever é responsável por buscar os chunks relevantes na base vetorial
retriever = vectorstore.as_retriever(search_kwargs={'k': 3}) # 'k' é o número de documentos a retornar

# O Prompt Template formata a pergunta do usuário e os documentos recuperados
# para enviar ao modelo de linguagem.
template = '''
Você é um especialista em informações sobre autores. 
Sua tarefa é responder perguntas do usuário usando apenas o contexto fornecido. 
Se a resposta não estiver no contexto, diga que a informação não está disponível.

## Contexto

{contexto_recuperado}

## Pergunta

{pergunta_do_usuario}

## Instruções para a Resposta

1.  Identifique o autor, a data de nascimento, o local de nascimento, a descrição no contexto.
2.  Combine as informações relevantes para responder à pergunta do usuário de forma clara e concisa.
3.  Se a pergunta for sobre um autor, apresente os dados em um texto com linguagem simples de forma clara.      
4.  Mantenha a resposta direta, sem adicionar informações extras ou fazer suposições.
'''

prompt = ChatPromptTemplate.from_template(template)

# O LLM (Large Language Model) que irá gerar a resposta final.
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', temperature=0.7)

# Construção da Cadeia (Chain) RAG com LangChain Expression Language (LCEL)
# Este é o 'cérebro' da aplicação
cadeia_rag = (
    {'contexto_recuperado': retriever, 'pergunta_do_usuario': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

logger.info('Pipeline de RAG pronto!')
