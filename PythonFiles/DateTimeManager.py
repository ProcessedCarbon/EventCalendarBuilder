import datetime as dt
import pytz
from datetime import datetime
from dateutil.parser import parse

class Interface:
    def __init__(self):
        self.today = dt.date.today()
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

        self._period = [
            "am",
            "pm"
        ]

        self._years = {str(x) for x in range(2000, self.today.year)}

    def isMonth(self, month):
        return (str(month).lower() in self._months)

    def isYear(self, year):
        return (year in self._years)
    
    def FormatToDateTime(self, date_string, format):
        try:
            dt = parse(date_string)
            return dt.strftime(format)
        except:
            return None 
    
    def isDateTime(self, datetime_, fuzzy):
        try:
            parse(datetime_, fuzzy=fuzzy)
            return True
        except ValueError:
            return False
        
    def isAPeriod(self, period_):
        period_string = str(period_)
        return period_string.lower() in self._period
    
    def getTimeZone(self, timezone_, country_code_):

        if timezone_ is None:
            print("Missing time zone  value")
            return "Asia/Singapore"
        
        # If valid timezone just return
        if timezone_ in pytz.all_timezones:
            return timezone_

        #look up the abbreviation
        country_tzones = None
        try:
            country_tzones = pytz.country_timezones[country_code_]
        except:
            pass
        set_zones = set()
        if country_tzones is not None and len(country_tzones) > 0:
            for name in country_tzones:
                tzone = pytz.timezone(name)
                for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
                    if tzabbrev.upper() == timezone_.upper():
                        set_zones.add(name)

            if len(set_zones) > 0:
                return min(set_zones, key=len)

            # none matched, at least pick one in the right country
            return min(country_tzones, key=len)

        #invalid country, just try to match the timezone abbreviation to any time zone
        for name in pytz.all_timezones:
            tzone = pytz.timezone(name)
            for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
                if tzabbrev.upper() == timezone_.upper():
                    set_zones.add(name)
        return min(set_zones)

    def convertTime12HTo24H(self, time_12h):
        try:
            time_object = datetime.strptime(time_12h, "%I:%M:%S %p")
            return time_object.strftime("%H:%M:%S")
        except:
            return None

# For testing
def main():
    dt_config = Interface()
    # Testing for time
    # test_tz = "SST"
    # test_cc = "SG"
    # print(dt_config.getTimeZone(timezone_ = test_tz, country_code_=test_cc))

    test_12h = "7pm"
    print(dt_config.convertTime12HTo24H(test_12h))

if __name__ == "__main__":
    main()