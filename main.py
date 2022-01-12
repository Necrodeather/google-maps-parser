import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent

ua = UserAgent()

urls = []


def get_input():
    get_country = "USA" #str(input('country: '))
    #get_region = None #str(input('region: '))
    get_town = "New York"#str(input('town: '))
    get_search = "Hotel"#str(input('search: '))
    get_request = f'{get_country}, {get_search}' #, {get_town}, ' #{get_region}, 
    return get_request


def url_txt(text):
    with open("url.txt", "a") as t:
        t.writelines(f'{text}\n')
    t.close()

class google_maps:
    def __init__(self, url):
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox()
        self.url = url
        self.parser = parser()


    def search(self):
        self.driver.get(self.url)
        self.get_search()
        sleep(10)
        self.result_search()
    

    def get_search(self):
        search = self.driver.find_element(By.ID, ('searchboxinput'))
        search.send_keys(get_input())
        search.send_keys(Keys.ENTER)
                

    def result_search(self):
        max_list = self.driver.find_element(By.CLASS_NAME, ('Jl2AFb'))
        next_btn = self.driver.find_element(By.ID,("ppdPk-Ej1Yeb-LgbsSe-tJiF1e"))
        disable_btn = next_btn.get_attribute('disabled')                    
        cards_search = self.driver.find_elements(By.CLASS_NAME,("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"))
        cards_search[-1].send_keys(Keys.PAGE_DOWN)
        try:
            urls_cards = [urls.append(card.get_attribute('href')) for card in cards_search]
        except StaleElementReferenceException:
            pass
        cards_search.clear()
        f_urls = set(urls)
        if len(f_urls) >= 20 or len(f_urls) >= int(max_list.text[-2:]):
            save_url = [url_txt(url_card) for url_card in f_urls]
            if disable_btn == "true": 
                self.driver.close()
                self.parser.start_parser()
            else:
                urls.clear()
                next_btn.click()
                sleep(10)
                self.result_search()
        else:
            sleep(5)
            try:
                self.result_search()
            except RecursionError:
                pass

class parser():
    def __init__(self):
        pass

    def read_urls(self):
        with open('url.txt', 'r') as list_parse:
            self.parse = list_parse.readlines()
        self.card_info()

    def card_info(self):
        for self.parsing in self.parse:
            print(self.parsing.strip('\n'))
            response = requests.get(url = self.parsing.strip('\n'), headers={'user-agent' : f'{ua.random}'})
            self.soup = BeautifulSoup(response.text, "lxml")
            self.card_name()

    def card_name(self):
        name = self.soup.find(class_="x3AX1-LfntMc-header-title") 
        print(name.text)      

        
        


def main():
    #selenium_search = google_maps("https://www.google.com/maps?hl=en")
    #selenium_search.search()
    q = parser()
    q.read_urls()
    

if __name__ == "__main__":
    main()


#sleep(15)
