from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from fake_useragent import UserAgent
import multiprocessing
from database.database import database
from time import sleep
import random

i = None

options = Options()
options.headless = True
useragent = UserAgent()
options.set_preference("general.useragent.override", useragent.random)


with open("proxy.txt") as proxy:
    proxy_list = proxy.read().splitlines()


class get_info():
    def get_start(self):
        self.database = database()
        with open("url.txt") as urls:
            self.urls = urls.read().splitlines()
        f_urls = set(self.urls)
        print('#'*20)
        for url in f_urls:
            self.multi_search(url)
        # multiprocessing.Pool(multiprocessing.cpu_count()).map(self.multi_search, f_urls)
        # multiprocessing.Pool(multiprocessing.cpu_count()).close()
        # multiprocessing.Pool(multiprocessing.cpu_count()).join()
        #multiprocessing.cpu_count()


    def multi_search(self, url):
        i = random.randint(0, int(len(proxy_list))-1)
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities["proxy"] = {
            "httpProxy": proxy_list[i],
            "sslProxy": proxy_list[i],
            "proxyType": "MANUAL",
        }
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(url)
        try:
            name = self.driver.find_element(
                By.XPATH, ('//div[@class="x3AX1-LfntMc-header-title-ij8cu"]/div/h1/span'))
            f_name = name.text
        except StaleElementReferenceException:
            name = self.driver.find_element(
                By.XPATH, ('//div[@class="x3AX1-LfntMc-header-title-ij8cu"]/div/h1/span'))
            f_name = name.text
        try:
            category = self.driver.find_element(
                By.XPATH, ('//button[@jsaction="pane.rating.category"]'))
            f_category = category.text
        except NoSuchElementException:
            f_category = 'Null'
        try:
            rating = self.driver.find_element(
                By.CLASS_NAME, ('aMPvhf-fI6EEc-KVuj8d'))
            f_rating = rating.text
        except NoSuchElementException:
            f_rating = 'Null'
        try:
            reviews = self.driver.find_element(
                By.XPATH, ('//button[@jsaction="pane.rating.moreReviews"]'))
            f_reviews = reviews.text
        except NoSuchElementException:
            f_reviews = 'Null'
        btn_info = self.driver.find_elements(
            By.XPATH, ("//button[@class='CsEnBe']"))
        info_attr = [x.get_attribute('aria-label') for x in btn_info]
        try:
            services = self.driver.find_elements(
                By.CLASS_NAME, ('uxOu9-sTGRBb-p83tee'))
            services_attr = [x.get_attribute('aria-label') for x in services]
            f_services = []
        except NoSuchElementException:
            f_services = 'Null'

        for value in services_attr:
            if value[:2] == 'No':
                continue
            else:
                f_services.append(value)
        try:
            f_time = []
            btn_time = self.driver.find_element(
                By.CLASS_NAME, ('n2H0ue-RWgCYc'))
            btn_time.click()
            weakly = self.driver.find_elements(
                By.CLASS_NAME, ('y0skZc-oKdM2c'))
            for day in weakly:
                f_time.append(day.text.replace('\n', ' '))
        except NoSuchElementException:
            f_time = 'Null'

        address = info_attr[0].replace('Address: ', '')
        find_a_table = False
        website = None
        phone = None
        plus_code = None
        f_menu = None
        if info_attr[1][:7] == 'Address':
            info_attr.pop(1)

        if info_attr[-1] == 'Claim this business':
            info_attr.pop(-1)

        for value in info_attr:
            if value[:7] == 'Website':
                website = value[9:]
            elif value[:5] == 'Phone':
                phone = value[7:]
            elif value[:9] == 'Plus code':
                plus_code = value[11:]
            elif value[:4] == 'Menu':
                menu = self.driver.find_element(
                    By.XPATH, ('//button[@aria-label="Menu"]/div[1]/div[2]/div[3]'))
                f_menu = menu.text
            elif value == 'Find a table':
                find_a_table = True
        self.database.insert_fisrt_info(f_name,f_category,f_reviews,f_rating,f_services,address,f_time,find_a_table,f_menu,website,phone,plus_code)
        try:
            self.get_reviews()
        except NoSuchElementException:
            print(f"[INFO] Отзывы на {f_name} не обнаружены!")
            print('#'*20)
        self.driver.back()
        try:
            self.get_photo(f_name)
        except NoSuchElementException:
            print(f"[INFO] Фотографии на {f_name} не обнаружены!")
            print('#'*20)
        self.driver.close()

    def get_reviews(self):
        self.reviews = {}
        btn_more_reviews = self.driver.find_elements(By.CLASS_NAME, ('M77dve'))
        for click_more_reviews in btn_more_reviews:
            if click_more_reviews.text[:12] == 'More reviews':
                click_more_reviews.click()
                break
        sleep(10)
        try:
            self.circle_reviews()
        except NoSuchElementException:
            return False

    def circle_reviews(self):
        reviews_cards = self.driver.find_elements(By.CLASS_NAME, ('ODSEW-ShBeI'))
        for review in reviews_cards:  
            author_name = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-title'))
            avatar_author = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-t1uDwd-HiaYvf')).get_attribute('src')
            rating_from_author = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-H1e3jb')).get_attribute('aria-label')
            try:
                btn_all_img = review.find_element(By.CLASS_NAME, ('gXqMYb-hSRGPd'))
                btn_all_img.click()
            except NoSuchElementException:
                pass
            try:
                full_text = review.find_element(By.CLASS_NAME, ('ODSEW-ShBeI-text'))
            except NoSuchElementException:
                full_text = 'Null'
            self.reviews['avatar_author'] = avatar_author
            self.reviews['author_name'] = author_name.text
            self.reviews['rating_from_author'] = rating_from_author
            self.reviews['full_text'] = full_text.text.replace('\n', '')
            print(f'{self.reviews}\n')
        sleep(3)



    def get_photo(self, name):
        f_img = []
        
        sleep(10)
        clicked_img = self.driver.find_elements(
            By.CLASS_NAME, ('mWq4Rd-eEDwDf'))
        img = self.driver.find_elements(
            By.CLASS_NAME, ('mWq4Rd-HiaYvf-MNynB-gevUs'))
        for click_img in clicked_img:
            click_img.click()
            if len(img) == 11:
                break
            else:
                img = self.driver.find_elements(
                    By.CLASS_NAME, ('mWq4Rd-HiaYvf-MNynB-gevUs'))
        img_attr = [x.get_attribute('style') for x in img]
        for url_img in img_attr[:10]:
            r_url_img = url_img.replace('background-image: url("', '')
            f_img.append(r_url_img.replace('");', ''))
        print(f'[INFO] Фотографии из {name} загружены')
        print('#'*20)