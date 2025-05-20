import streamlit as st
import requests as rq
import datetime
import sql
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Cadastro de Posters",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.subheader("Cadastro de Posters", divider='rainbow')

colinicio, colinicio2 = st.columns((1, 5))
with colinicio:
    tmdb = st.text_input('TMDB')
if tmdb:
    dados_filme = sql.get_dados_cartazes(tmdb)
    if dados_filme:
        #st.write(dados_filme)
        with colinicio2:
            st.caption("")
            st.error('Poster já cadastrado')
            vIMDB = dados_filme[0][2]
            vTitulo_original = dados_filme[0][3].upper()
            vTitulo_traduzido = dados_filme[0][4].upper()
            vPagina = dados_filme[0][6]
            vPasta = dados_filme[0][7]
            ano = int(dados_filme[0][8][0:4])
            mes = int(dados_filme[0][8][5:7])
            dia = int(dados_filme[0][8][8:])
            vLink = dados_filme[0][9]
            vSinopse = dados_filme[0][10]
            vColorido = 1 if dados_filme[0][11] == "Cores" else 0
            bMostraCampos = True
            bModoIncluir = 0
    else:
        with colinicio2:
            st.caption("")
            resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}?api_key=2b0120b7e901bbe70b631b2273fe28c9&language=pt-BR&include_adult=false')
            if resposta.status_code == 200:
                st.success('Novo Cadastro')
                dados_filme = resposta.json()
                vIMDB = dados_filme['imdb_id']
                vTitulo_original = dados_filme['original_title'].upper()
                vTitulo_traduzido = dados_filme['title'].upper()
                ano = int(dados_filme['release_date'][0:4])
                mes = int(dados_filme['release_date'][5:7])
                dia = int(dados_filme['release_date'][8:])
                vPagina = ""
                vPasta = ""
                vLink = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{dados_filme['poster_path']}" if dados_filme['poster_path'] != None else 'https://mardehistorias.files.wordpress.com/2016/01/rolo-de-filme.jpg'
                vSinopse = dados_filme['overview']
                vColorido = 0
                bMostraCampos = True
                bModoIncluir = 1
            else:
                bMostraCampos = False

    if bMostraCampos:
        col1, col2 = st.columns((2.5, 1))
        with col1:
            titulo_original = st.text_input('Título Original', value=vTitulo_original)
            titulo_traduzido = st.text_input('Título Traduzido', value=vTitulo_traduzido)
            col3, col4, col5, col6 = st.columns(4)
            with col3:
                imdb = st.text_input('IMDB', value=vIMDB)
            with col4:
                data_release = st.date_input('Data Release', datetime.date(ano, mes, dia), format="DD/MM/YYYY")
            with col5:
                pasta = st.text_input('Pasta', value=vPasta)
            with col6:
                pagina = st.text_input('Pagina', value=vPagina)
            link_imagem = st.text_input('Link Imagem', value=vLink)
            cores = st.radio('Cor', ['Preto Branco', 'Cores'], index=vColorido, horizontal=True)
        with col2:
            st.image(link_imagem, width=200)
        sinopse = st.text_area('Sinopse', value=vSinopse, height=150)

        # pegando as capinhas
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
        # ate aqui

        # pegando o elento
        resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}/credits?api_key=2b0120b7e901bbe70b631b2273fe28c9')
        if resposta.status_code == 200:
            imagens = resposta.json()
            cast = imagens['cast']

            # Exibindo os elenco horizontalmente com colunas
            st.subheader("Elenco Principal")

            # Defina um tamanho maior para as colunas
            num_colunas = 8  # Defina quantas colunas você quer por linha
            cols = st.columns(num_colunas)

            # carrego todos os posters não nulos num vetor
            atores_com_imagem = [ator for ator in cast if ator.get('profile_path')]

            # varro o vetor e mostro as imagens
            for i, ator in enumerate(atores_com_imagem):
                img_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{ator['profile_path']}"

                # Usa um espaçamento e ajusta a largura da imagem
                with cols[i % num_colunas]:  # Adiciona a imagem na coluna correspondente
                    st.image(img_url, width=90)  # Ajusta a largura da imagem
                    # st.write(ator['name'])  # Exibe o nome do ator abaixo da imagem
                    st.markdown(f"<p style='font-size:10px;  text-align: center;'>{ator['name']}</p>",
                                unsafe_allow_html=True)

            # Se você quiser adicionar uma nova linha após cada conjunto de imagens
            if len(cast) > num_colunas:
                st.write("")
        st.divider()

        #Botoes
        col20, col21, col23 = st.columns([2, 2, 8])
        with col20:
            if st.button('Atualizar', type="primary"):
                if bModoIncluir:
                    if sql.insere_cartazes(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores):
                        with col23:                        
                            st.success('Poster inserido com Sucesso!')
                    else:
                        with col23:                        
                            st.error('Ops deu erro')
                else:
                    if sql.update_cartazes(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores):
                        with col23:                        
                            st.success('Poster alterado com Sucesso!')
                    else:
                        with col23:                        
                            st.error('Ops deu erro')  
                switch_page("home")
        with col21:
            if st.button('Home'):
                switch_page("home")
    else:
        with colinicio2:
            st.info('Filme não encontrado')
