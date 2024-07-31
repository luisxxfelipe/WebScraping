import requests
from bs4 import BeautifulSoup
import re
import math
import csv

def get_site_link(url):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    link_element = soup.find('a', class_='UIIcon__UIIconElement-sc-1fnws5l-0', href=True)
    if link_element:
        return link_element['href']
    else:
        return None

base_url = 'https://ecosystem.hubspot.com/marketplace/solutions/customer-integrations/united-states'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

site = requests.get(base_url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

# Encontrando o elemento <i18n-string> dentro da seção com a classe 'ResultsSection-q0kudf-0'
results_section = soup.find('div', {'data-test-id': 'desktop-controls', 'class': 'ResultsSection-q0kudf-0'})
if results_section:
    element = results_section.find('i18n-string', {'data-key': 'ecosystem-marketplace-solutions-ui.storefront.results.resultsCount.default'})
    
    # Verificação adicional para garantir que encontramos o elemento
    if element:
        # Usando expressão regular para extrair apenas os dígitos
        qtd_itens_number = int(re.search(r'\d+', element.text.strip().split()[-1]).group())
    else:
        print("Elemento com a quantidade de itens não encontrado")
        qtd_itens_number = 0
else:
    print("Seção de resultados não encontrada")
    qtd_itens_number = 0

# Calculando o número total de páginas
total_pages = math.ceil(qtd_itens_number / 40)

# Lista para armazenar os dados das agências
agencies_data = []

for page_number in range(1, total_pages + 1):
    url_pag = f'https://ecosystem.hubspot.com/marketplace/solutions/customer-integrations/united-states?page={page_number}'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    agencies = soup.find_all('div', class_='UISection__ScrollWrapper-zlhef6-0')
    
    # Iterando sobre as agências e extraindo os dados
    for agency in agencies:
        nome_site = agency.find('h5', class_='Heading-8zapsq-0').get_text().strip()
        link_site = get_site_link('https://ecosystem.hubspot.com' + agency.find('a', href=True)['href'])
        
        # Adicionando os dados da agência à lista
        if link_site:
            agencies_data.append({'Nome do site': nome_site, 'Link do site': link_site})

# Salvar em um arquivo CSV com delimitador ',' e separador de texto '"'
csv_file_path = r'C:\Users\Luis\OneDrive\Documentos\Estágio Meerkat\Web\agencias.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Nome do site', 'Link do site']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',', quotechar='"')
    
    writer.writeheader()
    for agency in agencies_data:
        writer.writerow(agency)

print(f'Os dados foram salvos em: {csv_file_path}')
