from connection import conn
import re

def get_all_poster():
        
        cursor = conn.cursor()

        consulta = """
            SELECT
                *
            FROM
                POSTER
            ORDER BY
                ANO
            """
        cursor.execute(consulta)
        dados = cursor.fetchall()
        cursor.close()
        return dados

def get_dados_poster(tmdb):
        
        cursor = conn.cursor()

        consulta = """
            SELECT
                *
            FROM
                POSTER
            WHERE
                TMDB = %s
            """
        cursor.execute(consulta, (tmdb,))
        dados = cursor.fetchall()
        cursor.close()

        return dados

def insere(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores ):
        ano = data_release.year

        if pagina == '':
              pagina = None
        if pasta == '':
              pasta = None

        sinopse = re.sub(r"\n", "", sinopse)        
        titulo_original = titulo_original.upper()      
        titulo_traduzido = titulo_traduzido.upper()      

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO poster (tmdb, imdb, titulo_original, titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)", [tmdb, imdb, titulo_original.upper(), titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores])
            cursor.close()
            conn.commit()
            return True
        except (Exception, conn.Error) as error:
            print(error)
            return False
        
def update(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores ):
        ano = data_release.year

        if pagina == '':
              pagina = None
        if pasta == '':
              pasta = None

        sinopse = re.sub(r"\n", "", sinopse)
        titulo_original = titulo_original.upper()      
        titulo_traduzido = titulo_traduzido.upper()      

        cursor = conn.cursor()
        try:
            cursor.execute(""" UPDATE poster SET 
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
                WHERE TMDB = %s """, [imdb, titulo_original, titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores, tmdb])
            cursor.close()
            conn.commit()
            return True
        except (Exception, conn.Error) as error:
            print(error)
            return False