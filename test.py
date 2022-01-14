import csv

strana = 'США'


with open('full_list_countrys/city.csv') as full_city:
    city = csv.reader(full_city, delimiter = ";")
    list_city = [x for x in city]

with open('full_list_countrys/country.csv') as full_country:
    country = csv.reader(full_country, delimiter = ";")
    list_country = [x for x in country]
        
for f_country in list_country:
    if f_country[2] == strana:
        gorod = f_country[0]
        for f_city in list_city:
            if f_city[1] == gorod:
                print(f_city[3])
            else:
                continue
    else:
        continue