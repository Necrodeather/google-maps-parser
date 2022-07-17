from scripts import GoogleMaps, Parser
# from database import create_bd


def main():
    # create_bd()
    country = "Russia"  # str(input('country: '))
    search = "Restaurant"  # str(input('search: '))

    request = {
        'country': country,
        'city': "Krasnodar",
        'search': search.lower().capitalize()
    }
    #selenium_search: GoogleMaps = GoogleMaps(request)
    #selenium_search.get_search()
    Parser(['https://www.google.com/maps/place/Cafe+%C2%ABPorto+Carras%C2%BB/@45.0222863,38.9678019,17z/data=!4m5!3m4!1s0x40f04fb1249c57bd:0x5ae54babc55d2b8!8m2!3d45.0222863!4d38.9678019?authuser=0&hl=en']).started_parse()
    print('ПОИСК ЗАВЕРШЕН')


if __name__ == "__main__":
    main()
