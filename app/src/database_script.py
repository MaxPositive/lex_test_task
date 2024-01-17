import time

import psycopg2
from psycopg2 import sql

# Connection parameters
dbname = "postgres"
user = "postgres"
password = "postgres"
host = "postgres"

def create_connection():
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

def create_tables(cursor):
    # CREATE TABLE short_names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS short_names (
            name TEXT PRIMARY KEY,
            status INTEGER CHECK (status IN (0, 1))
        )
    """)

    # CREATE TABLE full_names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS full_names (
            name TEXT PRIMARY KEY,
            status INTEGER CHECK (status IN (0, 1))
        )
    """)

    # CREATE INDEX idx_short_names_status
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_short_names_status ON short_names (status)
    """)

    # CREATE INDEX idx_full_names_status
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_full_names_status ON full_names (status)
    """)
    print("Tables created successfully")

def insert_short_names(cursor):
    # CREATE SEQUENCE number_sequence
    cursor.execute("""
        CREATE SEQUENCE IF NOT EXISTS number_sequence START 1
    """)

    """
    Опять же тут могут быть проблемы, так как на примере там названия с цифрами в разнобой, а у меня по порядку. Поэтому,
    лучше  проверять на своих данных именно запросы в бд.
    """

    # INSERT INTO short_names
    cursor.execute("""
        INSERT INTO short_names (name, status)
        SELECT 'nazvanie' || nextval('number_sequence')::text,
            CASE WHEN random() < 0.5 THEN 1 ELSE 0 END
        FROM generate_series(1, 700000)
        ON CONFLICT (name) DO NOTHING
    """)

    # DROP SEQUENCE number_sequence
    cursor.execute("""
        DROP SEQUENCE IF EXISTS number_sequence
    """)
    print("Данные для short_names успешно вставлены")

def insert_full_names(cursor):
    # CREATE SEQUENCE number_sequence
    cursor.execute("""
        CREATE SEQUENCE IF NOT EXISTS number_sequence START 1
    """)

    # INSERT INTO full_names
    cursor.execute("""
        INSERT INTO full_names (name)
        SELECT 'nazvanie' || nextval('number_sequence')::text || '.' || substr(md5(random()::text), 1, 3)
        FROM generate_series(1, 500000)
        ON CONFLICT (name) DO NOTHING
    """)

    # DROP SEQUENCE number_sequence
    cursor.execute("""
        DROP SEQUENCE IF EXISTS number_sequence
    """)
    print("Данные для full_names успешно вставлены")

def run_updates(cursor):
    start_time = time.time()
    # FIRST OPTIMIZED
    cursor.execute("""
        UPDATE full_names
        SET status = short_names.status
        FROM short_names
        WHERE 
            SUBSTRING(full_names.name FROM 'nazvanie[0-9]+') = short_names.name;
    """)
    end_time = time.time()
    print("Время выполнения запроса на обновление статуса:", end_time - start_time)

def get_ten_names_from_short_names(cursor):
    cursor.execute("""
        SELECT name, status
        FROM short_names
        LIMIT 10
    """)
    print("10 data из таблицы short_names:", cursor.fetchall())

def get_ten_names_from_full_names(cursor):
    cursor.execute("""
        SELECT name, status
        FROM full_names
        ORDER BY name
        LIMIT 5
    """)
    print("10 data из таблицы full_names:", cursor.fetchall())


def main():
    connection = create_connection()
    cursor = connection.cursor()

    create_tables(cursor)
    insert_short_names(cursor)
    insert_full_names(cursor)
    run_updates(cursor)
    get_ten_names_from_short_names(cursor)
    get_ten_names_from_full_names(cursor)
    print("Все запросы выполнены. Выключаюсь...")

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()

