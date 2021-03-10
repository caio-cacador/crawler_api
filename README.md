# crawler_api
Este projeto tem como objetivo realizar crawler no site de finanças do yahoo

https://finance.yahoo.com/screener/new

# Requisitos
- Instalação das dependencias

pip install -r requirements.txt

- Download webdriver do mozilla
https://github.com/mozilla/geckodriver/releases

versão 32 bits:
https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux32.tar.gz

versão 64 bits:
https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz

 - OBS: Após isso extrair o arquivo na pasta raiz do projeto


### Como executar: (versão testada: python 3.8)
python run.py

### Como testar a api:
 - Realizar o GET passando o parametro 'region' como no exemplo abaixo:

localhost:5000/stocks?region=argentina


### Status Code mapeados:
- 400 - O argumento 'region' é obrigatório.
- 400 - A região requisitada não foi encontrada.
- 500 - Erro interno no crawler.

## Mudanças
* v1.0.0
 -- Desenvolvimento da api e implementação o crowler