import PySimpleGUI as sg
import time
import json

"""
Description:
    This program process the data from the .json file of aiports codes located in ./resources/airports-better.json
    and generates the Weather Underground url that is to be scraped.



"""

def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    from datetime import datetime
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day':datetime.now().day,
        'month':datetime.now().month,
        'year':datetime.now().year
    }
def generate_url():
    # Clean up some of the data to more easily display in the GUI and look up airport codes
    with open('./resources./airports-better.json') as f:
        airports = json.load(f)                             # Load Data
        cities_display = []                                 # Empty List to contain cities
        countries = []                                      # List of Countries for GUI output
        lookup = {}                                         # Will contain cities matched with their aiport codes
        for item in airports:
            city = item['city']                             # Will be used in display and lookup dictionary
            country = item['country']                       # To be used in display
            cities_display.append(f'{city}, {country}')     # display will have format "city, country" e.g. "Tampa, United States"
            lookup[city] = item['icao']                     # Match city with its airport code
            
            cities_display.sort()                           # Alphabetize list by City name
                               
    yearList = [i+1 for i in range(2000, 2023)]
    monthList = [i+1 for i in range (12)]
    dayList = [i+1 for i in range (31)]

    sg.theme('Light Brown 10')

    layout = [ 
            [sg.Text('Please enter your date')],
            [sg.Text('Year: ')], 
            [sg.Combo(yearList)], 
            [sg.Text('Month: ')], 
            [sg.Combo(monthList)], 
            [sg.Text('Day: ')], 
            [sg.Combo(dayList)],
            [sg.Text('city')], 
            [sg.Combo(cities_display)], 
            [sg.Text('Daily / Weekly / Monthly')], 
            [sg.Combo(['Daily', 'Weekly', 'Monthly'])], 
            [sg.OK()]
            ]

    window = sg.Window('Select Time and Location', layout, element_justification='left')
    event,values = window.read()
    window.close()
    
    current_month,current_day,current_year = currentDate('tuple')
    year = values[0] if values[0] else current_year
    month = values[1] if values[1] else current_month
    day = values[2] if values[2] else current_day
    city = values[3].split(',')[0] if values[3] else 'New York' 
    airport = lookup[city]
    filter = values[4].lower() if values[4] else 'daily'

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, City: {city}")
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    url = f'https://www.wunderground.com/history/{filter}/{airport}/date/{year}-{month}-{day}'
    return url

if __name__ == '__main__':
    generate_url()



