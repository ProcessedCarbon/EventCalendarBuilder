import inspect

# Dynamically returns a key
def getCode(start_val):
    info = {"count" : start_val}
    def number():
        info["count"] += 1
        return info['count']
    return number

class ErrorCodes:
    _code = 0
    _code = getCode(999)
    _error_codes = {
            _code() : "INVALID PARAM GIVEN!",                                                                # 1000
            _code() : "MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST",    # 1001
            _code() : "NO PAGES FOUND!",                                                                     # 1002
            _code() : "MISSING PAGES, PAGE NOT FOUND!",                                                      # 1003
            _code() : "MISSING MAIN APP WINDOW!",                                                            # 1004
        }

    def PrintError(errorCode:int):
        # current_frame = inspect.currentframe()
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name
        # caller_frame = current_frame.f_back
        # caller_name = caller_frame.f_globals["__name__"]
        # caller_class = caller_frame.f_locals["self"].__class__.__name__

        print(f'[{the_class.upper()}]({the_method}()): {ErrorCodes._error_codes[errorCode]}')

def main():
    error_code = ErrorCodes()
    print(error_code._error_codes[1000])


if __name__ == "__main__":
    main()