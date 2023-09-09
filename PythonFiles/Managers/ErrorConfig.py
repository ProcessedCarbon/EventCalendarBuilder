class ErrorCodes:
    _code = 0
    def __init__(self):
        _key = ErrorCodes.getKey()
        self._error_codes = {
            _key() : "INVALID PARAM GIVEN!",                                                                # 1000
            _key() : "MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST",    # 1001
            _key() : "NO PAGES FOUND!",                                                                     # 1002
            _key() : "MISSING PAGES, PAGE NOT FOUND!",                                                      # 1003
            _key() : "MISSING MAIN APP WINDOW!",                                                            # 1004
        }
    
    # Dynamically returns a key
    def getKey():
        info = {"count" : 999}
        def number():
            info["count"] += 1
            return info['count']
        return number
        
    
def main():
    error_code = ErrorCodes()
    print(error_code._error_codes[1000])


if __name__ == "__main__":
    main()