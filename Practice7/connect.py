import psycopg2
from config import database

def get_connection():
    return psycopg2.connect(
        host=database["host"],
        dbname=database["dbname"],
        user=database["user"],
        password=database["password"],
        port=database["port"]
    )