# 📚 Documentação do Código: Sistema RAG de Informações sobre Autores

## 📝 Descrição

Este código implementa um sistema de Geração Aumentada por Recuperação (RAG - Retrieval-Augmented Generation) utilizando o framework LangChain e a API do Google Gemini.

O objetivo principal do sistema é responder perguntas sobre autores com base em um conjunto de dados fornecido em um arquivo CSV. Ele faz isso processando o CSV, criando uma base de conhecimento vetorial e, em seguida, usando um modelo de linguagem grande (LLM) para formular respostas precisas com base nos trechos de dados recuperados (chunks).

## ⚙️ Funcionalidades

* Configuração de Logs: Configura um sistema de logging para rastrear o fluxo de execução e erros, salvando logs em agent.log e exibindo-os no console.

* Processamento de CSV: A função processar_csv_author_preparar_chunks lê um arquivo CSV (esperando colunas como author, data nascimento, local nascimento, descricao), transforma cada linha em um Document do LangChain e divide esses documentos em pedaços menores (chunks) usando o RecursiveCharacterTextSplitter.

* Criação de Base Vetorial (Vector Store): A função criar_base_vetorial utiliza embeddings do Google Gemini AI (GoogleGenerativeAIEmbeddings) para converter os chunks de texto em vetores numéricos. Esses vetores são armazenados no ChromaDB (em memória), criando a base de conhecimento pesquisável.

* Pipeline RAG: Constrói um pipeline completo de RAG usando LangChain Expression Language (LCEL), que inclui:

* Retriever: Busca os 3 (k=3) chunks mais relevantes na base vetorial.

* Prompt Template: Formata a consulta do usuário junto com o contexto recuperado para o LLM.

* LLM: Utiliza o modelo gemini-2.0-flash-001 para gerar a resposta final, seguindo as instruções do prompt para ser um especialista em autores.

* Orquestração: O código executa sequencialmente o processamento do CSV, a criação da base vetorial e a construção da cadeia RAG, preparando o sistema para receber perguntas.

## 📦 Dependências

Este projeto requer as seguintes bibliotecas Python, que devem ser instaladas no ambiente:

* csv (Biblioteca padrão do Python)

* logging (Biblioteca padrão do Python)

* os (Biblioteca padrão do Python)

* getpass (Biblioteca padrão do Python)

* langchain-google-genai (Para modelos LLM e Embeddings do Gemini)

* langchain (Framework principal do LangChain)

* langchain-community (Para componentes como Chroma e PyPDFLoader - embora este último não seja usado no fluxo principal)

Nota: A variável de ambiente GOOGLE_API_KEY é essencial e é solicitada ao usuário via getpass se não estiver configurada no ambiente.

## 💻 Estrutura do Código

A estrutura do código é organizada em seções lógicas para facilitar a manutenção e o entendimento do fluxo de trabalho:

1. Configuração Inicial e Importações
    
    * Importação de todas as bibliotecas necessárias (csv, logging, componentes do LangChain).

    * Configuração do sistema de logging para agent.log e console.

    * Verificação e solicitação da Chave API do Google.

```python
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
from langchain_community.document_loaders import PyPDFLoader # Importado, mas não usado no fluxo RAG

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
```

2. Processamento e Preparação dos Dados CSV (processar_csv_author_preparar_chunks)
    
    * Entrada: Caminho do arquivo CSV.

    * Processo: Lê o CSV, cria objetos Document combinando as colunas de autor, data, local e descrição.

    * Saída: Lista de chunks de documentos (chunks) prontos para vetorização.

```python

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
            # Combina os dados relevantes em um único conteúdo
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
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documentos_langchain)
    
    logger.info(f'{len(chunks)} chunks criados a partir de {len(documentos_langchain)} documentos.')
    return chunks

```

3. Criação da Base de Conhecimento Vetorial (criar_base_vetorial)
    
    * Entrada: A lista de chunks.

    * Processo: Inicializa o modelo de embeddings e armazena os vetores dos chunks no ChromaDB.

    * Saída: Um objeto vectorstore do Chroma.

```python

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

```

4. Lógica Principal de Orquestração
    
    * Define o caminho do CSV (file_author_csv).

    * Chama as funções de processamento e criação da base vetorial.

```python

# --- LÓGICA PRINCIPAL DE ORQUESTRAÇÃO ---
# Definindo o caminho do arquivo CSV
file_author_csv = './documents/author_sem_duplicatas.csv'
chunks_processados_csv_author = processar_csv_author_preparar_chunks(file_author_csv)
vectorstore = criar_base_vetorial(chunks_processados_csv_author)

```

5. Construção do Pipeline de RAG
    * Retriever: Configura o mecanismo de busca (vectorstore.as_retriever).

    * Prompt Template: Define o comportamento do agente (template).

    * LLM: Inicializa o modelo ChatGoogleGenerativeAI.

    * Cadeia RAG: Monta o pipeline usando LCEL, conectando a busca de contexto (retriever), o prompt e a geração de resposta pelo LLM.

```python

# --- CONSTRUÇÃO DO PIPELINE DE RAG ---
logger.info('Configurando o pipeline de RAG...')

# O Retriever é responsável por buscar os chunks relevantes na base vetorial
retriever = vectorstore.as_retriever(search_kwargs={'k': 3}) # 'k' é o número de documentos a retornar

# O Prompt Template
template = '''
Você é um especialista em informações sobre autores. 
Sua tarefa é responder perguntas do usuário usando apenas o contexto fornecido. 
Se a resposta não estiver no contexto, diga que a informação não está disponível.

## Contexto

{contexto_recuperado}

## Pergunta

{pergunta_do_usuario}

## Instruções para a Resposta
... (Instruções detalhadas omitidas aqui para brevidade na documentação, mas presentes no código)
'''

prompt = ChatPromptTemplate.from_template(template)

# O LLM (Large Language Model) que irá gerar a resposta final.
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', temperature=0.7)

# Construção da Cadeia (Chain) RAG com LangChain Expression Language (LCEL)
cadeia_rag = (
    {'contexto_recuperado': retriever, 'pergunta_do_usuario': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

logger.info('Pipeline de RAG pronto!')
```