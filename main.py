from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
driver = webdriver.Chrome()

driver.get("https://www.google.com/maps?hl=en")

def test(text):
    with open("test.txt", "a") as t:
        t.writelines(f'{text}\n')

get_country = "USA"#input()
get_region = None #input()
get_town = "New York" #input()
get_search = "Park"#input()

get = f'{get_country},{get_region},{get_town},{get_search}'

search = driver.find_element(By.ID, ('searchboxinput'))
driver.implicitly_wait(5)
search.send_keys(get)
search.send_keys(Keys.ENTER)
sleep(5)
post = driver.find_elements(By.CLASS_NAME,("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"))
ps = [p.get_attribute('href') for p in post]

post[-1].send_keys(Keys.PAGE_DOWN)
post.clear()
post = driver.find_elements(By.CLASS_NAME,("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"))
ps = [p.get_attribute('href') for p in post]

post[-1].send_keys(Keys.PAGE_DOWN)
post.clear()
post = driver.find_elements(By.CLASS_NAME,("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"))
ps = [p.get_attribute('href') for p in post]

p = set(ps)
url = [test(pq) for pq in p]

next = driver.find_element(By.ID,("ppdPk-Ej1Yeb-LgbsSe-tJiF1e"))
next.click()

#print(url)
print(len(url))
sleep(15)
