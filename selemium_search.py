from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import selenium_parser


urls = []

options = Options()
options.headless = True


def get_input():
    get_country = str(input('country: '))
    get_region = str(input('region: '))
    get_town = str(input('town: '))
    get_search = str(input('search: '))
    get_request = f'{get_country}, {get_region}, {get_town}, {get_search}' 
    return get_request


def url_txt(text):
    with open("url.txt", "a") as t:
        t.writelines(f'{text}\n')
    t.close()

class google_maps:
    def __init__(self, url):
        self.driver = webdriver.Firefox(options=options)
        self.url = url
        self.parser = selenium_parser.get_info()


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
        try:
            cards_search = self.driver.find_elements(By.CLASS_NAME,("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"))
            cards_search[-1].send_keys(Keys.PAGE_DOWN)
        except IndexError:
            self.driver.close()
            self.parser.get_start()
        except StaleElementReferenceException:
            self.result_search()
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
                self.parser.get_start()
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