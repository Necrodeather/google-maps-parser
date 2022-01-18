import pymysql
import json

with open("config.json", "r") as json_config:
    config = json.load(json_config)

def create_table():
    with connection:
        with connection.cursor() as cursor:
            create_table = f'USE {config["database"]}; CREATE TABLE IF NOT EXISTS main(id INT NOT NULL AUTO_INCREMENT, S_Name varchar(30))'
            cursor.execute(create_table)
            print("Done!")


try:
    connection = pymysql.connect(
        host = config["host"],
        port = config["port"],
        user = config["user"],
        password = config["password"],
        database = config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )
    print('Connection done!')
except Exception as ex:
    print('Connection refused...')
    print(ex)

try:
   create_table()
except NameError:
    print('[INFO] Создаем базу данных')
    connection = pymysql.connect(
        host = config["host"],
        port = config["port"],
        user = config["user"],
        password = config["password"],
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = connection.cursor()
    connection = create_db = f'CREATE DATABASE IF NOT EXISTS {config["database"]};'
    cursor.execute(create_db)
    print('Connection done!')
    create_table()