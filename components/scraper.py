from requests import get
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs


class Scraper:
    def __init__(self):
        self.url_root = "https://nomads.ncep.noaa.gov/"
        self.url_filetype = "cgi-bin/"

    def CheckAvailableFiles(self, dataset, date = False, quarter = False):
        if not date:
            date = dt.today().strftime("%Y%m%d")

        if not str(date).isnumeric():
            raise("Please, inform a valid date using the format yyyymmdd")

        if not quarter:
            quarter = int((int(dt.today().strftime("%H")) / 6) * 6)
            date = f"{quarter:02d}"
        elif int(quarter) not in (0, 6, 12, 18):
            raise("Please, inform a valid quarter between the options: 00, 06, 12, 18")
        elif isinstance(date, int):
            date  = f"{date:02d}"

        file = dataset["subdir"] + "." + date

        url = f"{self.url_root}{self.url_filetype}filter_{dataset["id"]}.pl?dir=%2F{dataset["subdir"]}.date%2F{quarter}"

        return get(url).text

    def CheckAllAvailableFiles(self, dataset):
        pass
