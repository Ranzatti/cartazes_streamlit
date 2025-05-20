import streamlit

from connection import conn
import re

@streamlit.cache_data
def get_all_cartazes():
    consulta = f"SELECT * FROM CARTAZES ORDER BY ANO, DATA_RELEASE, TMDB"
    cursor = conn.cursor()
    cursor.execute(consulta)
    dados = cursor.fetchall()
    cursor.close()
    return dados

@streamlit.cache_data
def get_cartazes(anos, cores, pasta):
    if (len(cores) == 0 and len(anos) == 0 and len(pasta) == 0):
        return get_all_cartazes()

    where = ""
    if len(anos) > 0:
        where = f" ANO IN ({', '.join(f"'{ano}'" for ano in anos)})"
        if 'None' in anos:
            where = " ANO is null"

    if len(cores) > 0:
        if len(where) > 0:
            where = where + " OR "
        where = where + f" CORES IN ({', '.join(f"'{cores}'" for cores in cores)})"

    if len(pasta) > 0:
        if len(where) > 0:
            where = where + " OR "
        where = where + f" PASTA IN ({', '.join(f"{pasta}" for pasta in pasta)})"

    consulta = f"SELECT * FROM CARTAZES WHERE {where}  ORDER BY ANO, DATA_RELEASE, TMDB"

    cursor = conn.cursor()
    cursor.execute(consulta)
    dados = cursor.fetchall()
    cursor.close()
    return dados

@streamlit.cache_data
def get_anos():
    consulta = f"SELECT distinct ANO FROM CARTAZES ORDER BY 1"
    cursor = conn.cursor()
    cursor.execute(consulta)
    dados = [str(row[0]) for row in cursor.fetchall()]
    cursor.close()
    return dados

@streamlit.cache_data
def get_pasta():
    consulta = f"SELECT distinct PASTA FROM CARTAZES ORDER BY 1"
    cursor = conn.cursor()
    cursor.execute(consulta)
    dados = [str(row[0]) for row in cursor.fetchall()]
    cursor.close()
    return dados

@streamlit.cache_data
def get_dados_cartazes(tmdb):
    consulta = f"SELECT * FROM CARTAZES WHERE TMDB = %s"
    cursor = conn.cursor()
    cursor.execute(consulta, (tmdb,))
    dados = cursor.fetchall()
    cursor.close()
    return dados


def insere_cartazes(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse,
                    cores):
    ano = data_release.year

    if pagina == '':
        pagina = None
    if pasta == '':
        pasta = None

    sinopse = re.sub(r"\n", "", sinopse)
    titulo_original = titulo_original.upper()
    titulo_traduzido = titulo_traduzido.upper()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO CARTAZES (tmdb, imdb, titulo_original, titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)",
            [tmdb, imdb, titulo_original.upper(), titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores])
        cursor.close()
        conn.commit()
        return True
    except (Exception, conn.Error) as error:
        print(error)
        return False


def update_cartazes(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse,
                    cores):
    ano = data_release.year

    if pagina == '':
        pagina = None
    if pasta == '':
        pasta = None

    sinopse = re.sub(r"\n", "", sinopse)
    titulo_original = titulo_original.upper()
    titulo_traduzido = titulo_traduzido.upper()

    try:
        cursor = conn.cursor()
        cursor.execute(""" UPDATE CARTAZES SET 
                imdb = %s,
                titulo_original = %s,
                titulo_traduzido = %s,
                ano = %s,
                pagina = %s,
                pasta = %s,
                data_release = %s,
                link_imagem = %s,
                sinopse = %s,
                cores = %s
                WHERE TMDB = %s """,[imdb, titulo_original, titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores, tmdb])
        cursor.close()
        conn.commit()
        return True
    except (Exception, conn.Error) as error:
        print(error)
        return False

@streamlit.cache_data
def graficoAnoPoster():
    cursor = conn.cursor()
    cursor.execute("SELECT coalesce(ANO, 2020) AS ANO, COUNT(*) AS QTDE FROM CARTAZES GROUP BY ANO ORDER BY 1")
    dados = cursor.fetchall()
    cursor.close()
    return dados
