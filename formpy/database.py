import mysql.connector
from config import DB_CONFIG


def conectar():
    return mysql.connector.connect(**DB_CONFIG)