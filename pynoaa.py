from json import load
from components.scraper import Scraper

class DatasetsNOAA:
    def __init__(self):
        with open("noaa_datasets.json") as f:
            self.datasets = load(f)

    def Get(self, dataset):
        s = Scraper()
        resp = s.CheckAvailableFiles(self.datasets[dataset])
        print(resp)

    def List(self):
        return tuple(self.datasets.keys())
