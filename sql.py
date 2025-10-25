import re
from connection import conn

# TABELA = "CARTAZES"
TABELA = "POSTERS"

def get_all_cartazes():
    consulta = f"SELECT * FROM {TABELA} ORDER BY ANO, DATA_RELEASE, TMDB"
    cursor = conn.cursor()
    cursor.execute(consulta)
    dados = cursor.fetchall()
    cursor.close()
    return dados

# def get_cartazes(anos, cores, pasta):
#     if (len(cores) == 0 and len(anos) == 0 and len(pasta) == 0):
#         return get_all_cartazes()
#
#     where = ""
#     if len(anos) > 0:
#         where = f" ANO IN ({', '.join(f"'{ano}'" for ano in anos)})"
#         if 'None' in anos:
#             where = " ANO is null"
#
#     if len(cores) > 0:
#         if len(where) > 0:
#             where = where + " and "
#         where = where + f" CORES IN ({', '.join(f"'{cores}'" for cores in cores)})"
#
#     if len(pasta) > 0:
#         if len(where) > 0:
#             where = where + " and "
#         where = where + f" PASTA IN ({', '.join(f"{pasta}" for pasta in pasta)})"
#
#     consulta = f"SELECT * FROM {TABELA} WHERE {where}  ORDER BY ANO, DATA_RELEASE, TMDB"
#
#     cursor = conn.cursor()
#     cursor.execute(consulta)
#     dados = cursor.fetchall()
#     cursor.close()
#     return dados

# def get_anos():
#     consulta = f"SELECT distinct ANO FROM {TABELA} ORDER BY 1"
#     cursor = conn.cursor()
#     cursor.execute(consulta)
#     dados = [str(row[0]) for row in cursor.fetchall()]
#     cursor.close()
#     return dados
#
# def get_pasta():
#     consulta = f"SELECT distinct PASTA FROM {TABELA} ORDER BY 1"
#     cursor = conn.cursor()
#     cursor.execute(consulta)
#     dados = [str(row[0]) for row in cursor.fetchall()]
#     cursor.close()
#     return dados

def get_dados_by_tmdb(tmdb):
    consulta = f"SELECT * FROM {TABELA} WHERE TMDB = %s"
    param=[tmdb]
    cursor = conn.cursor()
    cursor.execute(consulta, param)
    dados = cursor.fetchall()
    cursor.close()
    return dados

def get_dados_by_id(id):
    consulta = f"SELECT * FROM {TABELA} WHERE ID = %s"
    param=[id]
    cursor = conn.cursor()
    cursor.execute(consulta, param)
    dados = cursor.fetchall()
    cursor.close()
    return dados

def graficoAnoPoster():
    cursor = conn.cursor()
    cursor.execute(f"SELECT coalesce(ANO, 9999) AS ANO, COUNT(*) AS QTDE FROM {TABELA} GROUP BY ANO ORDER BY 1")
    dados = cursor.fetchall()
    cursor.close()
    return dados

def merge(id, tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores):
    try:
        cursor = conn.cursor()

        ano = data_release.year

        if pagina == '':
            pagina = None
        if pasta == '':
            pasta = None

        sinopse = re.sub(r"\n", "", sinopse)
        titulo_original = titulo_original.upper()
        titulo_traduzido = titulo_traduzido.upper()

        dados_filme = get_dados_by_id(id)
        if dados_filme:
            sql = f"""
            UPDATE {TABELA}
            SET imdb            = %s,
                titulo_original = %s,
                titulo_traduzido= %s,
                ano             = %s,
                pagina          = %s,
                pasta           = %s,
                data_release    = %s,
                link_imagem     = %s,
                sinopse         = %s,
                cores           = %s
            WHERE id = %s
            """

            params = [
                imdb,
                titulo_original,
                titulo_traduzido,
                ano,
                pagina,
                pasta,
                data_release,
                link_imagem,
                sinopse,
                cores,
                id
            ]
        else:
            sql = f"""
            INSERT INTO {TABELA} (
                tmdb,
                imdb,
                titulo_original,
                titulo_traduzido,
                ano,
                pagina,
                pasta,
                data_release,
                link_imagem,
                sinopse,
                cores
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            params = [
                tmdb,
                imdb,
                titulo_original,
                titulo_traduzido,
                ano,
                pagina,
                pasta,
                data_release,
                link_imagem,
                sinopse,
                cores
            ]

        cursor.execute(sql, params)
        cursor.close()
        conn.commit()
        return True
    except (Exception, conn.Error) as error:
        print(error)
        return False