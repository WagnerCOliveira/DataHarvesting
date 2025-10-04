# Funções

<!--ts-->   
   * [Função - raspagem_quotes_toscrape()](#scraper-de-citações--raspagem_quotes_toscrape)
   * [Função - raspagem_page_author()](#raspador-de-autores--raspagem_page_author)
   * [Função - cria_file_csv()](#cria_file_csv--exportador-csv)   
<!--te-->


# Scraper de Citações — `raspagem_quotes_toscrape`

## 📌 Descrição

Este projeto implementa um scraper em Python que percorre todas as páginas do site [Quotes to Scrape](https://quotes.toscrape.com) e coleta informações sobre cada citação: **autor, texto, tags** e a **URL da página**.  

O resultado é retornado em formato estruturado (lista de dicionários).

---

## ⚙️ Funcionalidades
- Navegação automática por todas as páginas de citações.
- Extração de:
  - Autor da citação  
  - Texto da citação  
  - Lista de tags associadas  
  - URL da página de origem  
- Retorno dos dados em formato estruturado (list[dict]).

---

## 📦 Dependências
Bibliotecas necessárias (instale com `pip`):

- [requests](https://pypi.org/project/requests/) → para requisições HTTP  
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) → para parsing e navegação no HTML  

Instalação rápida:
```bash
pip install requests beautifulsoup4
```



## 🗂 Estrutura do Código

### Definição da função

```python
def raspagem_quotes_toscrape(url: str) -> list[dict]:
```

* Cria uma função chamada `raspagem_quotes_toscrape`.
* Recebe como entrada `url` (uma string) — a página inicial do site de citações.
* Retorna uma lista de dicionários (`list[dict]`), cada um representando uma citação.

---

### Inicialização de variáveis

```python
headers = {"User-Agent": "Mozilla/5.0 (compatible; ScraperBot/1.0)"}
page_url = "/"
resultados: list[dict] = []
```

* `headers`: define um "User-Agent" para a requisição HTTP, simulando um navegador.
* `page_url = "/"`: indica que começamos pela página inicial do site.
* `resultados`: lista vazia que vai armazenar todas as citações encontradas.

---

### Mensagem de início

```python
logger.info("Iniciando a raspagem de dados das citações...")
```

* Registra uma mensagem no log informando que o scraper começou.
* `logger` é usado para substituir `print` e ter controle de nível de mensagens (`info`, `error` etc.).

---

### Loop principal de páginas

```python
while page_url:
    full_url = urljoin(url, page_url)
    logger.info("Raspando a página: %s", full_url)
```

* O loop `while` continua enquanto `page_url` tiver um valor (ou seja, enquanto houver próxima página).
* `urljoin(url, page_url)` combina a URL base com o caminho da página atual, formando a URL completa.
* Mostra no log a URL que está sendo raspada.

---

### Requisição HTTP

```python
try:
    resp = requests.get(full_url, headers=headers, timeout=10)
    resp.raise_for_status()
except requests.RequestException as e:
    logger.error("Falha ao acessar %s: %s", full_url, e)
    break
```

* Tenta acessar a página via `requests.get`.
* `timeout=10`: não espera mais que 10 segundos por uma resposta.
* `resp.raise_for_status()`: lança um erro se o servidor responder com erro HTTP (ex.: 404, 500).
* Se houver erro (`RequestException`), registra no log e **encerra o loop** (`break`).

---

### Parse do HTML

```python
soup = BeautifulSoup(resp.text, "html.parser")
```

* Converte o HTML da página em um objeto `BeautifulSoup`, permitindo navegar e buscar elementos com facilidade.

---

### Extração das citações

```python
for q in soup.find_all("div", class_="quote"):
    tags = [a.get_text(strip=True) for a in q.find_all("a", class_="tag")]
    resultados.append({
        "autor":   q.find("small", class_="author").get_text(strip=True),
        "citacao": q.find("span", class_="text").get_text(strip=True),
        "tags":    tags,
        "pagina":  full_url
    })
```

* Para cada `<div class="quote">` na página:

  * Busca todas as tags associadas (`a.tag`) e transforma em uma lista de strings.
  * Extrai:

    * **Autor**: texto dentro de `<small class="author">`.
    * **Citação**: texto dentro de `<span class="text">`.
    * **Tags**: lista extraída.
    * **Página**: URL completa de onde a citação veio.
  * Adiciona todas essas informações como um **dicionário** na lista `resultados`.

---

### Encontrar próxima página

```python
next_a = soup.select_one("li.next a")
page_url = next_a["href"] if next_a else None
```

* Procura o link da próxima página (`li.next a`).
* Se existir, atualiza `page_url` com o `href`; caso contrário, define como `None` para encerrar o loop.

---

### Retorno

```python
return resultados
```

* Retorna a lista de dicionários com as citações completas.

---


## ▶️ Como Executar

1. Clone o repositório ou copie o arquivo Python.
2. Crie um ambiente virtual (opcional, recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / Mac
   .venv\Scripts\activate      # Windows
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

   ou diretamente:

   ```bash
   pip install requests beautifulsoup4
   ```

---

## 📝 Exemplo de Uso

Shell Python:

```python
>>> from scraper import raspagem_quotes_toscrape
>>> import json


>>> url = "https://quotes.toscrape.com"
>>> resultados = raspagem_quotes_toscrape(url)
>>> print(json.dumps(resultados, ensure_ascii=False, indent=2))
```

---

## 📊 Saída Esperada

O retorno será uma lista de dicionários, por exemplo:

```json
[
  {
    "autor": "Albert Einstein",
    "citacao": "“The world as we have created it is a process of our thinking...”",
    "tags": ["change","deep-thoughts","thinking","world"],
    "pagina": "https://quotes.toscrape.com/page/1/"
  },
  ...
  {
    "autor": "Jane Austen",
    "citacao": "“It is a truth universally acknowledged...”",
    "tags": ["truth","love"],
    "pagina": "https://quotes.toscrape.com/page/2/"
  }
]
```

---

## 💡 Código Principal

```python

def raspagem_quotes_toscrape(url: str) -> list[dict]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ScraperBot/1.0)"}
    page_url = "/"
    resultados: list[dict] = []

    logging.info("Iniciando a raspagem de dados das citações...")

    while page_url:
        full_url = urljoin(url, page_url)
        logging.info("Raspando a página: %s", full_url)

        try:
            resp = requests.get(full_url, headers=headers, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            logging.error("Falha ao acessar %s: %s", full_url, e)
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        for q in soup.find_all("div", class_="quote"):
            tags = [a.get_text(strip=True) for a in q.find_all("a", class_="tag")]
            resultados.append({
                "autor":   q.find("small", class_="author").get_text(strip=True),
                "citacao": q.find("span", class_="text").get_text(strip=True),
                "tags":    tags,
                "pagina":  full_url
            })

        next_a = soup.select_one("li.next a")
        page_url = next_a["href"] if next_a else None

    return resultados
```


# Raspador de Autores — `raspagem_page_author`

## 📌 Descrição

Função única que percorre páginas paginadas de um site (p. ex. `quotes.toscrape.com`), encontra links "(about)" relativos a autores, abre cada página de autor e extrai informações básicas (nome, data de nascimento, local e descrição). Retorna uma lista de dicionários com os dados coletados.

---

## ⚙️ Funcionalidades

- Percorre páginas paginadas do site seguindo o link `li.next a`.
- Encontra links de autor cujo texto do anchor é exatamente `"(about)"`.
- Acessa cada página de autor (deduplicadas) e extrai:
  - Nome do autor (`h3.author-title`)
  - Data de nascimento (`span.author-born-date`)
  - Local de nascimento (`span.author-born-location`)
  - Descrição (`div.author-description`) — com limpeza simples de vírgulas, pontos e aspas.
- Retorna todos os registros em uma lista Python (`List[Dict[str, str]]`).

---

## 📦 Dependências

Bibliotecas necessárias (pelo menos):

- `requests` — requisições HTTP.
- `beautifulsoup4` (`bs4`) — parsing e extração de HTML.
- `re` — expressões regulares (módulo padrão do Python).
- `urllib` (módulo padrão) — usado no código original com `urlopen`.

---

## 🗂 Estrutura do Código


### Definição da função

```python
def raspagem_page_author(url: str, delay: float = 0.5, timeout: int = 10) -> List[Dict[str, str]]:
```

* `url`: endereço base do site para começar a raspagem.
* `delay`: tempo em segundos entre requisições (para não sobrecarregar o site).
* `timeout`: tempo máximo de espera para respostas HTTP.
* Retorno: uma lista de dicionários (`List[Dict[str,str]]`) com informações dos autores.

---

### Inicialização

```python
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; my-scraper/1.0)"})
author_data: List[Dict[str, str]] = []
visited_author_urls = set()
next_path: Optional[str] = "/"
```

* Cria uma **sessão** HTTP para reutilizar conexões.
* Define um **User-Agent** para se identificar ao servidor.
* `author_data`: lista que vai guardar todos os autores coletados.
* `visited_author_urls`: conjunto para evitar visitar a mesma página de autor mais de uma vez.
* `next_path`: guarda o caminho da próxima página (inicia com `/`).

---

### Loop principal das páginas

```python
while next_path:
    page_url = urljoin(url, next_path)
```

* Enquanto existir uma próxima página (`next_path`), a função continua.
* `urljoin` cria a URL completa da página atual.

---

###  Requisição e parsing da página

```python
resp = session.get(page_url, timeout=timeout)
soup = BeautifulSoup(resp.text, "html.parser")
```

* Faz o **GET HTTP** para baixar a página.
* Usa o **BeautifulSoup** para transformar o HTML em objeto navegável.

---

###  Buscar links de autores

```python
about_anchors = soup.find_all("a", string=lambda s: s and "(about)" in s)
```

* Procura todos os `<a>` cujo texto contém `(about)`.
* Cada link leva à página de detalhes do autor.

---

### Loop pelos autores da página

```python
for ah in about_anchors:
    href = ah.get("href")
    if not href: continue
    author_url = urljoin(url, href)
    if author_url in visited_author_urls: continue
    visited_author_urls.add(author_url)
```

* Constrói a URL completa de cada autor.
* Pula se o link já foi visitado.
* Marca como visitado adicionando ao `set`.

---

###  Requisição e parsing da página do autor

```python
r2 = session.get(author_url, timeout=timeout)
soup_a = BeautifulSoup(r2.text, "html.parser")
```

* Faz GET na página do autor.
* Converte HTML em `BeautifulSoup` para extrair dados.

---

### Extração de dados do autor

```python
name_tag = soup_a.find("h3", class_="author-title")
date_tag = soup_a.find("span", class_="author-born-date")
place_tag = soup_a.find("span", class_="author-born-location")
desc_tag = soup_a.find("div", class_="author-description")

name = name_tag.get_text(strip=True) if name_tag else ""
born_date = date_tag.get_text(strip=True) if date_tag else ""
born_location = place_tag.get_text(strip=True) if place_tag else ""
descricao = desc_tag.get_text(" ", strip=True) if desc_tag else ""
descricao = re.sub(r'["\u201c\u201d]', '', descricao)
```

* Extrai **nome, data, local e descrição**.
* Usa `get_text(strip=True)` para limpar espaços.
* Remove aspas e caracteres especiais da descrição com regex.

---

### Armazenar dados do autor

```python
author_data.append({
    "author": name,
    "data_nascimento": born_date,
    "local_nascimento": born_location,
    "descricao": descricao
})
```

* Adiciona um **dicionário** com os dados à lista `author_data`.

---

### Aguardar entre requisições

```python
time.sleep(delay)
```

* Espera o tempo definido em `delay` para não sobrecarregar o site.

---

### Encontrar próxima página

```python
next_li = soup.select_one("li.next a")
if next_li and next_li.get("href"):
    next_path = next_li["href"]
else:
    next_path = None
```

* Procura o link de **próxima página**.
* Se não houver, encerra o loop.

---

### Retorno final

```python
return author_data
```

* Retorna a lista de Dicionários completa de autores coletados.

---

Se você quiser, posso desenhar um **diagrama simples** mostrando o fluxo do código — isso ajuda muito a visualizar como as páginas e autores são percorridos.

Quer que eu faça?


---

## ▶️ Como Executar

1. Clone o repositório ou copie o arquivo Python.
2. Crie um ambiente virtual (opcional, recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / Mac
   .venv\Scripts\activate      # Windows
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

   ou diretamente:

   ```bash
   pip install requests beautifulsoup4
   ```

---

## 📝 Exemplo de Uso

Shell Python:

```python
>>> from scraper import raspagem_quotes_toscrape
>>> import json


>>> url = "https://quotes.toscrape.com"
>>> resultados = raspagem_page_author(url)
>>> print(json.dumps(resultados, ensure_ascii=False, indent=2))
```
---

## 📊 Saída Esperada

A função retorna `List[Dict[str, str]]`. Cada item é um dicionário com as chaves (nomes como no código original):

- `author` — nome do autor (string)
- `data nascimento` — data de nascimento (string)
- `local nascimento` — local de nascimento (string)
- `descricao` — descrição do autor (string, com algumas pontuações removidas)

Exemplo de item:

```py
{
  'author': 'Albert Einstein',
  'data nascimento': 'March 14, 1879',
  'local nascimento': 'in Ulm, Germany',
  'descricao': 'Físico teórico conhecido por...'
}
```
---

## 💡 Código Principal

```Python
def raspagem_page_author(url: str, delay: float = 0.5, timeout: int = 10) -> List[Dict[str, str]]:
    """
    Raspagem de autores a partir de um site paginado.
    Retorna lista de dicionários com chaves: 'author', 'data_nascimento', 'local_nascimento', 'descricao'.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; my-scraper/1.0)"})
    author_data: List[Dict[str, str]] = []
    visited_author_urls = set()
    
    next_path: Optional[str] = "/"

    while next_path:
        page_url = urljoin(url, next_path)
        logger.info(f"Raspando página: {page_url}")
        try:
            resp = session.get(page_url, timeout=timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.exception(f"Falha ao acessar {page_url}: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        
        about_anchors = soup.find_all("a", string=lambda s: s and "(about)" in s)

        for ah in about_anchors:
            href = ah.get("href")
            if not href:
                continue
            author_url = urljoin(url, href)
            if author_url in visited_author_urls:
                continue
            visited_author_urls.add(author_url)

            logger.info(f"Raspando autor: {author_url}")
            try:
                r2 = session.get(author_url, timeout=timeout)
                r2.raise_for_status()
            except requests.RequestException as e:
                logger.warning(f"Erro ao acessar página do autor {author_url}: {e}")
                continue

            soup_a = BeautifulSoup(r2.text, "html.parser")
            # uso de get_text(strip=True) e checagem de None
            name_tag = soup_a.find("h3", class_="author-title")
            date_tag = soup_a.find("span", class_="author-born-date")
            place_tag = soup_a.find("span", class_="author-born-location")
            desc_tag = soup_a.find("div", class_="author-description")

            name = name_tag.get_text(strip=True) if name_tag else ""
            born_date = date_tag.get_text(strip=True) if date_tag else ""
            born_location = place_tag.get_text(strip=True) if place_tag else ""
            descricao = desc_tag.get_text(" ", strip=True) if desc_tag else ""
            # limpeza controlada (remove quebras de linha e aspas extras)
            descricao = re.sub(r'["\u201c\u201d]', '', descricao)

            author_data.append({
                "author": name,
                "data_nascimento": born_date,
                "local_nascimento": born_location,
                "descricao": descricao
            })

            time.sleep(delay)  # respeitar servidor

        # Pegar link "next"
        next_li = soup.select_one("li.next a")
        if next_li and next_li.get("href"):
            next_path = next_li["href"]
        else:
            next_path = None

        time.sleep(delay)

    return author_data
```

---



# cria_file_csv — Exportador CSV

## 📌 Descrição

Função utilitária para exportar uma coleção de registros (cada registro representado por um dicionário Python) para um arquivo CSV. A função determina os nomes de coluna (fieldnames) a partir das chaves dos dicionários e grava o cabeçalho seguido das linhas de dados.

---

## ⚙️ Funcionalidades

- Grava uma lista/iterável de dicionários em um arquivo CSV.
- Permite usar a união de todas as chaves encontradas nos registros como cabeçalho (ou apenas as chaves do primeiro registro).
- Trata criação de diretórios ausentes automaticamente.
- Abre o arquivo com `newline=''` e codificação configurável (recomendado `utf-8-sig` para compatibilidade com Excel no Windows).
- Permite controlar o comportamento para chaves extras (`extrasaction='ignore'` ou `'raise'`).
- Registra erros de I/O com `logging` e re-levanta exceções para tratamento externo.

---


## 📦 Dependências

- Módulo padrão `csv` — escrita em CSV usando `DictWriter`.
- `pathlib.Path` — manipulação de caminhos e criação de diretórios.
- `logging` — para notificações de erro (opcional, parte da implementação sugerida).
- (Opcional) `pandas` — alternativa conveniente (`DataFrame.to_csv`) para conjuntos de dados maiores ou transformações adicionais.

> Observação: a versão mínima requer apenas o módulo `csv` da biblioteca padrão. `pathlib` e `logging` também fazem parte da biblioteca padrão do Python.

---

