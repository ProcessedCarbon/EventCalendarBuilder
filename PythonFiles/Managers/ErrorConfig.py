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
        # Getting the call stack
        stack = inspect.stack()
        # The previous frame in the stack is the caller
        caller_frame = stack[1]
        # Extract details from the caller frame
        caller_function_name = caller_frame.function
        caller_class_name = caller_frame[0].f_locals.get("self", None).__class__.__name__
        print(f'[{caller_class_name.upper()}]({caller_function_name}()): {ErrorCodes._error_codes[errorCode]}')
    
    def PrintCustomError(e:str):
        # Getting the call stack
        stack = inspect.stack()
        # The previous frame in the stack is the caller
        caller_frame = stack[1]
        # Extract details from the caller frame
        caller_function_name = caller_frame.function
        caller_class_name = caller_frame[0].f_locals.get("self", None).__class__.__name__
        print(f'[{caller_class_name.upper()}]({caller_function_name}()): {e}')

def getParamValFromKwarg(param_name:str, kwargs:dict, default=None, allowNone=True):
    return kwargs[param_name] if param_name in kwargs else default

def main():
    error_code = ErrorCodes()
    print(error_code._error_codes[1000])


if __name__ == "__main__":
    main()