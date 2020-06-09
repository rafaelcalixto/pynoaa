from json import load
from components.urlbuilder import Builder

class DatasetsNOAA:
    def __init__(self):
        with open("noaa_datasets.json") as f:
            self.datasets = load(f)
            self.s = Builder()

    def GetAvailableFiles(self, dsname, date = False, quarter = False):
        ds2check = {
            "name" : dsname,
            "date" : date,
            "quarter" : quarter,
            "coords" : self.datasets[dsname]
        }

        return self.s.CheckAvailableFiles(ds2check)

    def GetAvailableOptions(self, dsname, date = False, quarter = False):
        ds2check = {
            "name" : dsname,
            "date" : date,
            "quarter" : quarter,
            "coords" : self.datasets[dsname]
        }

        return self.s.CheckAvailableOptions(ds2check)

    def ListDatasets(self):
        return tuple(self.datasets.keys())

    def GetDataset(self, dsname, file, levels = [], variables = []
                       , subregion = [0, 360, 90, -90], date = False, quarter = False):
        ds2check = {
            "name" : dsname,
            "file" : file,
            "levels" : levels,
            "variables" : variables,
            "subregion" : subregion,
            "date" : date,
            "quarter" : quarter,
            "coords" : self.datasets[dsname]
        }

        url = self.s.GetDataset(ds2check)
