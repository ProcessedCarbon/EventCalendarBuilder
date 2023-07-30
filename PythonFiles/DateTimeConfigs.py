import datetime
from dateutil.parser import parse

class DTConfigs:
    def __init__(self):
        self.today = datetime.date.today()
        self._months = [
            "january",
            "feburary",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]

        self._years = {str(x) for x in range(2000, self.today.year)}

    def isMonth(self, month):
        return (str(month).lower() in self._months)

    def isYear(self, year):
        return (year in self._years)
    
    def FormatToDateTime(self, date_string, format):

        dt = parse(date_string)
        return dt.strftime(format) 
    
    def isDateTime(self, datetime_, fuzzy):
        try:
            parse(datetime_, fuzzy=fuzzy)
            return True
        except ValueError:
            return False