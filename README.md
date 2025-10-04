
Tabela de conteúdos
---
<!--ts-->   
   * [Tecnologias](#🛠-tecnologias-utilizadas)
   * [Criação Virtualenv](#criação-virtualenv)
   * [Instalação Pacotes](#instalação-de-pacotes)
   * [Acessando Virtualenv](#acessando-virtualenv---wsl-linux)
   * [Componentes](#componentes)
     * [Coletor](#coletor)
   * [Referências](#referências)
   * [Contribuição](#contribuidor)
   * [Autor](#autor)
   * [Licença](#licença)
<!--te-->


Tecnologias Utilizadas
---
As seguintes ferramentas foram usadas na construção do projeto:

- [Python 3.13](https://docs.python.org/pt-br/3/)



### Criação Virtualenv


~~~bash
python3 -m venv .venv
~~~


### Acessando Virtualenv - WSL, Linux



~~~bash
source .venv/bin/activate
~~~

### Acessando Virtualenv - Windows


~~~bash
.venv/Scripts/activate.bat
~~~


### Instalação de Pacotes


~~~bash
python -m pip install -r requirements.txt
~~~


Componentes
===

### Coletor

Este componente é responsavel por gerar arquivos **.csv** onde coletam dados de Autor, Citações, Tgas, links das páginas, e descrição do autor em páginas about(sobre), percorendo todas as páginas do site **http://quotes.toscrape.com** para fins de estudo, pode consultar a documentação deste componente neste [link](https://github.com/WagnerCOliveira/DataHarvesting/blob/main/src/docs/COLETOR.md)

### Agent

Referências
===

- [Python Documentação](https://docs.python.org/pt-br/3/)
- [Pandas Documentação](https://pandas.pydata.org/docs/)


Contribuidor
===

- Wagner da Costa Oliveira

Autor
===

- Wagner da Costa Oliveira

Licença
===

- [GNU General Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.html)