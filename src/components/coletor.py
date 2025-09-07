import csv
import re
import requests

from urllib.request import urlopen 
from bs4 import BeautifulSoup


def raspagem_quotes_toscrape(url: str):
    
    html = urlopen(url=url) 
    
    
    soup = BeautifulSoup(html, 'html.parser') 

    page_url = '/'    
    list_quote = []

    print('Iniciando a raspagem de dados das citações...')

    while page_url:
        full_url = url + page_url
        print(f'Raspando a página: {full_url}')

        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        regex = r'>(.*?)<'

        for i in soup.find_all('div', class_='quote'):
            
            # Separa Tags
            list_tags = []
            for t in i.find_all('a', class_='tag'):        
                tag_text = str(re.findall(regex, str(t))[0]).strip("'[]")
                #print(tag_text)
                list_tags.append(tag_text)
            
            
            list_quote.append({
                'autor' : i.find('small', class_='author').text,        
                'citacao' : i.find('span', class_='text').text,                
                'tags': list_tags,
                'pagina': full_url
            })

        # Encontrar o link para a próxima página
        next_li = soup.select_one('li.next a')
        
        if next_li:
            page_url = next_li['href']
        else:
            page_url = None # Sair do loop quando não houver mais páginas
   
    return list_quote


def raspagem_page_author(url: str):
    
    html = urlopen(url=url) 
    
    # Instanciar BeautifulSoup 
    soup = BeautifulSoup(html, 'html.parser')
    
    page_url = '/'    
    author_data = []     

    print('Iniciando a raspagem de dados das paginas sobre os Autores...')
    
    while page_url:

        full_url = url + page_url
        print(f'Raspando a página: {full_url}')

        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra a primeira citação para extrair o link do autor
        about_href = soup.find_all('a', string='(about)')

        if about_href:
            # Encontra o link 'about' do autor dentro da citação
            regex = r'<a href="(.*?)"'
            author_link = []

            for ah in about_href:        
                author_link.append(re.findall(regex, str(ah))[0])            
            
            for author_page in set(author_link):                
                
                full_url_ator = url + author_page                
                print(f'Raspando a página: {full_url_ator}')
                
                response = requests.get(full_url_ator)
                soup_ator = BeautifulSoup(response.text, 'html.parser')
                
                descricao = str(soup_ator.find('div', class_="author-description").text).strip()
                descricao = descricao.replace(',', '')
                descricao = descricao.replace('.', '')
                descricao = descricao.replace('"', '')
                
                author_data.append(
                    {
                        'author': soup_ator.find('h3', class_="author-title").text,
                        'data nascimento': soup_ator.find('span', class_="author-born-date").text,
                        'local nascimento': str(soup_ator.find('span', class_="author-born-location").text).replace('"',''),
                        'descricao': descricao
                    }
                )                    
        
        # Tentar encontrar o link para a próxima página
        next_li = soup.select_one('li.next a')
        
        if next_li:
            page_url = next_li['href']
        else:
            page_url = None # Sair do loop se não houver mais páginas
    
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


def remove_linhas_duplicadas():
    '''
    Lê o arquivo author.csv com a informações sobre autores que se repetem.
    Remove as linhas duplicadas utilizando pandas.
    Salva em outro arquivo sem as linhas duplicadas.
    '''
    
    import pandas as pd
    
    df = pd.read_csv('../documents/author.csv')    

    df_sem_duplicatas = df.drop_duplicates(subset=['autor'])
    
    df_sem_duplicatas.to_csv('../documents/author_sem_duplicatas.csv', index=False)

    print("Linhas duplicadas removidas e guardadas em 'author_sem_duplicatas.csv'")
    

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
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()