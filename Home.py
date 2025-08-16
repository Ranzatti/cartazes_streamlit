import sql
import pandas as pd
import streamlit as st
import altair as alt
import util

##############  para rodar o programa execute no console:  streamlit run Home.py ######################

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

# anos_select = st.sidebar.multiselect('Selecione o ano desejado',
#                                      placeholder="Selecione o ano desejado",
#                                      options=get_anos(),
#                                      label_visibility="collapsed")
#
# cores_select = st.sidebar.multiselect('Selecione a Cor desejada',
#                                       placeholder="Selecione a Cor desejada",
#                                       options=['Preto Branco', 'Cores'],
#                                       label_visibility="collapsed")
#
# pasta_select = st.sidebar.multiselect('Selecione a Pasta desejada',
#                                       placeholder="Selecione a Pasta desejada",
#                                       options=get_pasta(),
#                                       label_visibility="collapsed")

# @st.cache_data
def carregar_cartazes():
    dados = sql.get_all_cartazes()
    df = pd.DataFrame({
        "Poster": [linha[9] for linha in dados],
        "ID": [linha[0] for linha in dados],
        "Ano": [linha[5] for linha in dados],
        "TMDB": [linha[1] for linha in dados],
        "IMDB": [linha[2] for linha in dados],
        "Título Original": [linha[3] for linha in dados],
        "Título Traduzido": [linha[4] for linha in dados],
        "Pasta": [linha[7] for linha in dados],
        "Página": [linha[6] for linha in dados],
        "Data Release": [linha[8] for linha in dados],
        "Cores": [linha[11] for linha in dados],
        "Link TMDB": [f"https://www.themoviedb.org/movie/{linha[1]}" for linha in dados],
        "Link IMDB": [f"https://www.imdb.com/title/{linha[2]}" for linha in dados],
    })
    return df

# with st.spinner("Buscando Cartazes..."):
df = carregar_cartazes()
# dados = sql.get_cartazes(anos_select, cores_select, pasta_select)

util.monta_grid_pandas(df)
# util.monta_grid_aggrid(df)

st.divider()

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
        alt.datum.Ano == 9999,  # If the year is 1810 this test returns True,
        alt.value('red'),  # which sets the bar orange.
        alt.value('steelblue')  # And if it's not true it sets the bar steelblue.
    )
).properties(
    title='Quantidade de cartazes por Ano',
    # width=600,
    height=500
)

st.altair_chart(bar_chart, use_container_width=True)