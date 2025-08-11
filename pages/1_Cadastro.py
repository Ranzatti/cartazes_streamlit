import requests
import streamlit as st
import datetime

from streamlit_extras.switch_page_button import switch_page

import sql

st.set_page_config(
    page_title="Cadastro de Posters",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Coloque aqui sua chave do TMDb
TMDB_API_KEY = "2b0120b7e901bbe70b631b2273fe28c9"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w92"

def mostrar_posters_do_filme(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    params = {
        "api_key": TMDB_API_KEY
    }
    resposta = requests.get(url, params=params)

    if resposta.status_code == 200:
        imagens = resposta.json()
        posters = imagens.get('posters', [])

        # Filtra só os cartazes em inglês
        posters_ingles = [p for p in posters if p.get('iso_639_1') == 'en']

        # st.subheader("Capas Oficiais em Inglês")

        num_colunas = 6
        cols = st.columns(num_colunas)

        for i, poster in enumerate(posters_ingles[:30]):
            poster_url = f"https://image.tmdb.org/t/p/w300{poster['file_path']}"
            with cols[i % num_colunas]:
                st.image(poster_url, width=120)

def mostrar_elenco(movie_id, num_colunas=8):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        "api_key": TMDB_API_KEY
    }
    resposta = requests.get(url, params=params)

    if resposta.status_code == 200:
        dados = resposta.json()
        cast = dados.get('cast', [])

        st.subheader("Elenco Principal")

        cols = st.columns(num_colunas)

        atores_com_imagem = [ator for ator in cast if ator.get('profile_path')]

        for i, ator in enumerate(atores_com_imagem):
            img_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{ator['profile_path']}"

            with cols[i % num_colunas]:
                st.image(img_url, width=90)
                st.markdown(
                    f"<p style='font-size:10px; text-align: center;'>{ator['name']}</p>",
                    unsafe_allow_html=True
                )
    else:
        st.error(f"Erro ao buscar elenco: status {resposta.status_code}")


def search_movies(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "pt-BR"
    }
    resp = requests.get(url, params=params, timeout=8)
    resp.raise_for_status()
    return resp.json().get("results", [])

def get_movie_by_id(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "pt-BR"
        }
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()  # Lança um erro para status de erro HTTP
        return resp.json()
    except requests.exceptions.HTTPError as err:
        st.error(f"Erro HTTP: {err}. Verifique se o ID do filme está correto.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None

# Pega parâmetros da URL
params = st.query_params
pagina = params.get("pagina", "busca")
movie_id = params.get("id", None)

st.subheader("Cadastro de Posters", divider='rainbow')

# ------------------- TELA DE BUSCA -------------------
if pagina == "busca":
    escolha = st.radio("Opção de Busca", ["TMDB", "Titulo Original"], horizontal=True)
    if(escolha == "Titulo"):
        query = st.text_input("Digite o nome do filme (mínimo 2 caracteres)")
        if query and len(query) >= 2:
            try:
                with st.spinner("Buscando no TMDb..."):
                    results = search_movies(query)
            except Exception as e:
                st.error(f"Erro ao buscar filmes: {e}")
                results = []

            if not results:
                st.info("Nenhum filme encontrado.")
            else:
                for movie in results[:10]:
                    mid = str(movie.get("id"))
                    title = movie.get("title") or movie.get("original_title", "—")
                    year = (movie.get("release_date") or "")[:4] or "—"
                    poster_path = movie.get("poster_path")
                    poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else None

                    cols = st.columns([1, 6])
                    with cols[0]:
                        if poster_url:
                            st.image(poster_url, width=60)
                        else:
                            st.write("Sem imagem")
                    with cols[1]:
                        if st.button(f"ID: {mid} — {title} ({year})", key=mid):
                            st.query_params["pagina"] = "cadastro"
                            st.query_params["id"] = mid
                            st.rerun()
    else:
        col50, col51 = st.columns((0.5, 1))
        with col50:
            query = st.text_input("Digite o TMDB")

        if query:
            # Tenta converter o input para um número inteiro, pois IDs são numéricos
            try:
                movie_id = int(query)
                # O spinner mostra que a busca está em andamento
                with st.spinner(f"Buscando filme com o ID {movie_id}..."):
                    # Chama a nova função para buscar um único filme
                    movie = get_movie_by_id(movie_id)

            except ValueError:
                # Lida com o caso em que o input não é um número válido
                st.error("O código do TMDb deve ser um número inteiro.")
                movie = None
            except Exception as e:
                # Lida com outros erros inesperados na busca
                st.error(f"Erro ao buscar o filme: {e}")
                movie = None

            # Verifica se um filme foi encontrado
            if not movie:
                st.info("Nenhum filme encontrado com este código.")
            else:
                # Se o filme foi encontrado, exibe as informações e o botão de cadastro
                mid = str(movie.get("id"))
                title = movie.get("title") or movie.get("original_title", "—")
                year = (movie.get("release_date") or "")[:4] or "—"
                poster_path = movie.get("poster_path")
                poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else None

                cols = st.columns([1, 6])
                with cols[0]:
                    if poster_url:
                        st.image(poster_url, width=60)
                    else:
                        st.write("Sem imagem")
                with cols[1]:
                    # O botão agora apenas confirma a seleção do filme
                    if st.button(f"ID: {mid} — {title} ({year})", key=mid):
                        st.query_params["pagina"] = "cadastro"
                        st.query_params["id"] = mid
                        st.rerun()

# ------------------- TELA DE CADASTRO -------------------
elif pagina == "cadastro" and movie_id:

    dados_filme = sql.get_dados_by_tmdb(movie_id)
    # st.write(dados_filme)
    if dados_filme:
        st.error('Já cadastrado')
        vidFilme = dados_filme[0][0]
        vTMDB = dados_filme[0][1]
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
    else:
        st.success('Novo Cadastro')

        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "pt-BR",
            "include_adult": "false"
        }
        resposta = requests.get(url, params=params, timeout=8)
        if resposta.status_code == 200:
            dados_filme = resposta.json()
            vidFilme = None
            vTMDB = movie_id
            vIMDB = dados_filme['imdb_id']
            vTitulo_original = dados_filme['original_title'].upper()
            vTitulo_traduzido = dados_filme['title'].upper()
            ano = int(dados_filme['release_date'][0:4])
            mes = int(dados_filme['release_date'][5:7])
            dia = int(dados_filme['release_date'][8:])
            vPagina = ""
            vPasta = ""
            vLink = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{dados_filme['poster_path']}"
            vSinopse = dados_filme['overview']
            vColorido = 1
        else:
            st.error('Ops deu erro na busca do filme')

    col1, col2 = st.columns((2.5, 1))
    with col1:
        idFilme = st.text_input('ID', value=vidFilme, disabled=True) if vidFilme else None
        tmdb = st.text_input('TMDB', value=movie_id, disabled=True)
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
    with col2:
        st.image(link_imagem, width=200)
    cores = st.radio('Cor', ['Preto Branco', 'Cores'], index=vColorido, horizontal=True)
    sinopse = st.text_area('Sinopse', value=vSinopse, height=150)

    st.divider()

    mostrar_posters_do_filme(movie_id)

    st.divider()

    # pegando o elento
    # mostrar_elenco(movie_id)

    #Botoes
    col20, col21, col22 = st.columns([2, 2, 8])
    with col20:
        if st.button('Salvar', type="primary"):
            if sql.merge(idFilme, tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores):
                st.query_params.clear()
                st.query_params["pagina"] = "busca"
                st.rerun()
            else:
                with col22:
                    st.error('Ops deu erro')

    with col21:
        if st.button("⬅ Voltar"):
            st.query_params.clear()
            st.query_params["pagina"] = "busca"
            st.rerun()

    st.divider()
    # ate aqui




