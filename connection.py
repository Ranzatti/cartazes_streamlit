import psycopg2
from psycopg2 import OperationalError

# conn = psycopg2.connect(
#     # dbname='ranzatti',
#     # user='ranzatti',
#     # password='a',
#     # host='localhost'
#
#     dbname='postgres',
#     user='postgres.kngdhvmwmbcnrcutuuqm',
#     password='11711FIS237',
#     host='aws-0-sa-east-1.pooler.supabase.com'
# )


def get_connection():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres.kngdhvmwmbcnrcutuuqm',
            password='11711FIS237',
            host='aws-0-sa-east-1.pooler.supabase.com',
            port=5432,
            sslmode='require',
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
        return conn
    except OperationalError as e:
        print("Erro ao conectar:", e)
        return None

conn = get_connection()
