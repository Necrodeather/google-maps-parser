from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#from selenium.common.exceptions import StaleElementReferenceException
from time import sleep


options = Options()
options.headless = True


class get_info():
    def __init__(self):
        self.driver = webdriver.Firefox(options=options)

    def get_start(self):
        with open("url.txt") as urls:
            self.urls = urls.read().splitlines()

        for url in self.urls:
            self.driver.get(url)
            name = self.driver.find_element(By.CLASS_NAME,('x3AX1-LfntMc-header-title'))
            category = self.driver.find_element(By.CLASS_NAME,('h0ySl-wcwwM-E70qVe'))
            rating = self.driver.find_element(By.CLASS_NAME,('aMPvhf-fI6EEc-KVuj8d'))
            reviews = self.driver.find_element(By.CLASS_NAME,('Yr7JMd-pane-hSRGPd'))
            #adresses/phone
            #email
            #plus code
            print(f'{name.text}, {category.text}, {rating.text}, {reviews.text}\n')
