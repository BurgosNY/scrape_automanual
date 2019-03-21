import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def deputados_federais():
    url = 'https://pt.wikipedia.org/wiki/Lista_de_deputados_federais_do_Brasil_da_56.%C2%AA_legislatura'
    soup = bs(requests.get(url).content, "html.parser")
    estados = soup.find_all("h3")[1:28]
    data = []
    for estado in estados:
        uf = estado.text.split('[')[0].strip()
        table = estado.find_next_sibling('table')
        json = pd.read_html(str(table))[0].to_dict('records')
        for line in json[1:]:
            info = {"nome": line[0],
                    "partido": line[1],
                    "votos": int(''.join(i for i in line[3] if i.isdigit())),
                    "estado": uf,
                    "cargo": "deputado federal"}
            data.append(info)
    return data


def senado():
    data = []
    url = 'https://www25.senado.leg.br/web/senadores/em-exercicio'
    soup = bs(requests.get(url).content, "html.parser")
    table = soup.find("table")
    json = pd.read_html(str(table))[0].to_dict('records')
    for line in json:
        if type(line['Correio Eletrônico']) is str:
            info = {"nome": line['Nome'],
                    "partido": line['Partido'],
                    "estado": line['UF'],
                    "periodo": line['Período'],
                    "cargo": "senado federal"}
            data.append(info)
    return data
