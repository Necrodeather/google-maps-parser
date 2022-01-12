from os import close
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


urls = []


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
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox()
        self.url = url
        self.parser = parser()


    def search(self):
        self.driver.get(self.url)
        self.get_search()
        sleep(5)
        self.result_search()
    

    def get_search(self):
        search = self.driver.find_element(By.ID, ('searchboxinput'))
        self.driver.implicitly_wait(5)
        search.send_keys(get_input())
        search.send_keys(Keys.ENTER)
                

    def result_search(self):
        cards_search = self.driver.find_elements(By.CLASS_NAME,("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"))
        next_btn = self.driver.find_element(By.ID,("ppdPk-Ej1Yeb-LgbsSe-tJiF1e"))
        disable_btn = next_btn.get_attribute('disabled')            
        try:
            cards_search[-1].send_keys(Keys.PAGE_DOWN)
        except IndexError:
            self.parser.start_parser()
            urls_cards = [urls.append(card.get_attribute('href')) for card in cards_search]
            f_urls = set(urls)
            save_url = [url_txt(url_card) for url_card in f_urls]
        if len(f_urls) == 20:
            #urls.clear()
            #cards_search.clear()
            if disable_btn == "true": 
                self.parser.start_parser()
            else:
                next_btn.click()
                sleep(5)
                self.result_search()
        else:
            if disable_btn == "true": 
                self.parser.start_parser()
            else:
                sleep(5)
                self.result_search()


class parser():
    def __init__(self):
        self.list_urls = open('url.txt')

    def start_parser(self):
        text = [print(l) for l in self.list_urls]
        


def main():
    selenium_search = google_maps("https://www.google.com/maps?hl=en")
    selenium_search.search()
    


if __name__ == "__main__":
    main()


sleep(15)
