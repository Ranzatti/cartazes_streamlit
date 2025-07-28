from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import streamlit as st
import pandas as pd
from datetime import datetime
import sql
import numpy as np

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

# @st.dialog("Alteração de Cartaz", width="large")
# def Update(item):
#     st.write(f"Why is {item} your favorite?")
#     titulo_original = st.text_input('Título Original')
#     titulo_traduzido = st.text_input('Título Traduzido')
#     col3, col4, col5, col6 = st.columns(4)
#     with col3:
#         imdb = st.text_input('IMDB')
#     with col4:
#         data_release = st.date_input('Data Release')
#     with col5:
#         pasta = st.text_input('Pasta')
#     with col6:
#         pagina = st.text_input('Pagina')
#     link_imagem = st.text_input('Link Imagem')
#     cores = st.radio('Cor', ['Preto Branco', 'Cores'])
#     sinopse = st.text_area('Sinopse')
#
#     if st.button("Submit"):
#         st.session_state.Update = 0
#         st.rerun()

# Simulação do DataFrame real

dados = sql.get_all_cartazes()
id = []
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
for linha in dados:
    id.append(linha[0])
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
    # "Poster": link_imagem,
    "ID":id,
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
    # "Link TMDB": link_tmdb,
    # "Link IMDB": link_imdb,
})

st.subheader("Cartazes")

esquerdo, direito  = st.columns((5, 3))
with esquerdo:
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection('single', use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        height=700,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        # fit_columns_on_grid_load=True
    )

with direito:
    selected = pd.DataFrame(grid_response.get('selected_rows', [])) if grid_response else pd.DataFrame()
    if not selected.empty:
        registro = selected.iloc[0].to_dict()
        id = int(registro.get("ID", ""))

        # if "Update" not in st.session_state:
        #     id = registro.get("ID", "")
        #     Update(id)
        #
        # if 'Update' in st.session_state:
        #     del st.session_state['Update']

        dados_filme = sql.get_dados_by_id(id)
        # st.write(dados_filme)
        if dados_filme:
            tmdb = dados_filme[0][1]
            imdb = dados_filme[0][2]
            titulo_original = dados_filme[0][3].upper()
            titulo_traduzido = dados_filme[0][4].upper()
            ano = dados_filme[0][5]
            pagina = dados_filme[0][6]
            pasta = dados_filme[0][7]
            data_release = dados_filme[0][8]
            link_imagem = dados_filme[0][9]
            sinopse = dados_filme[0][10]
            cores = 1 if dados_filme[0][11] == "Cores" else 0

        col1, col2 = st.columns(2)
        with col1:
            tmdb = st.text_input('TMDB', value=tmdb, disabled=True)
            ano = st.text_input('ANO', value=ano)
            titulo_original = st.text_input('Título Original', value=titulo_original)
            titulo_traduzido = st.text_input('Título Traduzido', value=titulo_traduzido)
            imdb = st.text_input('IMDB', value=imdb)
            data_release = st.date_input('Data Release', data_release, format="DD/MM/YYYY")
            pasta = st.text_input('Pasta', value=pasta)
            pagina = st.text_input('Pagina', value=pagina)
            link_imagem = st.text_input('Link Imagem', value=link_imagem)
            cores = st.radio('Cor', ["Cores", "Preto Branco"], index=0 if cores == "Cores" else 1, horizontal=True)
        with col2:
            st.image(link_imagem, width=370)
        sinopse = st.text_area('Sinopse', value=sinopse, height=150)

        if st.button("Salvar alterações"):
            st.success("Registro atualizado com sucesso!")


