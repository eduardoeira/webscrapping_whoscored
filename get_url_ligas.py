from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import json
import pandas as pd

# Configuração do Selenium (Caminho para o chromedriver)
options = Options()
options.headless = True  # Rodar sem interface gráfica

# Usando webdriver-manager para gerenciar o ChromeDriver
service = Service(ChromeDriverManager().install())

# Inicializando o navegador
driver = webdriver.Chrome(service=service, options=options)


# URL do site
url = "https://br.whoscored.com/"
driver.get(url)

# Extraindo o HTML da página
page_source = driver.page_source

driver.quit()

# Expressão regular para capturar o JSON dentro do script
jogo = re.search(r'var allRegions = (\[.*?\]);', page_source, re.DOTALL)

if jogo:
    raw_json = jogo.group(1)
    
    # Ajustando formato do JSON
    raw_json = re.sub(r'([{,])\s*(\w+)\s*:', r'\1"\2":', raw_json)  # Adiciona aspas em torno das chaves
    raw_json = raw_json.replace("'", "\"")  # Substitui aspas simples por duplas
    raw_json = re.sub(r',\s*}', '}', raw_json)  # Remove vírgulas finais antes de chaves
    raw_json = re.sub(r',\s*]', ']', raw_json)  # Remove vírgulas finais antes de colchetes
    
    try:
        json_data = json.loads(raw_json)
        
        # Criando lista para armazenar os dados
        data = []
        
        # Extraindo informações
        for regiao in json_data:
            if regiao['tournaments']:
                pais = regiao['name']
                league_id = regiao['tournaments'][0]['id']
                url = "https://br.whoscored.com/" + regiao['tournaments'][0]['url']
                data.append([pais, league_id, url])
        
        # Criando DataFrame
        df = pd.DataFrame(data, columns=["País", "ID", "URL"])
        
        # Salvando em um arquivo TXT
        df.to_csv("url_ligas.txt", sep="\t", index=False)
        

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}\nJSON bruto capturado:\n{raw_json}")
else:
    print("Não foi possível encontrar os IDs das ligas no HTML.")
