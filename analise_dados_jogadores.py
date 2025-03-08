import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
file_path = "jogadores_final.xlsx"
df = pd.read_excel(file_path)

df = df[df['Campeonato'] == 'Brasileirão']
df["Jogador_Time"] = df["Jogador"] + "\n" + df["Time"]

# 1. Quais foram os jogadores com mais jogos?
top_jogadores_jogos = df[["Jogador_Time", "Total Jogos"]].sort_values(by="Total Jogos", ascending=False).head(15)
fig, ax = plt.subplots(figsize=(10, 5))  
sns.barplot(data=top_jogadores_jogos, x="Jogador_Time", y="Total Jogos", ax=ax, color = "gold").set(title="Top 15 Jogadores com Mais Jogos")
ax.set_xlabel("Jogador / Time", fontsize=12)

for p in ax.patches:
    ax.annotate(f"{p.get_height()}", 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=10, color='black')

plt.xticks(rotation=45, fontsize=8)  
plt.tight_layout()
plt.show()


# 2. Quais foram os jogadores que receberam mais cartões (amarelos e vermelhos)?
df["Total Cartões"] = df["Cartões Amarelo"] + df["Cartões Vermelho"]
top_cartoes = df[["Jogador_Time", "Total Cartões"]]
top_cartoes = top_cartoes.sort_values(by="Total Cartões", ascending=False).head(15)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_cartoes, x="Jogador_Time", y="Total Cartões", ax=ax, color = "gold").set(title="Top 15 Jogadores com Mais Cartões")
ax.set_xlabel("Jogador / Time", fontsize=12)

for p in ax.patches:
    ax.annotate(f"{p.get_height()}", 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=10, color='black')
    
plt.xticks(rotation=50, fontsize=9)  
plt.tight_layout()
plt.show()

# 3. Quais foram os jogadores com mais participações em gols?
top_participacoes_gols = df[["Jogador_Time", "Total Participações em Gols"]].sort_values(by="Total Participações em Gols", ascending=False).head(15)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_participacoes_gols, x="Jogador_Time", y="Total Participações em Gols", ax=ax, color = "gold").set(title="Top 15 Jogadores com Mais Participações em Gols")
ax.set_xlabel("Jogador / Time", fontsize=12)

for p in ax.patches:
    ax.annotate(f"{p.get_height()}", 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=10, color='black')

plt.xticks(rotation=50, fontsize=9)  
plt.tight_layout()
plt.show()

# 4. Quais jogadores tiveram a maior média de assistências por jogo?
top_assistencias_media = df[["Jogador", "Assistências por Jogo"]].sort_values(by="Assistências por Jogo", ascending=False)
fig, ax = plt.subplots(figsize=(10, 20))
sns.barplot(data=top_assistencias_media, x="Assistências por Jogo", y="Jogador", ax=ax).set(title="Top 10 Jogadores com Maior Média de Assistências")
plt.tight_layout()
plt.show()

# 5. Qual foi a idade média dos jogadores por time?
idade_media_time = df.groupby("Time")["Idade"].mean().reset_index()
idade_media_time = idade_media_time.sort_values(by="Idade", ascending=False)
sns.barplot(data=idade_media_time, x="Time", y="Idade", ax=ax).set(title="Idade Média dos Jogadores por Time")
plt.tight_layout()
plt.show()

# 6. Quais os jogadores com maiores notas por posição?
top_notas_posicao = df.loc[df.groupby("Posição")["Nota"].idxmax(), ["Jogador", "Posição", "Nota"]]
top_notas_posicao.head()

# 7. Quais jogadores com melhor acertividade nos chutes?
top_precisao_chutes = df[["Jogador", "Acertividade dos Chutes"]].sort_values(by="Acertividade dos Chutes", ascending=False)
fig, ax = plt.subplots(figsize=(10, 40))
sns.barplot(data=top_precisao_chutes, x="Acertividade dos Chutes", y="Jogador", ax=ax).set(title="Top 5 Jogadores com Melhor Acertividade nos Chutes")
plt.tight_layout()
plt.show()

# 8. Quais zagueiros com mais participações em gols?
zagueiros = df[df["Zagueiro"] == "sim"]
top_zagueiros_participacao = zagueiros[["Jogador", "Gols", "Assistências", "Total Participações em Gols"]].sort_values(by="Total Participações em Gols", ascending=False)
fig, ax = plt.subplots(figsize=(10, 40))
sns.barplot(data=top_zagueiros_participacao, x="Total Participações em Gols", y="Jogador", ax=ax).set(title="Top 5 Zagueiros com Mais Participações em Gols")
plt.tight_layout()
plt.show()

# 9. Quais zagueiros com maior taxa de duelos aéreos ganhos?
zagueiros = df[(df["Zagueiro"] == "sim") & (df["Duelos Aérios Ganhos"] > 3)]
top_zagueiros_duelos = zagueiros[["Jogador_Time", "Taxa de Duelo Aéreo Ganho"]].sort_values(by="Taxa de Duelo Aéreo Ganho", ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_zagueiros_duelos, x="Jogador_Time", y="Taxa de Duelo Aéreo Ganho", ax=ax).set(title="Top 10 Zagueiros com Maior Taxa de Duelos Aéreos Ganhos")
ax.set_xlabel("Jogador / Time", fontsize=12)

for p in ax.patches:
    # Exibe a acertividade dos chutes
    acertividade = f"{p.get_height():.2f}"
    # Encontra o total de chutes correspondente a cada jogador
    jogador = top_precisao_chutes.iloc[int(p.get_x() + p.get_width() / 2)]['Jogador_Time']
    total_chutes = top_precisao_chutes[top_precisao_chutes['Jogador_Time'] == jogador]['Total de Chutes'].values[0]
    
    # Coloca tanto a acertividade quanto o total de chutes na barra
    ax.annotate(f"{acertividade}\n({total_chutes})",  
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=10, color='black')


plt.xticks(rotation=50, fontsize=9)  
plt.tight_layout()
plt.show()

# 10. Quais atacantes com maior taxa de duelos aéreos ganhos?
atacantes = df[df["Atacante"] == "sim"]
top_atacantes_duelos = atacantes[["Jogador", "Taxa de Duelo Aéreo Ganho"]].sort_values(by="Taxa de Duelo Aéreo Ganho", ascending=False)
fig, ax = plt.subplots(figsize=(10, 40))
sns.barplot(data=top_atacantes_duelos, x="Taxa de Duelo Aéreo Ganho", y="Jogador", ax=ax).set(title="Top 5 Atacantes com Maior Taxa de Duelos Aéreos Ganhos")
plt.tight_layout()
plt.show()

# 11. Quais meias atacantes com mais passes decisivos por jogo?
meias = df[df["Meia Atacante"] == "sim"]
top_meias_passes = meias[["Jogador", "Passes Decisivos por Jogo"]].sort_values(by="Passes Decisivos por Jogo", ascending=False)
fig, ax = plt.subplots(figsize=(10, 40))
sns.barplot(data=top_meias_passes, x="Passes Decisivos por Jogo", y="Jogador", ax=ax).set(title="Top 5 Meia Atacantes com Mais Passes Decisivos por Jogo")
plt.tight_layout()
plt.show()

# 12. Quais pontas com mais dribles por jogo?
pontas = df[df["Ponta Direita"] == "sim" | df["Ponta Esquerda"] == "sim"]
top_pontas_dribles = pontas[["Jogador", "Dribles por Jogo"]].sort_values(by="Dribles por Jogo", ascending=False)
fig, ax = plt.subplots(figsize=(10, 40))
sns.barplot(data=top_pontas_dribles, x="Dribles por Jogo", y="Jogador", ax=ax).set(title="Top 5 Pontas com Mais Dribles por Jogo")
plt.tight_layout()
plt.show()

# 13. Quais laterais com melhor acertividade nos cruzamentos?
laterais = df[df["Lateral Direito"] == "sim" | df["Lateral Esquerdo"] == "sim"]
top_laterais_cruzamentos = laterais[["Jogador", "Acertividade dos Cruzamentos"]].sort_values(by="Acertividade dos Cruzamentos", ascending=False)
fig, ax = plt.subplots(figsize=(10, 40))
sns.barplot(data=top_laterais_cruzamentos, x="Acertividade dos Cruzamentos", y="Jogador", ax=ax).set(title="Top 5 Laterias com Maior Acertividade dos Cruzamentos")
plt.tight_layout()
plt.show()

# 14. Quais volantes com menos dribles sofridos por jogo?
volantes = df[df["Volante"] == "sim"]
top_volantes_dribles = volantes[["Jogador", "Dribles Sofridos por Jogo"]].sort_values(by="Dribles Sofridos por Jogo")
fig, ax = plt.subplots(figsize=(10, 40))
sns.barplot(data=top_volantes_dribles, x="Dribles Sofridos por Jogo", y="Jogador", ax=ax).set(title="Top 5 Volantes com Menos Dribles Sofridos por Jogo")
plt.tight_layout()
plt.show()

# 15. Existe correlação entre idade e dribles sofridos por jogo?
correlacao_idade_dribles_sofridos = df[["Idade", "Dribles Sofridos por Jogo"]].corr().iloc[0, 1]
fig, ax = plt.subplots(figsize=(12, 5))
sns.scatterplot(data=df, x="Idade", y="Dribles Sofridos por Jogo", ax=ax).set(title="Correlação entre Idade e Dribles Sofridos por Jogo")
plt.tight_layout()
plt.show()

# 16. Existe correlação entre idade e número de participação em gols?
correlacao_idade_gols = df[["Idade", "Total Participações em Gols"]].corr().iloc[0, 1]
fig, ax = plt.subplots(figsize=(12, 5))
sns.scatterplot(data=df, x="Idade", y="Total Participações em Gols", ax=ax).set(title="Correlação entre Idade e Participação em Gols")
plt.tight_layout()
plt.show()

# 17. Existe correlação entre idade e nota?
correlacao_idade_nota = df[["Idade", "Nota"]].corr().iloc[0, 1]
fig, ax = plt.subplots(figsize=(12, 5))
sns.scatterplot(data=df, x="Idade", y="Nota", ax=ax).set(title="Correlação entre Idade e Nota")
plt.tight_layout()
plt.show()

