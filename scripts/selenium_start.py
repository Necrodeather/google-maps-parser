from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent


class Selenium:
    options = Options()
    options.headless = True
    useragent = UserAgent()
    options.set_preference("general.useragent.override", useragent.random)

    @classmethod
    async def get_start(cls, request: dict) -> WebDriver:
        driver: WebDriver = WebDriver(options=cls.options)
        driver.get("https://www.google.com/maps?hl=en")
        try:
            search = driver.find_element(By.ID, ('searchboxinput'))
        except NoSuchElementException:
            await cls.__output_search()
            await cls.get_start(request)
        search.send_keys(f'{request["country"]}, {request["city"]}, {request["search"]}')
        search.send_keys(Keys.ENTER)
        return driver

    @classmethod
    async def close_driver(cls, driver: WebDriver) -> None:
        return driver.close()

    @staticmethod
    async def __output_search() -> None:
        return None
        # TODO: Дальнейшее добавление функционала на прокси
        # i = random.randint(0, int(len(proxy_list))-1)
        # firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        # firefox_capabilities["proxy"] = {
        #     "httpProxy": proxy_list[i],
        #     "sslProxy": proxy_list[i],
        #     "proxyType": "MANUAL",
        # }

    @classmethod
    async def opened_info(cls, url: str) -> WebDriver:
        driver: WebDriver = WebDriver(options=cls.options)
        driver.get(url)

        return driver
