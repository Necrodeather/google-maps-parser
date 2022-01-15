from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep


options = Options()
options.headless = True


class get_info():
    def get_start(self):
        self.driver = webdriver.Firefox(options=options)
        with open("url.txt") as urls:
            self.urls = urls.read().splitlines()
        #f_urls = self.urls[:5]
        f_urls = set(self.urls)
        print('#'*20)
        for url in f_urls:
            self.driver.get(url)
            name = self.driver.find_element(By.XPATH,('//div[@class="x3AX1-LfntMc-header-title-ij8cu"]/div/h1/span'))
            f_name = name.text
            try:
                category = self.driver.find_element(By.XPATH,('//button[@jsaction="pane.rating.category"]'))
                f_category = category.text 
            except NoSuchElementException:
                f_category = 'Null'
            try:
                rating = self.driver.find_element(By.CLASS_NAME,('aMPvhf-fI6EEc-KVuj8d'))
                f_rating = rating.text
            except NoSuchElementException:
                f_rating = 'Null'
            try:
                reviews = self.driver.find_element(By.XPATH,('//button[@jsaction="pane.rating.moreReviews"]'))
                f_reviews = reviews.text
            except NoSuchElementException:
                f_reviews = 'Null'
            btn_info = self.driver.find_elements(By.XPATH,("//button[@class='CsEnBe']"))
            info_attr = [x.get_attribute('aria-label') for x in btn_info]

            address = info_attr[0]
            website = None
            phone = None
            plus_code = None
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

            print(f'Name: {f_name}\nCategory: {f_category}\nReviews: {f_reviews}\nRating: {f_rating}\nAddress: {address}\nWebsite: {website}\nPhone: {phone}\nPlus code: {plus_code}')
            print('#'*20)

        self.driver.close()