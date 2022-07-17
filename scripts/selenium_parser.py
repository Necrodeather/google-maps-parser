from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from .selenium_start import Selenium


class Parser:
    def __init__(self, urls: set):
        self.urls: list = list(urls)
        self.full_info: dict = {}

    def started_parse(self) -> None:
        task = [self.get_info(url) for url in self.urls]

    def get_info(self, url: str) -> None:
        driver: WebDriver = self.__get_driver(url)
        self.full_info['url']: str = url
        self.full_info['name']: str = self.__find_element(driver, 'h1.DUwDvf')
        self.full_info['category']: str = self.__find_element(driver, 'button.DkEaL')
        self.full_info['services']: list = self.__find_element(driver, 'div.E0DTEd').split('\n·\n')
        self.full_info['rating']: str = self.__find_element(driver, 'div.F7nice')
        self.full_info['reviews']: str = self.__find_element(driver, 'span.F7nice')
        self.full_info['work_time'] = self.__search_work_time(driver)
        self.get_data(driver)
        driver.close()
        print(self.full_info)

    def get_data(self, driver: WebDriver) -> None:
        self.__get_data_info(driver, "//button[@class='CsEnBe']")
        self.__get_data_info(driver, "//a[@class='CsEnBe']")
        return None

    def __get_data_info(self, driver: WebDriver, xpath: str) -> None:
        info: list = [x.get_attribute('aria-label') for x in driver.find_elements(By.XPATH, (xpath))]
        if info[-1] == 'Claim this business':
            info.pop(-1)
        for value in info:
            try:
                if value[:5] == 'Phone':
                    self.full_info['phone'] = value[7:]
                elif value[:9] == 'Plus code':
                    self.full_info['plus_code'] = value[11:]
                elif value[:4] == 'Menu':
                    search_menu: list = driver.find_elements(By.CSS_SELECTOR, ('div.gSkmPd'))
                    for menu in search_menu:
                        if menu.get_attribute('jstcache') == 156:
                            self.full_info['menu'] = menu.text
                elif value == 'Find a table':
                    self.full_info['find_a_table'] = True
                elif value[:7] == 'Website':
                    self.full_info['website'] = value[9:]
                elif value[:10] == 'Located in':
                    self.full_info['located'] = value[11:]
            except TypeError:
                continue
        return None

    @staticmethod
    def __get_driver(url: str) -> WebDriver:
        driver: WebDriver = Selenium.opened_info(url)
        return driver

    @staticmethod
    def __find_element(driver: WebDriver, selector: str) -> str:
        element = driver.find_element(By.CSS_SELECTOR, (selector))
        return element.text

    @staticmethod
    def __search_work_time(driver: WebDriver) -> list | None:
        full_span: list = driver.find_elements(By.TAG_NAME, ('span'))
        for span in full_span:
            if span.get_attribute('aria-label') == "Show open hours for the week":
                span.click()
                weakly = driver.find_elements(By.CSS_SELECTOR, ('tr.y0skZc'))
                work_time: list = [day.text.replace('\n', ' ') for day in weakly]
                return work_time
        return None

    # def get_reviews(self, name):
    #     self.reviews = {}
    #     btn_more_reviews = driver.find_elements(By.CLASS_NAME, ('M77dve'))
    #     for click_more_reviews in btn_more_reviews:
    #         if click_more_reviews.text[:12] == 'More reviews':
    #             click_more_reviews.click()
    #             break
    #     sleep(10)
    #     try:
    #         self.circle_reviews(name)
    #     except NoSuchElementException:
    #         return False
    #
    # def circle_reviews(self, name):
    #     reviews_cards = self.driver.find_elements(By.CLASS_NAME, ('ODSEW-ShBeI'))
    #     for review in reviews_cards:
    #         author_name = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-title'))
    #         avatar_author = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-t1uDwd-HiaYvf')).get_attribute('src')
    #         rating_from_author = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-H1e3jb')).get_attribute('aria-label')
    #         try:
    #             btn_all_img = review.find_element(By.CLASS_NAME, ('gXqMYb-hSRGPd'))
    #             btn_all_img.click()
    #         except NoSuchElementException:
    #             pass
    #         try:
    #             full_text = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-text'))
    #         except NoSuchElementException:
    #             full_text = 'Null'
    #         self.reviews['avatar_author'] = avatar_author
    #         self.reviews['author_name'] = author_name.text
    #         self.reviews['rating_from_author'] = rating_from_author
    #         self.reviews['full_text'] = full_text.text.replace('\n', '')
    #         reviews = self.reviews.values()
    #         self.reviews_database(name, list(reviews))
    #     back_btn = self.driver.find_element(By.CLASS_NAME, ('VfPpkd-kBDsod'))
    #     back_btn.click()
    #     sleep(10)
    #
    # def get_photo(self, name):
    #     f_img = []
    #
    #     clicked_img = self.driver.find_element(
    #         By.CLASS_NAME, ('a4izxd-tUdTXb-xJzy8c-haAclf-UDotu'))
    #     clicked_img.click()
    #     sleep(10)
    #     img = self.driver.find_elements(
    #         By.CLASS_NAME, ('mWq4Rd-HiaYvf-MNynB-gevUs'))
    #     img_attr = [x.get_attribute('style') for x in img]
    #     for url_img in img_attr[:10]:
    #         r_url_img = url_img.replace('background-image: url("', '')
    #         if r_url_img != '//:0");' and img != '");':
    #             f_img.append(r_url_img.replace('");', ''))
    #         else:
    #             continue
    #     for img in f_img:
    #         self.photo_database(name, img)
    #     print(f'Добавлена фотография о {name}')
    #     print('#' * 20)


