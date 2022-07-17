import asyncio

from scripts import GoogleMaps, Parser
# from database import create_bd


async def main():
    # create_bd()
    country = "Russia"  # str(input('country: '))
    search = "Restaurant"  # str(input('search: '))

    request = {
        'country': country,
        'city': "Krasnodar",
        'search': search.lower().capitalize()
    }
    selenium_search: GoogleMaps = GoogleMaps(request)
    urls: set = await selenium_search.get_search()
    await Parser(urls).started_parse()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

