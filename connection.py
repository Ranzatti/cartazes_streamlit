import psycopg2

conn = psycopg2.connect(
    dbname='socorrpm',
    user='socorrpm',
    password='SICSADM',
    host='localhost'
)