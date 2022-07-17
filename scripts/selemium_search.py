from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, \
    ElementNotInteractableException

from .selenium_start import Selenium


class GoogleMaps:
    def __init__(self, request: dict):
        self.urls: set = set()
        self.request: dict = request

    async def get_search(self) -> set:
        driver: WebDriver = await Selenium.get_start(self.request)
        while True:
            try:
                self.urls = set([card.get_attribute('href') for card in await self.__find_cards(driver)])
            except (IndexError, NoSuchElementException, InvalidSessionIdException, ElementNotInteractableException):
                continue
            try:
                # endpoint in cards
                driver.find_element(By.CSS_SELECTOR, ('span.HlvSq'))
                self.urls = set([card.get_attribute('href') for card in await self.__find_cards(driver)])
                await Selenium.close_driver(driver)
                return self.urls
            except NoSuchElementException:
                continue

    @staticmethod
    async def __find_cards(driver) -> list:
        cards_search: list = driver.find_elements(By.CSS_SELECTOR, ('a.hfpxzc'))
        cards_search[-1].send_keys(Keys.PAGE_DOWN)
        return cards_search
