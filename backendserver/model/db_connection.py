import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()


user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')


def conectar_mysql():
    conn = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )

    return conn
