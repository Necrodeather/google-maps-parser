import multiprocessing #Костыль

#Настройка соединения к БД
host = "localhost"
port = 3306
user = "root"
password = "Sqwerty1"
database = "Test"
#Настройка Многопроцессорности
#multiprocessing.cpu_count() - Использует все ядра
#Если поменять количество использования ядер, 
#то в proccess прописывать proccesses = {число} 
proccess = multiprocessing.cpu_count()

