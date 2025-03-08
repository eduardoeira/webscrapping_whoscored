import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Carregar lista de URLs dos clubes a partir do arquivo txt
df_times = pd.read_csv('times_brasileirao.txt', sep='\t')
clubes_urls = df_times['URL'].tolist()

# Configuração do Selenium
options = Options()
options.headless = True  # Rodar sem interface gráfica
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Lista para armazenar todos os jogadores
jogadores_info = []

# Loop sobre cada clube
for clube_url in clubes_urls:
    driver.get(clube_url)
    time.sleep(5)  # Ajuste conforme necessário
    
    # Encontrar todos os jogadores e suas URLs
    jogadores = driver.find_elements(By.XPATH, "//a[contains(@href, '/players/')]")
    
    for jogador in jogadores:
        nome = jogador.text.strip()
        nome = re.sub(r'\\n', '', nome)  # Remove \n
        if nome:
            url = jogador.get_attribute('href')
            jogador_id_match = re.search(r'/players/(\d+)', url)
            if jogador_id_match:
                jogador_id = jogador_id_match.group(1)
                jogadores_info.append((nome, jogador_id, url))

# Criar DataFrame
df = pd.DataFrame(jogadores_info, columns=["Nome do Jogador", "ID do Jogador", "URL"])

# Limpar nomes
df['Nome do Jogador'] = df['Nome do Jogador'].apply(lambda x: re.sub(r'^\d+\\n', '', x))
df['Nome do Jogador'] = df['Nome do Jogador'].apply(lambda x: re.sub(r'^\d+', '', x))
df['Nome do Jogador'] = df['Nome do Jogador'].apply(lambda x: x.lstrip('\n'))

# Remover URLs duplicadas
df = df.drop_duplicates(subset=['URL'])

# Salvar em um arquivo
df.to_csv('jogadores_urls.txt', sep='\t', index=False)

# Exibir o DataFrame
print(df)

# Fechar navegador
driver.quit()
