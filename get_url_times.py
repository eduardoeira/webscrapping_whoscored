import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

# Configuração do Selenium (Caminho para o chromedriver)
options = Options()
options.headless = True  # Rodar sem interface gráfica

# Usando webdriver-manager para gerenciar o ChromeDriver
service = Service(ChromeDriverManager().install())

# Inicializando o navegador
driver = webdriver.Chrome(service=service, options=options)

# Abrir o site do campeonato brasileiro (alterar caso queira)
driver.get('https://br.whoscored.com/regions/31/tournaments/95/brasil-brasileir%C3%A3o')

# Espera até que os times sejam carregados (ajustar conforme necessário)
driver.implicitly_wait(10)

# Encontrar todos os links de times na página
links_times = driver.find_elements(By.XPATH, "//a[contains(@href, '/teams/')]")

# Criar uma lista para armazenar os dados
dados_times = []

# Função para normalizar URLs (remover parâmetros e tudo depois de '/show/')
def normalize_url(url):
    parsed_url = urlparse(url)
    # Cortar a URL até o segmento '/show/' e ignorar o que vem depois
    normalized_url = parsed_url.normalized_url.split('/show/')[0]  # Pega a parte da URL até '/show/'

    return normalized_url

# Extrair nome e link dos times
for link_time in links_times:
    time_nome = link_time.text.strip()
    time_url = link_time.get_attribute('href')
    
    # Normalizar a URL para remover variações
    normalized_url = normalize_url(time_url)
    
    # Adicionar ao resultado se o nome e a URL estiverem presentes
    if time_nome and normalized_url:
        dados_times.append((time_nome, normalized_url))

# Criar o DataFrame
df_times = pd.DataFrame(dados_times, columns=['Time', 'URL'])

# Remover URLs duplicadas
df_times = df_times.drop_duplicates(subset='URL', keep='first')

# Adicionar 'https://br.whoscored.com/' no início e '/show/' no final de cada URL
df_times['URL'] = 'https://br.whoscored.com' + df_times['URL'] + '/show/'


# Salvar o DataFrame em um arquivo .txt com separador de tabulação
df_times.to_csv('times_brasileirao.txt', sep='\t', index=False)

# Fechar o navegador
driver.quit()
