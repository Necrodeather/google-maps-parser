from selemium_search import google_maps
#from selenium_parser import get_info
def main():
    selenium_search = google_maps("https://www.google.com/maps?hl=en")
    selenium_search.search()

if __name__ == "__main__":
    main()
