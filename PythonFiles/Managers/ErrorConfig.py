class ErrorCodes:
    _code = 0
    def __init__(self):
        _key = self.getKey()
        self._error_codes = {
            _key() : "INVALID PARAM GIVEN!",    # 1000
            _key() : "MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST",    # 1001
        }
    
    def getKey(self):
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