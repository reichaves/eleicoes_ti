# -*- coding: utf-8
# Reinaldo Chaves (@paidatocandeira)
# Transparency International - Brazil (https://transparenciainternacional.org.br)
# Faz o download de fotos do DivulgaCand a partir de DataFrame que tem os códigos sequencial do TSE
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time
import urllib.request, urllib.parse, urllib.error

# Root URL of the site that is accessed to fetch the photo link
url_raiz = 'http://divulgacandcontas.tse.jus.br/divulga/#/candidato/2018/2022802018/'

# Accesses the dataframe that has the "sequencial" type codes
candidatos = pd.read_excel('fotosrestantes.xlsx',sheet_name='Sheet1', converters={'sequencial': lambda x: str(x), 'cpf': lambda x: str(x),'numero_urna': lambda x: str(x)})

# Function that opens each page and takes the link from the photo
def pegalink(url):
    profile = webdriver.FirefoxProfile()
    browser = webdriver.Firefox(profile)

    browser.get(url)
    time.sleep(10)

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    browser.close()

    link = soup.find("img", {"class": "img-thumbnail img-responsive dvg-cand-foto ng-scope"})['src']

    return link

# Function that downloads the photo and saves it with the code name "cpf"
def baixa_foto(nome, url):
      urllib.request.urlretrieve(url, nome)


# Iteration in the dataframe
for num, row in candidatos.iterrows():
    cpf = "img_" + (row['cpf']).strip()
    uf = (row['uf']).strip()
    print(cpf)
    print("-/-")
    sequencial = (row['sequencial']).strip()

    # Creates full page address
    url = url_raiz + uf + '/' + sequencial

    link_foto = pegalink(url)

    baixa_foto(cpf, link_foto)
