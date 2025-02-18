from datetime import date

import pandas as pd
import streamlit as st

import sql

st.set_page_config(
    page_title="Coleção de Posters de Jornal",
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

dados = sql.get_all_cartazes()
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
    "Link TMDB": link_tmdb,
    "Link IMDB": link_imdb,
})

st.dataframe(
    df,
    height=700,
    # width=1800,
    use_container_width=True,
    column_config={
        "Poster": st.column_config.ImageColumn("Poster"),
        "Ano": st.column_config.NumberColumn(format="%d"),
        "TMDB": st.column_config.NumberColumn(format="%d"),
        "Título Original": st.column_config.TextColumn(width="large"),
        "Título Traduzido": st.column_config.Column(width="large"),
        "Imagem": st.column_config.LinkColumn(display_text="🔗"),
        "Link TMDB": st.column_config.LinkColumn(display_text="🔗"),
        "Link IMDB": st.column_config.LinkColumn(display_text="🔗"),
        "Data Release": st.column_config.DateColumn(format="DD-MM-YYYY")
    },
    hide_index=True,
)
