import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Função para obter dados de torneios de um jogador
def get_dados_jogadores(url):
    # Configuração do Selenium (Caminho para o chromedriver)
    options = Options()
    options.headless = True  # Rodar sem interface gráfica

    # Usando webdriver-manager para gerenciar o ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Inicializando o navegador
    driver = webdriver.Chrome(service=service, options=options)

    # Acessando a página
    driver.get(url)
    driver.implicitly_wait(5)

    # Extrair o script da página contendo os dados
    scripts = driver.find_elements(By.TAG_NAME, "script")
    dados_jogadores = None

    for script in scripts:
        if "require.config.params['args']" in script.get_attribute("innerHTML"):
            script_content = script.get_attribute("innerHTML")
            start = script_content.find("tournaments: [") + len("tournaments: ")
            end = script_content.find("],", start) + 1
            json_text = script_content[start:end]
            dados_jogadores = json.loads(json_text)
            break

    # Fechar o navegador
    driver.quit()

    # Se dados de torneios foram encontrados, converter para DataFrame
    if dados_jogadores:
        df = pd.DataFrame(dados_jogadores)
    else:
        df = pd.DataFrame()  # Caso não encontre os dados

    return df

# Carregar lista de URLs
jogadores_urls = pd.read_csv('jogadores_urls.txt', sep='\t')['URL'].tolist()

# Criar um DataFrame vazio para armazenar os dados de todos os jogadores
dados_todos_jogadores = pd.DataFrame()

# Para cada URL, obter os dados e adicionar ao DataFrame principal
for url in jogadores_urls:
    dados_jogador = get_dados_jogadores(url)
    dados_todos_jogadores = pd.concat([dados_todos_jogadores, dados_jogador], ignore_index=True)
    
    # Esperar 5 segundos entre as buscas para não sobrecarregar o site
    time.sleep(5)  # Tempo de espera (em segundos)

# Exibir o DataFrame final com os dados dos torneios
dados_todos_jogadores.to_csv("jogadores_dados.csv", index=False)
