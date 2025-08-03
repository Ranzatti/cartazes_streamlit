from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, JsCode

import sql
from sql import get_pasta, get_anos

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

anos_select = st.sidebar.multiselect('Selecione o ano desejado',
                                     placeholder="Selecione o ano desejado",
                                     options=get_anos(),
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

def convert_date_format(date_str: str) -> str:
    """
    Converte uma string de data do formato 'YYYY-MM-DD' para 'DD-MM-YYYY'.
    Retorna uma string vazia se o formato de origem for inválido, for None ou vazio.

    Args:
        date_str (str): A string de data que pode ser 'YYYY-MM-DD', None ou "".

    Returns:
        str: A string de data convertida para 'DD-MM-YYYY' ou uma string vazia.
    """
    # Verifica se a string é None ou vazia, retornando uma string vazia imediatamente
    if not date_str:
        return ""

    try:
        # Tenta converter a string para um objeto datetime,
        # usando o formato de origem '%Y-%m-%d'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        # Se a conversão for bem-sucedida, formata o objeto para o novo formato
        new_date_str = date_obj.strftime('%d-%m-%Y')

        return new_date_str
    except ValueError:
        # Se a conversão falhar (por exemplo, a data está em outro formato),
        # imprime um aviso no console e retorna uma string vazia
        print(f"Aviso: Não foi possível converter a data '{date_str}'. Verifique o formato.")
        return ""


ano = []
tmdb = []
imdb = []
titulo_original = []
titulo_traduzido = []
pagina = []
pasta = []
data_release = []
poster = []
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
    data_release.append(convert_date_format(linha[8]))
    poster.append(linha[9])
    cores.append(linha[11])
    link_tmdb.append(f"https://www.themoviedb.org/movie/{linha[1]}")
    link_imdb.append(f"https://www.imdb.com/title/{linha[2]}")

df = pd.DataFrame({
    "Poster": poster,
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

# altura = 700
# if (len(dados) < 700):
#     altura = None

# st.dataframe(
#     df,
#     height=altura,
#     # width=1800,
#     use_container_width=True,
#     column_config={
#         "Poster": st.column_config.ImageColumn("Poster", width=2),
#         "Ano": st.column_config.NumberColumn(format="%d", width=2),
#         "TMDB": st.column_config.NumberColumn(format="%d", width=10),
#         "IMDB": st.column_config.TextColumn(width=5),
#         "Título Original": st.column_config.TextColumn(width=500),
#         "Título Traduzido": st.column_config.Column(width=500),
#         "Pasta": st.column_config.NumberColumn(format="%d", width=5),
#         "Página": st.column_config.NumberColumn(format="%d", width=5),
#         # "Imagem": st.column_config.LinkColumn(display_text="🔗"),
#         "Link TMDB": st.column_config.LinkColumn(display_text="🔗", width=10),
#         "Link IMDB": st.column_config.LinkColumn(display_text="🔗", width=10),
#         "Data Release": st.column_config.DateColumn(format="DD-MM-YYYY", width=10)
#     },
#     hide_index=True,
# )


cell_renderer_image = JsCode("""
    class ImageCellRenderer {
        init(params) {
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = '<img src="' + params.value + '" style="width: 100%; height: auto; border-radius: 5px;">';
        }

        getGui() {
            return this.eGui;
        }

        refresh(params) {
            return false;
        }
    }
""")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_selection('single')
gb.configure_default_column(filter=True)  # Ativa filtro para todas as colunas
gb.configure_column("Ano", width=70)
gb.configure_column("TMDB", width=80, editable=True)
gb.configure_column("IMDB", width=80)
gb.configure_column("Pasta", width=70)
gb.configure_column("Página", width=70)
gb.configure_column("Data Release", width=90)
gb.configure_column("Título Original", width=300)
gb.configure_column("Título Traduzido", width=300)
gb.configure_column("Cores", width=90)
gb.configure_column("Link TMDB", editable=True)
gb.configure_column("Link IMDB", editable=True)

gb.configure_column(
    "Poster",
    header_name="Poster",
    cellRenderer=cell_renderer_image,
    autoHeight=True,
    width=80  # Ajuste a largura da coluna para a imagem
)

grid_options = gb.build()

AgGrid(
        df,
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        height=800,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode='AS_INPUT',
        width='100%'
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