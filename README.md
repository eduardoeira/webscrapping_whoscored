# Web Scraping de Estatísticas de Jogadores do Brasileirão 2024

## Descrição
Este projeto realiza web scraping para coletar e analisar estatísticas de jogadores do Brasileirão 2024. O processo inclui a extração de URLs das principais ligas, clubes e jogadores, seguido pela coleta e tratamento dos dados estatísticos. Embora focado no Brasileirão, o projeto pode ser adaptado para qualquer outra liga.

Os dados foram extraídos do site [WhoScored.com](https://www.br.whoscored.com), uma das principais plataformas de estatísticas de futebol. O site fornece uma vasta quantidade de informações detalhadas sobre jogadores, equipes e competições, incluindo dados avançados como mapas de calor, passes, finalizações, duelos e outros indicadores de desempenho.

## Estrutura do Projeto
O projeto está organizado nos seguintes scripts:

1. **get_url_ligas.py** - Coleta as URLs das principais ligas do mundo.
2. **get_url_times.py** - Obtém as URLs dos times de cada liga.
3. **get_url_jogadores.py** - Obtém as URLs dos jogadores de cada time.
4. **get_info_jogadores.py** - Coleta informações detalhadas dos jogadores.
5. **get_dados_jogadores.py** - Coleta dados e estatísticas dos jogadores.
6. **tratamento_dados_jogadores.py** - Processa, limpa e trata os dados coletados, removendo inconsistências e preparando-os para análise.
7. **analise_dados_jogadores.ipynb** - Um Jupyter Notebook contendo insights gerados a partir dos dados tratados.

## Tecnologias Utilizadas
- **Python** (para automação do scraping e tratamento dos dados)
- **Pandas** (para manipulação de dados)
- **BeautifulSoup/Selenium** (para extração de dados da web)
- **Jupyter Notebook** (para análise exploratória dos dados)

## Como Utilizar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute os scripts na ordem desejada para coleta e tratamento dos dados.
4. Utilize o Jupyter Notebook para visualizar a análise dos dados coletados.

## Contribuição
Contribuições são bem-vindas! Para sugerir melhorias, abra uma issue ou envie um pull request.

## Licença
Este projeto é disponibilizado sob a licença MIT.

