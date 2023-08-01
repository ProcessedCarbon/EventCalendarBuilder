import requests

class Interface:
    
    def getCurrentCountry(self):
        try:
            # Go online and try to get current location
            response = requests.get('http://ip-api.com/json').json()
            return response['country']
        except Exception as e:
            print(f"Error: {e}")
            return None

# For testing
def main():
    location_manager = Interface()
    print(location_manager.getCurrentCountry())

if __name__ == "__main__":
    main()