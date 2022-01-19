import pymysql
import config

def create_main(cursor):
    create_table = """
    CREATE TABLE IF NOT EXISTS main
    (
        id SERIAL NOT NULL AUTO_INCREMENT, 
        S_Name text,
        Category text,
        Reviews text,
        Rating text,
        Services text,
        Address text,
        Work_time text,
        Find_a_table text,
        Menu text ,
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
	    S_Name text REFERENCES main(S_Name),
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
	    S_Name text REFERENCES main (S_Name),
	    Avatar_Author text,
	    Author_name text,	
	    Rating text,	
	    Full_Text text,
        primary key(id)
    )"""
    cursor.execute(create_table)
    print("[INFO]Таблица 'reviews' Подключена!")


def connection_db():
    try:
        connection = pymysql.connect(
            host = config.host,
            port = config.port,
            user = config.user,
            password = config.password,
            database = config.database,
            cursorclass=pymysql.cursors.DictCursor
        )
        print('Connection done!')
        cursor = connection.cursor()
        create_main(cursor)
        create_photo(cursor)
        create_reviews(cursor)
    except Exception as ex:
        print(ex)

    return connection


cursor = connection_db()

def insert_fisrt_info(name, category, reviews, rating, services, 
    address,work_time, find_a_table, menu, website, phone, plus_code):
    insert_sql = name, category, reviews, rating, services, address, work_time, find_a_table, menu, website, phone, plus_code
    cursor.cursor().execute('INSERT INTO main (S_Name, Category, Rating, Reviews, Services, Address, Work_time, Find_a_table, Menu, Website, Phone, Plus_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', insert_sql) 
    cursor.commit()
    print(f'[INFO] Добавлена информация о {name}')
    print('#'*20)
    return True

def insert_second_reviews(name, review):
    insert_sql = name, str(review[0]), str(review[1]), str(review[2]), str(review[3])
    cursor.cursor().execute('INSERT INTO reviews (S_Name, Avatar_Author, Author_name, Rating, Full_Text) VALUES (%s,%s,%s,%s,%s)', insert_sql) 
    cursor.commit()
    return True

def insert_three_photo(name, photo):
    insert_sql = name, photo
    cursor.cursor().execute('INSERT INTO photo (S_Name, Photo) VALUES (%s,%s)', insert_sql) 
    cursor.commit()
    return True