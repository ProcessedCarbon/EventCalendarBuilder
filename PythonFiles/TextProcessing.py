import string
from re import sub
from re import split
from Managers.DateTimeManager import DateTimeManager
from Managers.ErrorConfig import ErrorCodes
import wordninja

class TextProcessingManager:
    _accepted_chars = ["-", "to"]
    _special_chars = string.punctuation
    _dt_config = DateTimeManager()
    _error_codes_list = ErrorCodes()._error_codes

    def MultipleDelimSplitString(self, string, delims):
        """
        Splits a string by a list of delimiters.

        :param string (str): string to be split
        :param delimiters (list): list of delimiters

        return: list of split strings
        """
        new_string = self.RemoveEnDashU2013(string)
        pattern = r'|'.join(delims)
        return split(pattern, new_string)
    
    def GetDateStruct(self, day, month, year):
        """
        Returns a structure with day, month and year. 

        :param day (str): day 
        :param month (str): month 
        :param year (str): year 

        return: structured date
        """
        return  {
                "day" : sub(r'[^0-9]', '', day),
                "month" : self._dt_config.isMonth(month) and month or None,
                "year" : self._dt_config.isYear(year) and year or None
            }
    
    def RemoveUncessarySpecialChars(self, string, special_char_to_keep):
        """
        Returns the new string where all uneeded characters are removed or the original string 
        if no characters are removed. 

        :param string (str): text to remove uneeded characters 
        :param special_char_to_keep (list): list of chars to keep

        return: structured date
        """
        for c in string:
                if c in self._special_chars:
                    if c not in special_char_to_keep:
                        string = string.replace(c, '')

        return string

    def SplitWordAndRemoveEmptySlots(self, text):
        splitted = wordninja.split(text)
        return [x for x in splitted if x != '']

    def RemoveEnDashU2013(self, text):
        return text.replace(u'\u2013', "-")

    def ConvertToTimedFormat(self, time_text: str):
        """
        Converts time_text to a acceptable time format for datetime parsing. Does not handle seconds,
        they are treated as 00 and are placed in there for the purpose of fulfilling format criteria. 

        :param time_text (str): string of text to convert to

        return: accpetable format for datetime parsing
        """
        # TODO: Handle single digit cases
        
        string_obj = str(time_text)

        # Remove all spaces and special char from string object
        for c in string_obj:
            if c == " " or c.isalnum() == False:
                string_obj = string_obj.replace(c, "")
        
        # Check return None if time includes seconds, if not check if first digit of hour is single
        if len(string_obj) > 6:
            print(f"[{str(self.__class__.__name__).upper()}](ConvertToTimedFormat()): {self._error_codes_list[1000]}")
            return None
        
        # Pad string with zeros till length is even, do not take into account last 2 char when counting len
        while len(string_obj[:len(string_obj) - 2]) % 2 != 0:
            string_obj = "0" + string_obj

        # check if string has seconds included
        # Disregard seconds because timing of an event rarely comes in w/ seconds

        H = string_obj[:2]
        M = self._dt_config.isAPeriod(string_obj[2:4]) and "00" or string_obj[2:4]
        P = self._dt_config.isAPeriod(string_obj[-2:]) and string_obj[-2:].upper() or ""

        # Convert 24h time format to 12h to remain consistent
        #if self._dt_config.isAPeriod(P) == False:
            # P = (int(H) > 12) and "PM" or "AM"
            # H = (int(H) > 12) and str(int(H) - 12) or str(H)
        
        return H + ":" + M + ":00" + " " + P 

    def ProcessDateForGoogleCalendar(self, date_text: str):
        """
        Returns a list of strings formatted in the way that can be used for Google Calendars. 

        :param date_text (str): string of text that has the dates 

        return: list of formatted dates suitable for google calendars
        """

        if date_text == "None" or "" or len(date_text) <= 0:
            print(f"[{str(self.__class__.__name__).upper()}](ProcessTimeForGoogleCalendars()): {self._error_codes_list[1000]}")
            return []

        date_to_use = self.RemoveUncessarySpecialChars(string=date_text, special_char_to_keep=self._accepted_chars)
        splitted_date = self.MultipleDelimSplitString(string=date_to_use, delims=self._accepted_chars)

        # Find year
        # At this point max each array slot should have max DD MM YYYY
        list_of_processed = []
        for date in splitted_date:
            remove_empty = self.SplitWordAndRemoveEmptySlots(text=date)
            
            # Remove anything that is not a month or number
            for var in remove_empty:
                if var.isdigit() == False and not self._dt_config.isMonth(var):
                    remove_empty.remove(var)

            # Len == 1 > Only has day
            # Len == 2 > Has both day and month
            # Len == 3 > Has all day, month and year
            date_struct = self.GetDateStruct(day=remove_empty[0], 
                                             month=len(remove_empty) > 1 and remove_empty[1] or 0,
                                             year=len(remove_empty) > 2 and remove_empty[2] or 0
                                            )
            # Get reference month and year from a substring that has one
            founded_month = date_struct['month'] != None and date_struct['month'] or None
            founded_year = date_struct['year'] != None and date_struct['year'] or None

            list_of_processed.append(date_struct)
        
        # Assign year and month to be used for substrings that do not posses one
        currentDate = self._dt_config.getCurrentDate()
        year = founded_year != None and founded_year or currentDate.year
        month = founded_month != None and founded_month or currentDate.month

        for index, struct in enumerate(list_of_processed):
            struct['month'] = struct['month'] == None and month or struct['month']
            struct['year'] = struct['year'] == None and year or struct['year']

            s_date = str(struct['day']) + str(struct['month']) + str(struct['year'])
            list_of_processed[index] = self._dt_config.FormatToDateTime(date_string=s_date, format='%Y-%m-%d')

        return len(list_of_processed) == 1 and list_of_processed[0] or list_of_processed
    
    def ProcessTimeForGoogleCalendars(self, time_text: str):
        """
        Returns a list of time strings formatted in the way that can be used for Google Calendars. 

        :param time_text (str): string of text that has the dates 

        return: list of formatted times suitable for google calendars
        """

        if time_text == "None" or "" or len(time_text) <= 0:
            print(f"[{str(self.__class__.__name__).upper()}](ProcessTimeForGoogleCalendars()): {self._error_codes_list[1000]}")
            return []

        # Form new list of accepted chars which include delims and time periods
        new_accepted_chars = self._accepted_chars + self._dt_config._period

        # Remove uncessary special chars and delim string
        time_to_use = self.RemoveUncessarySpecialChars(string=time_text, special_char_to_keep=new_accepted_chars)
        splitted_time = self.MultipleDelimSplitString(string=time_to_use, delims=self._accepted_chars)

        list_of_correct_time_format = []
        for time in splitted_time:
            # Remove empty elements in list
            time_list = self.SplitWordAndRemoveEmptySlots(text=time)
            
            # Remove uncessary chars from list
            for text in time_list:
                if text.isdigit() == False and not self._dt_config.isAPeriod(text):
                    time_list.remove(text)
            
            # Combine remaining char in list to form the time string
            time_string = str(time_list)
            time_format = self.ConvertToTimedFormat(time_string)
            if time_format != None:
                list_of_correct_time_format.append(time_format)
            
        # Check if there are any time format without a period
        # 2 Problems with this
        #   1. Still encounter problems like these (4-6pm, ['4::00 PM', '18:00:00'])
        period = ""
        for format in list_of_correct_time_format:
            if self._dt_config.isAPeriod(format[-2:]):
                period = format[-2:].upper()
                break

        if period != "":
            for i in range(len(list_of_correct_time_format)):
                format = list_of_correct_time_format[i]
                if self._dt_config.isAPeriod(format[-2:]) == False:
                    list_of_correct_time_format[i] += str(period)
        else:
            for i in range(len(list_of_correct_time_format)):
                format = list_of_correct_time_format[i]
                split = format.split(":")
                H = split[0]
                period = (int(H) >= 12) and "PM" or "AM"
                H = (int(H) >= 12) and str(int(H) - 12) or str(H)
                split[0] = H
                new_format = ':'.join(split)
                new_format += period
                list_of_correct_time_format[i] = new_format

        for index, time_format in enumerate(list_of_correct_time_format):
            time_obj = self._dt_config.convertTime12HTo24H(time_format)
            if time_obj != None:
                list_of_correct_time_format[index] = time_obj

        return len(list_of_correct_time_format) == 1 and list_of_correct_time_format[0] or list_of_correct_time_format

# ================================================  TEST ======================================================================== #
def Test_ProcessTimeForGoogleCalendars():
    print("==========================================================================================")
    print("Test_ProcessTimeForGoogleCalendars")
    print("==========================================================================================")

    text_process_manager = TextProcessingManager()
    # Testing for time
    convert12HTo24H_test_list ={
        # "12am",
        # "1.30am",
        # "1330",
        # "230pm",
        # "1pm",
        # "12.30 - 3pm",
        # "1pm - 3pm",
        "4-6pm"
    }

    for t in convert12HTo24H_test_list:
        print("Original: ", t)
        print(f"After: {text_process_manager.ProcessTimeForGoogleCalendars(t)}")
        print("------------------------------------------------")
    print("==========================================================================================")

# For testing
def main():
    t = TextProcessingManager()

    # Testing for date
    # test_date = "23rd to 25th Aug"
    # formatted = t.ProcessDateForGoogleCalendar(test_date)
    # for f in formatted:
    #     print(f)

    Test_ProcessTimeForGoogleCalendars()

if __name__ == "__main__":
    main()

    
    