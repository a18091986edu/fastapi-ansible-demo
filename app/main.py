# main.py

from fastapi import FastAPI
import psycopg2
import time

app = FastAPI()


def connect_to_db():
    """
    Пытаемся подключиться к БД.
    PostgreSQL может стартовать дольше приложения,
    поэтому делаем несколько попыток.
    """
    while True:
        try:
            conn = psycopg2.connect(
                host="db",            # имя сервиса в docker-compose
                database="mydb",
                user="user",
                password="password"
            )
            print("✅ Connected to database!")
            return conn
        except Exception as e:
            print("⏳ Waiting for DB...", e)
            time.sleep(2)


# Подключаемся при старте
conn = connect_to_db()


@app.get("/")
def read_root():
    return {"message": "Hello with DB! NEW"}


@app.get("/db")
def check_db():
    """
    Проверяем, что БД отвечает
    """
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    return {"db_response": result}