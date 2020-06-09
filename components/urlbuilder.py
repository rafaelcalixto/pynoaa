from requests import get
from datetime import datetime as dt
from lxml import html

class Builder:
    def __init__(self):
        self.url_root = "https://nomads.ncep.noaa.gov/"
        self.url_filetype = "cgi-bin/"

    def CheckParameters(self, dsinfos):
        if not dsinfos["date"]:
            dsinfos["date"] = dt.today().strftime("%Y%m%d")

        if not str(dsinfos["date"]).isnumeric():
            raise("Please, inform a valid date using the format yyyymmdd")

        if not dsinfos["quarter"]:
            m = 6
            if dsinfos["name"] in ["GFS Ensemble Precip Bias-Corrected"
            , "NAEFS high resolution Bias-Corrected", "NAEFS NDGD resolution Bias-Corrected"
            , "FNMOC Ensemble and Bias Corrected", "CMC Ensemble"]:
                m = m * 2
            q = int(int(dt.today().strftime("%H")) / m) * m
            if dsinfos["coords"]["class"] == "sref":
                q += 3
            dsinfos["quarter"] = f"{q:02d}"
        elif int(dsinfos["quarter"]) not in (0, 3, 6, 9, 12, 15, 18, 21):
            raise("Please, inform a valid quarter between the options: 00, 03, 06, 09, 12, 15, 18, 21")
        elif isinstance(dsinfos["quarter"], int):
            dsinfos["quarter"]  = f"{dsinfos['quarter']:02d}"

    def FillURL2ConfPage(self, dsinfos):
        url = "{}{}filter_{}.pl?dir=%2F{}.{}".format(
                                              self.url_root
                                            , self.url_filetype
                                            , dsinfos["coords"]['id']
                                            , dsinfos["coords"]['class']
                                            , dsinfos["date"]
                                            )

        if dsinfos["coords"]["quarter"]:
            url += f"%2F{dsinfos['quarter']}"
        if "subdir" in dsinfos["coords"].keys():
            url += f"%2F{dsinfos['coords']['subdir']}"

        return url

    def CheckAvailableFiles(self, dsinfos):
        self.CheckParameters(dsinfos)

        url = self.FillURL2ConfPage(dsinfos)

        tree = html.fromstring(get(url).text)
        files = tree.xpath("//option/@value")

        return files

    def CheckAvailableOptions(self, dsinfos):
        self.CheckParameters(dsinfos)

        url = self.FillURL2ConfPage(dsinfos)

        tree = html.fromstring(get(url).text)
        oplist = tree.xpath("//body/form/p/input/@name")

        options = {
            "lev" : ["all_lev"],
            "var" : ["all_var"]
        }

        for each in oplist:
            try:
                options[each[:3]].append(each)
            except:
                pass

        return options

    def BuildURL(self, dsinfos):
        self.CheckParameters(dsinfos)

        url = self.FillURL2ConfPage(dsinfos)
        url += f"&file={dsinfos['file']}"
        levandvar = ""

        if not len(dsinfos["levels"]):
            levandvar += f"&all_lev=on"
        else:
            for l in dsinfos["levels"]:
                levandvar += f"&lev_{l}=on"

        if not len(dsinfos["variables"]):
            levandvar += f"&all_var=on"
        else:
            for v in dsinfos["variables"]:
                levandvar += f"&var_{v}=on"

        ll = dsinfos["subregion"][0]
        rl = dsinfos['subregion'][1]
        tl = dsinfos['subregion'][2]
        bl = dsinfos['subregion'][3]
        coords = f"&leftlon={ll}&rightlon={rl}&toplat={tl}&bottomlat={bl}"

        return url + levandvar + coords
