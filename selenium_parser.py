from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import multiprocessing
from time import sleep


options = Options()
options.headless = True



class get_info():
    def get_start(self):
        with open("url.txt") as urls:
            self.urls = urls.read().splitlines()
        #f_urls = self.urls[:28]  # test
        f_urls = set(self.urls)
        print('#'*20)
        try:
            multiprocessing.Pool(multiprocessing.cpu_count()).map(self.multi_search, f_urls)
            multiprocessing.Pool(multiprocessing.cpu_count()).close()
            multiprocessing.Pool(multiprocessing.cpu_count()).join()
        except NameError:
            return True
        


    def multi_search(self, url):

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

        print(f'Name: {f_name}\nCategory: {f_category}\nReviews: {f_reviews}\nRating: {f_rating}\nServices: {f_services}\nAddress: {address}\nWork time: {f_time}\nFind a table: {find_a_table}\nMenu: {f_menu}\nWebsite: {website}\nPhone: {phone}\nPlus code: {plus_code}')
        print('#'*20)
        # self.get_reviews()
        try:
            self.get_photo(f_name)
        except NoSuchElementException:
            print(f"[INFO] Фотографии на {f_name} не обнаружены!")
        self.driver.close()
        p.close()

    def get_reviews(self):
        self.full_reviews = {}
        btn_more_reviews = self.driver.find_elements(By.CLASS_NAME, ('M77dve'))
        for click_more_reviews in btn_more_reviews:
            if click_more_reviews.text[:12] == 'More reviews':
                click_more_reviews.click()
                break
        sleep(10)
        self.author_names = self.driver.find_elements(
            By.CLASS_NAME, ('ODSEW-ShBeI-title'))
        avatar_authors = self.driver.find_elements(
            By.CLASS_NAME, ('ODSEW-ShBeI-t1uDwd-HiaYvf'))
        self.avatar_authors_attr = [
            x.get_attribute('src') for x in avatar_authors]
        rating_from_authors = self.driver.find_elements(
            By.CLASS_NAME, ('ODSEW-ShBeI-H1e3jb'))
        self.rating_from_authors_attr = [x.get_attribute(
            'aria-label') for x in rating_from_authors]
        self.full_texts = self.driver.find_elements(
            By.CLASS_NAME, ('ODSEW-ShBeI-text'))
        self.circle_reviews()

    def circle_reviews(self):
        for author_name in self.author_names:
            self.full_reviews['name'] = author_name.text
            for avatar_author in self.avatar_authors_attr:
                self.full_reviews['avatar'] = avatar_author
                for rating_from_author in self.rating_from_authors_attr:
                    self.full_reviews['rating'] = rating_from_author
                    for full_text in self.full_texts:
                        self.full_reviews['text'] = full_text.text

                        print(self.full_reviews)
                        self.circle_reviews()

    def get_photo(self, name):
        f_img = []
        btn_all_img = self.driver.find_element(
            By.CLASS_NAME, ('a4izxd-tUdTXb-xJzy8c-haAclf'))
        btn_all_img.click()
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