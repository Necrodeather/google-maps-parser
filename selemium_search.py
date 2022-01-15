from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from time import sleep
import selenium_parser


urls = []
site_list = []
options = Options()
#options.headless = True


def url_txt(text):
    with open("url.txt", "a") as t:
        t.writelines(f'{text}\n')
    t.close()

class google_maps:
    def __init__(self, url, get_country, get_town, get_search):
        self.url = url
        self.parser = selenium_parser.get_info()
        self.get_country = get_country
        self.get_town = get_town
        self.get_search = get_search


    def output_search(self):
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.url)
        search = self.driver.find_element(By.ID, ('searchboxinput'))
        search.send_keys(f'{self.get_country}, {self.get_town}, {self.get_search}')
        search.send_keys(Keys.ENTER)
                

    def result_search(self):
        try:
            try:
                name = self.driver.find_element(By.CLASS_NAME,('x3AX1-LfntMc-header-title'))
                url_txt(self.driver.current_url)
                self.driver.close()
                self.parser.get_start()
            except NoSuchElementException:
                pass
            cards_search = self.driver.find_elements(By.CLASS_NAME,("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"))
            max_list = self.driver.find_element(By.CLASS_NAME, ('Jl2AFb'))
            next_btn = self.driver.find_element(By.ID,("ppdPk-Ej1Yeb-LgbsSe-tJiF1e"))
            disable_btn = next_btn.get_attribute('disabled')                    
        except NoSuchElementException:
            self.driver.implicitly_wait(5)
            self.result_search()
        
        try:    
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
        try:
            s = (int(max_list.text[-3:])+1) - int(max_list.text[-9:-6])
        except ValueError:
            try:
                s = (int(max_list.text[-3:])+1) - int(max_list.text[-8:-5])
            except ValueError:
                s = (int(max_list.text[-3:])+1) - int(max_list.text[-7:-5])
        if len(f_urls) >= s:
            save_url = [url_txt(url_card) for url_card in f_urls]
            while disable_btn == "true": 
                self.driver.close()
                self.parser.get_start()    
                break
            else:
                urls.clear()
                try:
                    next_btn.click()
                except ElementClickInterceptedException:
                    pass
                self.result_search()
        else:
            self.result_search()
