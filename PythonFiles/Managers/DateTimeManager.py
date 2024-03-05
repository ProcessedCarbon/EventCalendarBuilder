import datetime as dt
import pytz
from datetime import datetime, timedelta
from dateutil.parser import parse
from zoneinfo import ZoneInfo
import logging

class DateTimeManager:
    _months = [
            "january",
            "february",
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
            "dec",]
    
    _period = ["am", "pm"]
    
    _years = {str(x) for x in range(2000, dt.date.today().year)}

    def isMonth(month: str):
        return (str(month).lower() in DateTimeManager._months)

    def isYear(year):
        return (year in DateTimeManager._years)
    
    # Attempts to format date time to datetime datatype
    def FormatToDateTime(date_string: str, format: str):
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
            logging.error(f'[{__name__}]: {e}')
            return None 
    
    def isDateTime(datetime_: str, fuzzy: bool):
        try:
            parse(datetime_, fuzzy=fuzzy)
            return True
        except Exception as e:
            logging.error(f'[{__name__}]: {e}')
            return False
        
    def isAPeriod(period_: str):
        period_string = str(period_).lower()
        return period_string.lower() in DateTimeManager._period

    # Converts a given 12H time in HH MM SS pp to 24H format
    def convertTime12HTo24H(time_12h: str):
        """
        Try and convert a 12 hour format to 24 hours. 
        
        :param time_12h (str): 12hr string to try and convert. Must be in the format of HH:MM:SS_period

        return: 24 hour format of the string or none if failed to convert
        """

        try:
            time_object = datetime.strptime(time_12h, "%I:%M:%S %p")
            return time_object.strftime("%H:%M:%S")
        except Exception as e:
            logging.error(f'[{__name__}]: {e}')
            return None
    
    def getCurrentDate():
        return dt.date.today()
    
    def getCurrentTime():
        now = DateTimeManager.getDateTimeNow()
        now_format = now.strftime("%H:%M:%S")
        return now_format
    
        # Converts a given 12H time in HH MM SS pp to 24H format
    
    # Performs addition to a time given
    def AddToTime(time: str, s=0, min=0, hrs=0):
        try:
            time_obj = parse(time)
            new = time_obj + timedelta(seconds=s, 
                                    minutes=min, 
                                    hours=hrs, 
                                    )
            return format(new, '%H:%M:%S')
        except Exception as e:
            logging.error(f'[{__name__}]: {e}')
            return None
    
    # Performs addition to a date
    def AddToDate(date: str, d=0, wks=0):
        try:
            date_obj = parse(date)
            date_string = str(date_obj + timedelta(days=d, weeks=wks))
            return DateTimeManager.FormatToDateTime(date_string, format='%Y-%m-%d')
        except Exception as e:
            logging.error(f'[{__name__}]: {e}')
            return None
    
    # 2023-05-17 14:00:00+08:00
    # Returns format YYYY-MM-DD HH:MM:SS Z
    def getDateTime(hour:int, min:int, sec:int, day:int, month:int, year:int)->datetime:
        # Handle timezone
        tz = ZoneInfo("Singapore")
        return datetime(year, month, day, hour, min, sec, tzinfo=tz)
    
    # Accepts only format of YYYY-MM-DD HH:MM:SS z for both
    def hasDateTimeClash(start1:str, end1:str, start2:str, end2:str, fmt='%Y-%m-%d %H:%M:%S%z')->bool:
        # Format: %Y-%m-%d %H:%M:%S%z
        try:
            start_1 = datetime.strptime(start1, fmt)
            end_1 = datetime.strptime(end1, fmt)

            start_2 = datetime.strptime(start2, fmt)
            end_2 = datetime.strptime(end2, fmt)
            
            return start_1 <= end_2 and start_2 <= end_1
        except Exception as e:
            logging.error(f'[{__name__}]: {e}')

    def CompareTimes(time_str1, time_str2, fmt='%H:%M:%S')->bool:
        """Compare two time strings and print if the first is smaller, equal, or larger than the second."""
        
        # Convert strings to datetime objects
        time1 = DateTimeManager.getDateTimeObject(time_str1, fmt)
        time2 = DateTimeManager.getDateTimeObject(time_str2, fmt)
        
        # Compare times
        return time1 < time2
    
    def getTimeStamps(timestamps:int):
        return datetime.fromtimestamp(timestamps)
    
    def getDateTimeNow():
        return datetime.now()
    
    def getDateTimeObject(time, fmt='%H:%M:%S'):
        return datetime.strptime(time, fmt)