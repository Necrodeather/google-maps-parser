from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, \
    ElementNotInteractableException

from .selenium_start import Selenium
from .selenium_parser import Parser


class GoogleMaps:
    def __init__(self, request: dict):
        self.urls: set = set()
        self.driver: WebDriver = Selenium.get_start(request)

    def get_search(self) -> None:
        try:
            self.urls = set([card.get_attribute('href') for card in self.__find_cards()])
        except (IndexError, NoSuchElementException, InvalidSessionIdException, ElementNotInteractableException):
            self.get_search()

        try:
            # endpoint in cards
            self.driver.find_element(By.CLASS_NAME, ('HlvSq'))
            self.urls = set([card.get_attribute('href') for card in self.__find_cards()])
            self.driver.close()
            return Parser(self.urls).started_parse()
        except NoSuchElementException:
            self.get_search()

    def __find_cards(self) -> list:
        cards_search: list = self.driver.find_elements(By.CSS_SELECTOR, ('a.hfpxzc'))
        cards_search[-1].send_keys(Keys.PAGE_DOWN)
        return cards_search
