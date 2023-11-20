import streamlit as st
import requests as rq
import datetime
import sql
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Posters de Jornal",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.subheader("Cadastro de Posters", divider='rainbow')

colinicio, colinicio2 = st.columns((1, 5))
with colinicio:
    tmdb = st.text_input('TMDB')
if tmdb:
    resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}?api_key=2b0120b7e901bbe70b631b2273fe28c9&language=pt-BR&include_adult=false')
    if resposta.status_code == 200:
        dados_filme = resposta.json()
        col1, col2 = st.columns((2.5, 1))
        with col1:
            titulo_original = st.text_input('Título Original', value=dados_filme['original_title']).upper()
            titulo_traduzido = st.text_input('Título Traduzido', value=dados_filme['title']).upper()
            col3, col4, col5, col6 = st.columns(4)
            with col3:
                imdb = st.text_input('IMDB', value=dados_filme['imdb_id'])
            with col4:
                # data_release = st.text_input('Data Release', value=dados_filme['release_date'])
                ano = int(dados_filme['release_date'][0:4])
                mes = int(dados_filme['release_date'][5:7])
                dia = int(dados_filme['release_date'][8:])
                data_release = st.date_input('Data Release', datetime.date(ano, mes, dia))
            with col5:
                pasta = st.text_input('Pasta')
            with col6:
                pagina = st.text_input('Pagina')
            link_imagem = st.text_input('Link Imagem', value=f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{dados_filme['poster_path']}")
            cores = st.radio('Colorido', ['Preto Branco', 'Cores'], index=0, horizontal=True)
        with col2:
            st.image(link_imagem, width=200)
        sinopse = st.text_area('Sinopse', value=dados_filme['overview'], height=150)

        resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}/images?api_key=2b0120b7e901bbe70b631b2273fe28c9')
        if resposta.status_code == 200:
                imagens = resposta.json()

                jpgs = imagens['posters']

                div = """ 
                    <style>
                        .table_wrapper{
                        display: block;
                        overflow-x: auto;
                        white-space: nowrap;
                        }
                    </style>
                """

                st.markdown(div, unsafe_allow_html=True)

                colunas = ''

                for jpg in jpgs:
                    colunas = colunas + f"""<td><img width="100px" src="https://image.tmdb.org/t/p/w600_and_h900_bestv2{jpg['file_path']}"></td>"""

                tabela = "<nav aria-label='breadcrumb'><ol class='breadcrumb''><label>Posters Disponíveis</label><div class='table_wrapper'><table><tr>" + colunas + "</tr></table></div></ol></nav>"

                st.markdown(tabela, unsafe_allow_html=True)
        
        st.divider()

        col20, col21, col23 = st.columns([0.8, 0.8, 5])
        with col20:
            if st.button('Inserir'):
                dados = sql.get_dados_poster(tmdb)

                if dados:
                    with col23:
                        st.error('Poster já cadastrado')
                else:
                    if sql.insere(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores):
                        with col23:                        
                            st.success('Poster inserido com Sucesso!')
                    else:
                        with col23:                        
                            st.error('Ops deu erro')
        with col21:
            if st.button('Home'):
                switch_page("home")
    else:
        st.info("Filme não encontrado")


