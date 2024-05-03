import streamlit as st
import sql
import pandas as pd
from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode

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

total_linhas_pagina_ag_grid = 30
ano = []
tmdb = []
imdb = []
titulo_original = []
titulo_traduzido = []
pagina = []
pasta = []
link_imagem = []
link_tmdb = []
link_imdb = []

#custom_css = {".ag-header-cell-text": {"font-size": "20px", 'text-overflow': 'revert;', 'font-weight': 1700},
#       ".ag-theme-streamlit": {'transform': "scale(0.8)", "transform-origin": '0 0'}}

cell_renderer =  JsCode("""
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'Imagem';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """)
cell_renderer_tmdb =  JsCode("""
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'Link TMDB';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """)

cell_renderer_imdb =  JsCode("""
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'Link IMDB';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """)

dados = sql.get_all_poster()
# st.write(dados)

for linha in dados:
    tmdb.append(linha[1])
    imdb.append(linha[2])
    titulo_original.append(linha[3])
    titulo_traduzido.append(linha[4])
    ano.append(linha[5])
    pagina.append(linha[6])
    pasta.append(linha[7])
    link_imagem.append(linha[9])
    link_tmdb.append(f"https://www.themoviedb.org/movie/{linha[1]}")
    link_imdb.append(f"https://www.imdb.com/title/{linha[2]}")

df=pd.DataFrame({
    "Ano":ano,
    "TMDB":tmdb,
    "Título Original":titulo_original,
    "Título Traduzido":titulo_traduzido,
    "Pasta":pasta,
    "Página":pagina,
    "Imagem":link_imagem,
    "Link TMDB":link_tmdb,
    "Link IMDB":link_imdb,
})
    #"IMDB":imdb,

gb = GridOptionsBuilder.from_dataframe(df, theme='streamlit')
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=total_linhas_pagina_ag_grid)
gb.configure_column('Ano', minWidth=70, maxWidth=70)
gb.configure_column('TMDB', minWidth=80, maxWidth=80, editable=True)
gb.configure_column('Título Original', minWidth=350, maxWidth=350, editable=True)
gb.configure_column('Título Traduzido', minWidth=350, maxWidth=350, editable=True)
#gb.configure_column('IMDB', minWidth=100,maxWidth=100)
gb.configure_column('Página', minWidth=50, maxWidth=80)
gb.configure_column('Pasta', minWidth=50, maxWidth=70)
gb.configure_column('Imagem', cellRenderer=cell_renderer, minWidth=90, maxWidth=90)
gb.configure_column('Link TMDB', cellRenderer=cell_renderer_tmdb, minWidth=120,maxWidth=100)
gb.configure_column('Link IMDB', cellRenderer=cell_renderer_imdb, minWidth=120,maxWidth=100)
gridoption = gb.build()


col1, col2, col3 = st.columns([0.5,500,0.5])
with col2:
  AgGrid(df,
          gridOptions=gridoption,
          #custom_css=custom_css,
          columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, 
          updateMode=GridUpdateMode.VALUE_CHANGED,
          allow_unsafe_jscode=True
          )