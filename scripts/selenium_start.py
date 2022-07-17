from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
from fake_useragent import UserAgent


class Selenium:
    options = Options()
    # options.headless = True
    useragent = UserAgent()
    options.set_preference("general.useragent.override", useragent.random)

    @classmethod
    def get_start(cls, request: dict) -> WebDriver:
        driver: WebDriver = WebDriver(options=cls.options)
        driver.get("https://www.google.com/maps?hl=en")
        try:
            search = driver.find_element(By.ID, ('searchboxinput'))
        except NoSuchElementException:
            cls.__output_search()
        search.send_keys(f'{request["country"]}, {request["city"]}, {request["search"]}')
        search.send_keys(Keys.ENTER)
        return driver

    @staticmethod
    def __output_search():
        pass
        # i = random.randint(0, int(len(proxy_list))-1)
        # firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        # firefox_capabilities["proxy"] = {
        #     "httpProxy": proxy_list[i],
        #     "sslProxy": proxy_list[i],
        #     "proxyType": "MANUAL",
        # }

    @classmethod
    def opened_info(cls, url: str) -> WebDriver:
        #try:
        driver: WebDriver = WebDriver(options=cls.options)
        driver.get(url)

        return driver
        # except InvalidSessionIdException:
        #     cls.opened_info(url)
