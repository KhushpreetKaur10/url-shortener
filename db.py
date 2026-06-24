import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="url_DB"
    )
