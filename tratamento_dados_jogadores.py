import pandas as pd
from datetime import datetime
import re

def drop_columns(df, columns):
    """Remove colunas desnecessárias e exibe o número de colunas descartadas."""
    df.drop(columns, axis=1, inplace=True, errors='ignore')


def verificar_posicoes(df, column_name):
    """Transforma as posições dos jogadores em colunas binárias ('sim' ou '')."""
    mapeamento_posicoes = {
        "Atacante": "Atacante",
        "Defensor": "Defensor",
        "Goleiro": "Goleiro",
        "Meia Atacante": "Meia Atacante",
        "Meia Atacante C": "Meia Atacante",
        "Meia Atacante Direito": "Ponta Direita",
        "Meia Atacante Esquerdo": "Ponta Esquerda",
        "Meiocampista": "Meio Campista",
        "Meio Campo MC": "Meio Campista",
        "Meio Campo MDireito": "Meia pela Direita",
        "Meio Campo MEsquerdo": "Meia pela Esquerda",
        "Meiocampista Defensivo": "Volante",
        "Zagueiro": "Zagueiro",
        "Zagueiro MCDireito": "Zagueiro",
        "Zagueiro ZADireito": "Lateral Direito",
        "Zagueiro ZAEsquerdo": "Lateral Esquerdo",
    }

    posicoes = list(set(mapeamento_posicoes.values()))
    df[posicoes] = ""

    def transformar_posicao(value):
        if pd.isna(value) or value.strip() == "":
            return {}

        value = re.sub(r"[\[\]']", "", value)  # Remove colchetes e aspas
        value = re.sub(r"\s+", " ", value.strip())  # Remove espaços extras

        matches = re.findall(r"(\w+(?:\s\w+)*)\s*\(([^)]+)\)", value)
        positions = [pos.strip() for pos, variations in matches]
        for pos, variations in matches:
            positions.extend([f"{pos} {v.strip()}" for v in variations.split(",")])

        for part in re.split(r",\s*", value):
            if "(" not in part and part.strip():
                positions.append(part.strip())

        return {mapeamento_posicoes.get(pos, ""): "sim" for pos in positions if pos in mapeamento_posicoes}

    for index, row in df.iterrows():
        mapped_positions = transformar_posicao(row[column_name])
        for col in mapped_positions:
            df.at[index, col] = "sim"

    return df

def calcular_estatisticas_por_jogo(df, col_total, col_jogos, col_resultado):
    """Calcula estatísticas por jogo, tratando valores nulos para evitar divisão por zero."""
    df[col_resultado] = df[col_total].div(df[col_jogos]).fillna(0).replace([float('inf'), -float('inf')], 0)

def calcular_taxas(df, col_numerador, col_denominador, col_resultado):
    """Calcula taxas percentuais de acerto, tratando valores nulos e divisão por zero."""
    df[col_resultado] = df[col_numerador].div(df[col_denominador]).fillna(0).replace([float('inf'), -float('inf')], 0)

cabecalho = [
    "ID_jogador",
    "ID_Time_atual",
    "Jogador",
    "Time Atual",
    "Data Nascimento",
    "Nacionalidade",
    "Posições",
    "ID_regiao",
    "Nome Região",
    "ID_campeonato",
    "Campeonato",
    "ID_temporada_campeonato",
    "IsOpta",
    "StageId",
    "ID_regiao_campeonato",
    "Região do Time",
    "Seleção",
    "TournamentShortName",
    "SeasonName",
    "ID_time",
    "Time",
    "Código da Região do Time",
    "Código da Região",
    "PlayedPositionsRaw",
    "PositionText",
    "PositionShort",
    "PositionLong",
    "Name",
    "Height",
    "Weight",
    "FirstName",
    "LastName",
    "KnownName",
    "WSName",
    "DateOfBirth",
    "Age",
    "Field",
    "Atualmente Joga nesse time",
    "Jogos Titular",
    "Entrou no Decorrere do Jogo",
    "Foi Subtituído",
    "Cartões Amarelo",
    "Segundo Amarelo",
    "Cartões Vermelho",
    "Total Gols",
    "Total Assistências",
    "Total de Passes",
    "Passes Certos",
    "Duelos Aéreos Ganhos",
    "Duelos Aéreos Perdidos",
    "Nota",
    "Homem do Jogo",
    "Total de Divididas",
    "Total Interceptações",
    "Total Faltas",
    "Impedimentos Ganhos",
    "Total Chutões",
    "Total Dribles Sofridos",
    "Total de Chutes",
    "Chutes no Gol",
    "Chutes Bloqueados",
    "Gols Contra",
    "Total Passes Decisivos",
    "Total de Dribles",
    "Total Faltas Sofridas",
    "Impedimentos",
    "Desarmado",
    "Erro de Domínio",
    "Total de Cruzamentos",
    "Cruzamentos Certos",
    "Total de Bolas Longas",
    "Bolas Longas Certas",
    "Total Bolas Enfiadas",
    "Bolas Enfiadas Certas",
    "Ranking"
] 

colunas_para_drop = [
    "Posições",
    "IsOpta",
    "StageId",
    "TournamentShortName",
    "SeasonName",
    "PlayedPositionsRaw",
    "PositionText",
    "PositionShort",
    "PositionLong",
    "Name",
    "Height",
    "Weight",
    "FirstName",
    "LastName",
    "KnownName",
    "WSName",
    "DateOfBirth",
    "Age",
    "Field",
    "Ranking"
]

cabecalho_final = [
    "ID_jogador",
    "Jogador",
    "ID_Time_atual",
    "Time Atual",
    "Data Nascimento",
    "Idade",
    "Nacionalidade",
    "Atacante",
    "Defensor",
    "Goleiro",
    "Meia Atacante",
    "Ponta Direita",
    "Ponta Esquerda",
    "Meio Campista",
    "Meia pela Direita",
    "Meia pela Esquerda",
    "Volante",
    "Zagueiro",
    "Lateral Esquerdo",
    "Lateral Direito",
    "ID_regiao",
    "Nome Região",
    "ID_campeonato",
    "Campeonato",
    "ID_temporada_campeonato",
    "ID_regiao_campeonato",
    "Região do Time",
    "Seleção",
    "ID_time",
    "Time",
    "Código da Região do Time",
    "Código da Região",
    "Atualmente Joga nesse time",
    "Nota",
    "Homem do Jogo",
    "Total Jogos",
    "Jogos Titular",
    "Entrou no Decorrere do Jogo",
    "Foi Subtituído",
    "Cartões Amarelo",
    "Segundo Amarelo",
    "Cartões Vermelho",
    "Total Gols",
    "Gols por Jogo",
    "Gols Contra",
    "Total de Chutes",
    "Chutes por Jogo",
    "Chutes no Gol",
    "Acertividade dos Chutes",
    "Chutes Bloqueados",
    "Taxa de Chutes Bloqueados",
    "Total Assistências",
    "Assistências por Jogo",
    "Total Participações em Gols",
    "Participações em Gols por Jogo",
    "Total de Passes",
    "Passes por Jogo",
    "Passes Certos",
    "Acertividade dos Passes",
    "Total Passes Decisivos",
    "Passes Decisivos por Jogo",
    "Total de Cruzamentos",
    "Cruzamentos por Jogo",
    "Cruzamentos Certos",
    "Acertividade dos Cruzamentos",
    "Total de Bolas Longas",
    "Bolas Longas por Jogo",
    "Bolas Longas Certas",
    "Acertividade de Bolas Longas",
    "Total Bolas Enfiadas",
    "Bolas Enfiadas por Jogo",
    "Bolas Enfiadas Certas",
    "Acertividade de Bolas Enfiadas",
    "Duelos Aéreos Ganhos",
    "Duelos Aéreos Perdidos",
    "Taxa de Duelo Aéreo Ganho",
    "Total de Divididas",
    "Divididas por Jogo",
    "Total Interceptações",
    "Interceptações por Jogo",
    "Total Faltas",
    "Faltas por Jogo",
    "Total Faltas Sofridas",
    "Faltas Sofridas por Jogo",
    "Impedimentos Ganhos",
    "Total Chutões",
    "Chutões por Jogo",
    "Total Dribles Sofridos",
    "Dribles Sofridos por Jogo",
    "Total de Dribles",
    "Dribles por Jogo",
    "Impedimentos",
    "Desarmado",
    "Desarmado por Jogo",
    "Erro de Domínio",
    "Erros de Domínio por Jogo" 
]

# Importação de dados
jogadores_dados = pd.read_csv("jogadores_dados.csv")
jogadores_est = pd.read_csv("jogadores_infos.csv")

# Merge dos datasets
df_completo = pd.merge(jogadores_dados, jogadores_est, on="PlayerId", how="inner")

# Definir cabeçalho corretamente
df_completo.columns = cabecalho

# Tratamento das posições
df_completo = verificar_posicoes(df_completo, "Posições")

# Remoção de colunas desnecessárias
drop_columns(df_completo, colunas_para_drop)

# Tratamento de datas e cálculo da idade
df_completo["Data Nascimento"] = pd.to_datetime(df_completo["Data Nascimento"], format="%d-%m-%Y", errors="coerce")
df_completo["Idade"] = df_completo["Data Nascimento"].apply(lambda x: (datetime.now() - x).days // 365 if pd.notnull(x) else None)

# Ajuste de valores booleanos
df_completo["Seleção"] = df_completo["Seleção"].map({True: "Sim", False: ""})
df_completo["Atualmente Joga nesse time"] = df_completo["Atualmente Joga nesse time"].map({True: "Sim", False: ""})

# Cálculo de total de jogos
df_completo["Total Jogos"] = df_completo[["Jogos Titular", "Entrou no Decorrere do Jogo"]].sum(axis=1).fillna(0)

# Cálculo Participações em Gols
df_completo["Total Participações em Gols"] = df_completo[["Total Gols", "Total Assistências"]].sum(axis=1).fillna(0)

# Estatísticas por jogo
estatisticas_por_jogo = {
    "Total Gols": "Gols por Jogo",
    "Total Assistências": "Assistências por Jogo",
    "Total de Passes": "Passes por Jogo",
    "Total de Divididas": "Divididas por Jogo",
    "Total Interceptações": "Interceptações por Jogo",
    "Total Faltas": "Faltas por Jogo",
    "Total Chutões": "Chutões por Jogo",
    "Total Dribles Sofridos": "Dribles Sofridos por Jogo",
    "Total de Chutes": "Chutes por Jogo",
    "Total de Dribles": "Dribles por Jogo",
    "Total Passes Decisivos": "Passes Decisivos por Jogo",
    "Desarmado": "Desarmado por Jogo",
    "Erro de Domínio": "Erros de Domínio por Jogo",
    "Total de Cruzamentos": "Cruzamentos por Jogo",
    "Total de Bolas Longas": "Bolas Longas por Jogo",
    "Total Bolas Enfiadas": "Bolas Enfiadas por Jogo",
    "Total Faltas Sofridas" : "Faltas Sofridas por Jogo",
    "Total Participações em Gols" : "Participações em Gols por Jogo"
}

for col_total, col_resultado in estatisticas_por_jogo.items():
    calcular_estatisticas_por_jogo(df_completo, col_total, "Total Jogos", col_resultado)

# Cálculo de taxas de acerto
taxas_acerto = {
    ("Passes Certos", "Total de Passes"): "Acertividade dos Passes",
    ("Chutes no Gol", "Total de Chutes"): "Acertividade dos Chutes",
    ("Chutes Bloqueados", "Total de Chutes"): "Taxa de Chutes Bloqueados",
    ("Cruzamentos Certos", "Total de Cruzamentos"): "Acertividade dos Cruzamentos",
    ("Bolas Longas Certas", "Total de Bolas Longas"): "Acertividade de Bolas Longas",
    ("Bolas Enfiadas Certas", "Total Bolas Enfiadas"): "Acertividade de Bolas Enfiadas"
}

for (num, den), res in taxas_acerto.items():
    calcular_taxas(df_completo, num, den, res)

# Calcula taxa de duelos aéreos ganhos
df_completo["Taxa de Duelo Aéreo Ganho"] = (df_completo["Duelos Aéreos Ganhos"] / (df_completo["Duelos Aéreos Ganhos"] + df_completo["Duelos Aéreos Perdidos"])).fillna(0)

# Reordenar colunas
df_completo = df_completo[cabecalho_final]

# Exportar para Excel
df_completo.to_excel("jogadores_final.xlsx", index=False)
