import pymysql
import json

with open("config.json", "r") as json_config:
    config = json.load(json_config)


try:
    connection = pymysql.connect(
        host = config["host"],
        port = config["port"],
        user = config["user"],
        password = config["password"],
        database = config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )
except Exception as ex:
    print('Connection refused...')
    print(ex)