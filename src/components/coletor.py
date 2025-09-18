import csv
import re
import requests
import time
import logging

from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.request import urlopen
from urllib.parse import urljoin 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('coletor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)    


def raspagem_quotes_toscrape(url: str) -> list[dict]:
    
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; ScraperBot/1.0)'}
    page_url = '/'
    resultados: list[dict] = []

    logger.info('Iniciando a raspagem de dados das citações...')

    while page_url:
        full_url = urljoin(url, page_url)
        logger.info('Raspando a página: %s', full_url)

        try:
            resp = requests.get(full_url, headers=headers, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error('Falha ao acessar %s: %s', full_url, e)
            break

        soup = BeautifulSoup(resp.text, 'html.parser')

        for q in soup.find_all('div', class_='quote'):
            tags = [a.get_text(strip=True) for a in q.find_all('a', class_='tag')]
            resultados.append({
                'autor':   q.find('small', class_='author').get_text(strip=True),
                'citacao': q.find('span', class_='text').get_text(strip=True),
                'tags':    tags,
                'pagina':  full_url
            })

        next_a = soup.select_one('li.next a')
        page_url = next_a['href'] if next_a else None

    return resultados


def raspagem_page_author(url: str, delay: float = 0.8, timeout: int = 10) -> List[Dict[str, str]]:
    '''
    Raspagem de autores a partir de um site paginado.
    Retorna lista de dicionários com chaves: 'author', 'data_nascimento', 'local_nascimento', 'descricao'.
    '''
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; my-scraper/1.0)'})
    author_data: List[Dict[str, str]] = []
    visited_author_urls = set()
    
    next_path: Optional[str] = '/'

    while next_path:
        page_url = urljoin(url, next_path)
        logger.info(f'Raspando página: {page_url}')
        try:
            resp = session.get(page_url, timeout=timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.exception(f'Falha ao acessar {page_url}: {e}')
            break

        soup = BeautifulSoup(resp.text, 'html.parser')
        
        about_anchors = soup.find_all('a', string='(about)')
                
        for ah in about_anchors:            
            href = ah.get('href')
            if not href:
                continue
            author_url = urljoin(url, href)
            if author_url in visited_author_urls:
                continue
            visited_author_urls.add(author_url)

            logger.info(f'Raspando autor: {author_url}')
            try:
                r2 = session.get(author_url, timeout=timeout)
                r2.raise_for_status()
            except requests.RequestException as e:
                logger.warning(f'Erro ao acessar página do autor {author_url}: {e}')
                continue

            soup_a = BeautifulSoup(r2.text, 'html.parser')
            # uso de get_text(strip=True) e checagem de None
            name_tag = soup_a.find('h3', class_='author-title')
            date_tag = soup_a.find('span', class_='author-born-date')
            place_tag = soup_a.find('span', class_='author-born-location')
            desc_tag = soup_a.find('div', class_='author-description')

            name = name_tag.get_text(strip=True) if name_tag else ''
            born_date = date_tag.get_text(strip=True) if date_tag else ''
            born_location = place_tag.get_text(strip=True) if place_tag else ''
            descricao = desc_tag.get_text(' ', strip=True) if desc_tag else ''
            # limpeza controlada (remove quebras de linha e aspas extras)
            descricao = re.sub(r'["\u201c\u201d]', '', descricao)

            author_data.append({
                'author': name,
                'data_nascimento': born_date,
                'local_nascimento': born_location,
                'descricao': descricao
            })

            time.sleep(delay)  # respeitar servidor

        # Pegar link 'next'
        next_li = soup.select_one('li.next a')
        if next_li and next_li.get('href'):
            next_path = next_li['href']
        else:
            next_path = None

        time.sleep(delay)

    return author_data


def cria_file_csv(dados, nome_file):
  
    # Obter os nomes dos campos (chaves dos dicionários)
    chaves = dados[0].keys()

    with open(nome_file, 'w', newline='') as file_csv:
        escritor = csv.DictWriter(file_csv, fieldnames=chaves)

        # Escrever o cabeçalho
        escritor.writeheader()

        # Escrever os dados
        escritor.writerows(dados)


def main():
    try:
        url = 'http://quotes.toscrape.com'

        file_author = '../documents/author.csv'
        cria_file_csv(raspagem_page_author(url=url), file_author)

        file = '../documents/dados.csv'
        cria_file_csv(raspagem_quotes_toscrape(url=url), file)

        print('-' * 30)
        print(f'Raspagem concluída!')    
    except Exception as e:
        print(f'Erro: {e}')


if __name__ == '__main__':
    main()