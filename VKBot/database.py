import psycopg2
from config2 import *

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

connection.autocommit = True


def create_table_users():
    # создание таблицы USERS для найденных пользователей
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial,
                first_name varchar(50) NOT NULL,
                last_name varchar(25) NOT NULL,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                vk_link varchar(50));"""
        )
    print("Table USERS was created.")


def create_table_seen_users():  # references users(vk_id)
    # создание таблицы SEEN_USERS для просмотренных пользователей
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id varchar(50) PRIMARY KEY);"""
        )
    print("Table SEEN_USERS was created.")


def insert_data_users(first_name, last_name, vk_id, vk_link):
    # вставка данных в таблицу users
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (first_name, last_name, vk_id, vk_link) 
            VALUES (%s,%s,%s,%s);""",(first_name, last_name, vk_id, vk_link)
        )

def get_data_users():
    # получить данные из таблицы users
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT first_name,
                       last_name,
                       vk_id,
                       vk_link
                       FROM users"""
        )
        return cursor.fetchall()
        #return cursor.fetchone()


def insert_data_seen_users(vk_id : str, index):
    # вставка данных в таблицу seen_users
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO seen_users (vk_id)
                VALUES(%s) RETURNING id;""",(vk_id,)
            )
            return cursor.fetchone()
    except:
        return -1

def select(index):
    # выборка из непросмотренных людей
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT u.first_name,
                    u.last_name,
                    u.vk_id,
                    u.vk_link,
                    su.vk_id
                    FROM users AS u
                    LEFT JOIN seen_users AS su 
                    ON u.vk_id = su.vk_id
                    WHERE su.vk_id IS NULL
                    OFFSET %s;""", (index,)
        )
        return cursor.fetchone()


def drop_users():
    # Удаление таблицы USERS каскадом
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS users CASCADE;"""
        )
        print('Table USERS was deleted.')


def drop_seen_users():
    # Удаление таблицы SEEN_USERS каскадом
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS seen_users CASCADE;"""
        )
        print('Table SEEN_USERS was deleted.')


def creating_database():
    #drop_users()
    #drop_seen_users()
    create_table_users()
    create_table_seen_users()