from datetime import datetime

import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, JsCode

def monta_grid_pandas(df):
    st.dataframe(
        df,
        height=700,
        # width=1800,
        use_container_width=True,
        column_config={
            "Poster": st.column_config.ImageColumn("Poster", width=2),
            "ID": st.column_config.NumberColumn("ID", width=1),
            "Ano": st.column_config.NumberColumn(format="%d", width=2),
            "TMDB": st.column_config.NumberColumn(format="%d", width=10),
            "IMDB": st.column_config.TextColumn(width=10),
            "Título Original": st.column_config.TextColumn(width=600),
            "Título Traduzido": st.column_config.Column(width=600),
            "Pasta": st.column_config.NumberColumn(format="%d", width=5),
            "Página": st.column_config.NumberColumn(format="%d", width=5),
            # "Imagem": st.column_config.LinkColumn(display_text="🔗"),
            "Link TMDB": st.column_config.LinkColumn(display_text="🔗", width=10),
            "Link IMDB": st.column_config.LinkColumn(display_text="🔗", width=10),
            "Data Release": st.column_config.DateColumn(format="DD-MM-YYYY", width=20)
        },
        hide_index=True,
    )
    st.write(f"Total de Registros: {len(df)} ")

def monta_grid_aggrid(df):
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

    gb.configure_column(
        "Data Release",
        valueFormatter="`${('0'+new Date(value).getDate()).slice(-2)}-${('0'+(new Date(value).getMonth()+1)).slice(-2)}-${new Date(value).getFullYear()}`"
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
