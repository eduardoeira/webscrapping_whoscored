import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Função para extrair as informações de um jogador
def get_info_jogador(url):
    # Configuração do Selenium (Caminho para o chromedriver)
    options = Options()
    options.headless = True  # Executar o navegador sem interface gráfica

    # Usando webdriver-manager para gerenciar o ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Inicializando o navegador
    driver = webdriver.Chrome(service=service, options=options)

    # Acessando a página
    driver.get(url)

    # Esperando o carregamento da página
    driver.implicitly_wait(5)

    # Função para extrair informações
    def get_info(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return None

    # Extrair as informações
    nome = get_info('//h1[@class="header-name"]').replace("\n", "").strip()
    time_atual = get_info('//span[text()="Time Atual: "]/following-sibling::a')
    data_nascimento = get_info('//span[text()="Idade: "]/following-sibling::i')
    nacionalidade = get_info('//span[text()="Nacionalidade: "]/following-sibling::span')
    posicoes = get_info('//span[text()="Posições: "]/following-sibling::span')

    # Extrair PlayerId e CurrentTeamId a partir do script da página
    scripts = driver.find_elements(By.TAG_NAME, "script")
    player_id = None
    current_team_id = None

    for script in scripts:
        if "require.config.params['args']" in script.get_attribute("innerHTML"):
            script_content = script.get_attribute("innerHTML")

            # Extrair PlayerId
            try:
                player_start = script_content.find("playerId:") + len("playerId:")
                player_end = script_content.find(",", player_start)
                player_id = int(script_content[player_start:player_end].strip())

                # Extrair CurrentTeamId
                team_start = script_content.find("currentTeamId:") + len("currentTeamId:")
                team_end = script_content.find("}", team_start)
                current_team_id = int(script_content[team_start:team_end].strip())
            except ValueError:
                print("Erro ao extrair PlayerId ou CurrentTeamId")
            break

    # Organizar os dados em um dicionário
    data = {
        'PlayerId': [player_id],
        'CurrentTeamId': [current_team_id],
        'Nome': [nome],
        'Time Atual': [time_atual],
        'Data Nascimento': [data_nascimento],
        'Nacionalidade': [nacionalidade],
        'Posições': [posicoes.split(',')]  # Dividido por vírgula
    }

    # Criar DataFrame
    df = pd.DataFrame(data)

    # Fechar o navegador
    driver.quit()

    return df


# Carregar lista de URLs dos clubes a partir do arquivo txt
df_jogadores = pd.read_csv('jogadores_urls.txt', sep='\t')
jogadores_urls = df_jogadores['URL'].tolist()


# Criar um DataFrame vazio para armazenar os dados
info_todos_jogadores = pd.DataFrame()

# Para cada URL, obter os dados e adicionar ao DataFrame principal
for url in jogadores_urls:
    info_jogador = get_info_jogador(url)
    info_todos_jogadores = pd.concat([info_todos_jogadores, info_jogador], ignore_index=True)
    
    # Esperar 2 segundos entre as buscas para não sobrecarregar o site
    time.sleep(2)  # Tempo de espera (em segundos)

# Exibir o DataFrame final com todos os jogadores
info_todos_jogadores.to_csv("jogadores_infos.csv", index=False)
