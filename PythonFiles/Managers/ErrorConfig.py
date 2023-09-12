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
            _code() : "NONE PROVIDED FOR NON-NONE PARAM!",                                                   # 1005
        }

    def PrintErrorWithCode(errorCode:int):
        className, methodName = ErrorCodes.getCallerClassAndMethod()
        print(f'[{className.upper()}]({methodName}()): {ErrorCodes._error_codes[errorCode]}')
    
    def PrintCustomError(e:str):
        className, methodName = ErrorCodes.getCallerClassAndMethod()
        print(f'[{className.upper()}]({methodName}()): {e}')
    
    def getCallerClassAndMethod()->list[str,str]:
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name
        return the_class, the_method

def getParamValFromKwarg(param_name:str, kwargs:dict, default=None, allowNone=True):
    return kwargs[param_name] if param_name in kwargs else default

def main():
    error_code = ErrorCodes()
    print(error_code._error_codes[1000])


if __name__ == "__main__":
    main()