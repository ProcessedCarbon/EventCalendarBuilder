import datetime as dt
import pytz
from datetime import datetime, timedelta
from dateutil.parser import parse

class DateTimeManager:
    _months = [
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
    
    _period = ["am", "pm"]
    
    _years = {str(x) for x in range(2000, dt.date.today().year)}

    def isMonth(self, month: str):
        return (str(month).lower() in self._months)

    def isYear(self, year):
        return (year in self._years)
    
    def FormatToDateTime(self, date_string: str, format: str):
        """
        Try and convert date string into a datetime obj in the given format. 
        
        :param date_string (str): Date in string format
        :param format (str): format to be converted to

        return: the formatted datetime obj
        """

        try:
            dt = parse(date_string)
            return dt.strftime(format)
        except Exception as e:
            print(f'[{str(self.__class__.__name__).upper}](FormatToDateTime()): {e}')
            return None 
    
    def isDateTime(self, datetime_: str, fuzzy: bool):
        try:
            parse(datetime_, fuzzy=fuzzy)
            return True
        except Exception as e:
            print(f'[{str(self.__class__.__name__).upper()}](isDateTime()): {e}')
            return False
        
    def isAPeriod(self, period_: str):
        period_string = str(period_).lower()
        return period_string.lower() in self._period
    
    def getTimeZone(self, timezone_abrev_="", country_code_="", country_=""):
        """
        Attempt to get timezone given the abbreviation, country code and country.
        Tries to find the abrev first, if that fails, country code to get a list of potential abrev and try and match
        If all else fails, use country and look through all of Olson databse 
        
        :param timezone_abrev_ (str): Initial abreviation given
        :param country_code_ (str): country code to use in case timezone_abrev_ fails
        :param country_ (str): country to use in case all else fails

        return: a timezone from Olson database or None if timezone cannot be found
        """

        # Attempt to use abrev to get timezone
        if timezone_abrev_ in pytz.all_timezones:
            return timezone_abrev_

        # Attempt to use abrev and country code to get time zone
        country_tzones = None
        try:
            country_tzones = pytz.country_timezones[country_code_]
        except:
            pass
        set_zones = set()
        if country_tzones is not None and len(country_tzones) > 0:
            for name in country_tzones:
                tzone = pytz.timezone(name)
                for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, dt.datetime.now(tzone).tzname()]]):
                    if tzabbrev.upper() == timezone_abrev_.upper():
                        set_zones.add(name)

            if len(set_zones) > 0:
                return min(set_zones, key=len)

            # none matched, at least pick one in the right country
            return min(country_tzones, key=len)

        # If all else fails, use country to get timezone instead.
        for name in pytz.all_timezones:
            if country_.lower() in name.lower():
                return name
            
        return None

    def convertTime12HTo24H(self, time_12h: str):
        """
        Try and convert a 12 hour format to 24 hours. 
        
        :param time_12h (str): 12hr string to try and convert. Must be in the format of HH:MM:SS_period

        return: 24 hour format of the string or none if failed to convert
        """

        try:
            time_object = datetime.strptime(time_12h, "%I:%M:%S %p")
            return time_object.strftime("%H:%M:%S")
        except Exception as e:
            print(f'[{str(self.__class__.__name__).upper()}](convertTime12HTo24H()): {e}')
            return None
    
    def getCurrentDate(self):
        return dt.date.today()
    
    def getCurrentTime(self):
        now = datetime.now()
        now_format = now.strftime("%H:%M:%S")
        return now_format
    
    def AddToTime(self, time: str, s=0, min=0, hrs=0):
        try:
            time_obj = parse(time)
            new = time_obj + timedelta(seconds=s, 
                                    minutes=min, 
                                    hours=hrs, 
                                    )
            return format(new, '%H:%M:%S')
        except Exception as e:
            print(f'[{str(self.__class__.__name__).upper()}](AddToTim())): {e}')
            return None
    
    def AddToDate(self, date: str, d=0, wks=0):
        try:
            date_obj = parse(date)
            date_string = str(date_obj + timedelta(days=d, weeks=wks))
            return self.FormatToDateTime(date_string, format='%Y-%m-%d')
        except Exception as e:
            print(f'[{str(self.__class__.__name__).upper()}](AddToDate()): {e}')
            return None
    
# For testing
def main():
    dt_config = DateTimeManager()
    # Testing for time
    # test_tz = "SST"
    # test_cc = "SG"
    # print(dt_config.getTimeZone(country_="Singapore"))

    # test_12h = "7pm"
    # print(dt_config.convertTime12HTo24H(test_12h))

    # print("Time: " , dt_config.getCurrentTime())
    # print("Date: " , dt_config.getCurrentDate())

    # current_time = dt_config.getCurrentTime()
    # new_time = dt_config.AddToTime(time=str(current_time), hrs=1)
    # print("New Time: " , new_time)

    # current_date = dt_config.getCurrentDate()
    # new_date = dt_config.AddToDate(date=str(current_date), d=1)
    # print("New date: ", new_date)

if __name__ == "__main__":
    main()