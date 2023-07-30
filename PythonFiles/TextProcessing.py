import string
from re import sub
from re import split
import DateTimeConfigs

class Interface:
    def __init__(self):
        self._accepted_chars = ["-", "to"]
        self._special_chars = string.punctuation
        self._dt_config = DateTimeConfigs.DTConfigs()

    def MultipleDelimSplitString(self, string, delims):
        """
        Splits a string by a list of delimiters.

        :param string (str): string to be split
        :param delimiters (list): list of delimiters

        return: list of split strings
        """
        pattern = r'|'.join(delims)
        return split(pattern, string)

    
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
                        test_date = string.replace(c, '')

        return 'test_date' in locals() and test_date or string

    def ProcessDateForGoogleCalendar(self, date_text):
        """
        Returns a list of strings formatted in the way that can be used for Google Calendars. 

        :param date_text (str): string of text that has the dates 

        return: list of formatted dates suitable for google calendars
        """
        date_to_use = self.RemoveUncessarySpecialChars(string=date_text, special_char_to_keep=self._accepted_chars)
        splitted_date = self.MultipleDelimSplitString(string=date_to_use, delims=self._accepted_chars)

        # Find year
        # At this point max each array slot should have max DD MM YYYY
        list_of_processed = []
        for date in splitted_date:
            d = date.split(" ")
            remove_empty = [x for x in d if x != '']
            
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
        year = founded_year != None and founded_year or self._dt_config.today.year
        month = founded_month != None and founded_month or self._dt_config.today.month

        formatted = []
        for struct in list_of_processed:
            struct['month'] = struct['month'] == None and month or struct['month']
            struct['year'] = struct['year'] == None and year or struct['year']

            s_date = str(struct['day']) + str(struct['month']) + str(struct['year'])
            formatted.append(self._dt_config.FormatToDateTime(date_string=s_date, format='%Y-%m-%d'))

        return formatted
    
    def ProcessTimeForGoogleCalendars(self, time_text):
        return self._dt_config.isTime(time_text, '%H:%M:%S')

# For testing
def main():
    t = Interface()

    # Testing for date
    test_date = "23rd Aug 42"
    formatted = t.ProcessDateForGoogleCalendar(test_date)
    for f in formatted:
        print(f)

    # Testing for time
    # test_time = "4-6pm"
    # print(t.ProcessTimeForGoogleCalendars(test_time))

if __name__ == "__main__":
    main()

    
    