import pymysql
import json

with open("config.json", "r") as json_config:
    config = json.load(json_config)

def create_main(cursor):
    create_table = """
    CREATE TABLE IF NOT EXISTS main
    (
        id SERIAL NOT NULL AUTO_INCREMENT, 
        S_Name varchar(30), 
        Category varchar(30),
        Reviews varchar(15),
        Rating varchar(3),
        Services text,
        Address text,
        Location text,
        Work_time text,
        Find_a_table boolean,
        Menu text,
        Website text,
        Phone text,	
        Plus_code text,
        primary key(id)
    )"""
    cursor.execute(create_table)
    print("[INFO]Таблица 'main' Подключена!")

def create_photo(cursor):
    create_table = """
    CREATE TABLE IF NOT EXISTS photo
    (
	    id SERIAL NOT NULL AUTO_INCREMENT,
	    Fk_Photo int REFERENCES main(Id),
	    S_Name varchar(30) REFERENCES main(S_Name),
	    Photo text,
	    primary key(id)
    )"""
    cursor.execute(create_table)
    print("[INFO]Таблица 'photo' Подключена!")


def create_reviews(cursor):
    create_table = """
    CREATE TABLE IF NOT EXISTS reviews
    (
	    id SERIAL NOT NULL AUTO_INCREMENT,	
	    fk_Reviews INT REFERENCES main (Id), 	
	    S_Name varchar(30) REFERENCES main (S_Name),
	    Avatar_Author text,
	    Author_name varchar(30),	
	    Rating varchar(3),	
	    Full_Text text,
        primary key(id)
    )"""
    cursor.execute(create_table)
    print("[INFO]Таблица 'reviews' Подключена!")





""" name, category, reviews, rating, services, 
    address,work_time, find_a_table, menu, website, phone, plus_code, 
    photo, avatar_author, author_name, rating_from_author, full_texts):"""
class database():
    def __init__(self):
        pass
    
    def create_database(self):
            print('[INFO] Создаем базу данных')
            connection = pymysql.connect(
                host = config["host"],
                port = config["port"],
                user = config["user"],
                password = config["password"],
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = connection.cursor()
            connection = create_db = f'CREATE DATABASE {config["database"]};'
            cursor.execute(create_db)
            self.create_connection()

    def create_connection(self):
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
            self.cursor = connection.cursor()
            create_main(self.cursor)
            create_photo(self.cursor)
            create_reviews(self.cursor)
        except pymysql.OperationalError:
            print('[WARNING]База данных не найдена!')
            self.create_database()

data = database()
data.create_connection()