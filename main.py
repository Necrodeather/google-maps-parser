import csv
from scripts.selemium_search import google_maps
from selenium.common.exceptions import InvalidSessionIdException



with open('full_list_countrys/city.csv', encoding = 'utf-8') as full_city:
    city = csv.reader(full_city, delimiter = ";")
    list_city = [x for x in city]


with open('full_list_countrys/country.csv', encoding = 'utf-8') as full_country:
    country = csv.reader(full_country, delimiter = ";")
    list_country = [x for x in country]


def url_txt():
    with open("url.txt", "w+") as t:
        t.seek(0)
        t.write('')
    t.close()


def main():
    print('#'*20)
    url_txt()
    print('#'*20)
    country = str(input('country: '))
    search = str(input('search: '))
    
    for f_country in list_country:
            if f_country[2] == country.lower().capitalize():
                id_country = f_country[0]
                for f_city in list_city:
                    if f_city[1] == id_country:
                        print('#'*20)
                        print(f_city[3])
                        town = f_city[3]
                        selenium_search = google_maps("https://www.google.com/maps?hl=en", country, town, search.lower().capitalize())
                        url_txt()
                        try:
                            selenium_search.output_search()
                            selenium_search.result_search()
                        except InvalidSessionIdException:
                            continue
                    else:
                        continue
            else:
                continue
    
    
    print('ПОИСК ЗАВЕРШЕН')


if __name__ == "__main__":
    main()
