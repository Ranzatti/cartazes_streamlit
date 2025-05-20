import pandas as pd
import streamlit as st
import altair as alt

import sql
from sql import get_pasta

st.set_page_config(
    page_title="Coleção de Cartazes de Jornal",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.subheader("Coleção de Posters", divider='rainbow')

anosCartazes = sql.get_anos()
anos_select = st.sidebar.multiselect('Selecione o ano desejado',
                                     placeholder="Selecione o ano desejado",
                                     options=anosCartazes,
                                     label_visibility="collapsed")

cores_select = st.sidebar.multiselect('Selecione a Cor desejada',
                                      placeholder="Selecione a Cor desejada",
                                      options=['Preto Branco', 'Cores'],
                                      label_visibility="collapsed")

pasta_select = st.sidebar.multiselect('Selecione a Pasta desejada',
                                      placeholder="Selecione a Pasta desejada",
                                      options=get_pasta(),
                                      label_visibility="collapsed")

# st.write(len(anos_select))
# st.write(len(cores_select))
# st.write(pasta_select)


ano = []
tmdb = []
imdb = []
titulo_original = []
titulo_traduzido = []
pagina = []
pasta = []
data_release = []
link_imagem = []
link_tmdb = []
link_imdb = []
cores = []

# dados = sql.get_all_cartazes()
dados = sql.get_cartazes(anos_select, cores_select, pasta_select)
# st.write(dados)

for linha in dados:
    tmdb.append(linha[1])
    imdb.append(linha[2])
    titulo_original.append(linha[3])
    titulo_traduzido.append(linha[4])
    ano.append(linha[5])
    pagina.append(linha[6])
    pasta.append(linha[7])
    data_release.append(linha[8])
    link_imagem.append(linha[9])
    cores.append(linha[11])
    link_tmdb.append(f"https://www.themoviedb.org/movie/{linha[1]}")
    link_imdb.append(f"https://www.imdb.com/title/{linha[2]}")

df = pd.DataFrame({
    "Poster": link_imagem,
    "Ano": ano,
    "TMDB": tmdb,
    "IMDB": imdb,
    "Título Original": titulo_original,
    "Título Traduzido": titulo_traduzido,
    "Pasta": pasta,
    "Página": pagina,
    "Data Release": data_release,
    # "Imagem": link_imagem,
    "Cores": cores,
    "Link TMDB": link_tmdb,
    "Link IMDB": link_imdb,
})

altura = 700
if (len(dados) < 700):
    altura = None

st.dataframe(
    df,
    height=altura,
    # width=1800,
    use_container_width=True,
    column_config={
        "Poster": st.column_config.ImageColumn("Poster", width=2),
        "Ano": st.column_config.NumberColumn(format="%d", width=2),
        "TMDB": st.column_config.NumberColumn(format="%d", width=10),
        "IMDB": st.column_config.TextColumn(width=5),
        "Título Original": st.column_config.TextColumn(width=500),
        "Título Traduzido": st.column_config.Column(width=500),
        "Pasta": st.column_config.NumberColumn(format="%d", width=5),
        "Página": st.column_config.NumberColumn(format="%d", width=5),
        # "Imagem": st.column_config.LinkColumn(display_text="🔗"),
        "Link TMDB": st.column_config.LinkColumn(display_text="🔗", width=10),
        "Link IMDB": st.column_config.LinkColumn(display_text="🔗", width=10),
        "Data Release": st.column_config.DateColumn(format="DD-MM-YYYY", width=10)
    },
    hide_index=True,
)
st.write(f"Total de Registros: {len(dados)} ")

############################################################
######################### GRAFICO ##########################
############################################################
dados = sql.graficoAnoPoster()
ano = []
quantidade = []

i = 0
for dado in dados:
    ano.append(dados[i][0])
    quantidade.append(dados[i][1])
    i += 1

source = pd.DataFrame({
    'Ano': ano,
    'Quantidade': quantidade
})

bar_chart = alt.Chart(source).mark_bar().encode(
    x='Ano:O',
    y='Quantidade',
    color=alt.condition(
        alt.datum.Ano == 2020,  # If the year is 1810 this test returns True,
        alt.value('red'),  # which sets the bar orange.
        alt.value('steelblue')  # And if it's not true it sets the bar steelblue.
    )
).properties(
    title='Quantidade de cartazes por Ano',
    # width=600,
    height=500
)

st.altair_chart(bar_chart, use_container_width=True)