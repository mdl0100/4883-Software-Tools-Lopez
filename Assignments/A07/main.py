"""
Assignment A07
Marcos Lopez
Webscraping with BeautifulSoup

Description: 
    The purpose of this program is to scrape weather data from Weather Underground based on 
    user entered parameters, and present it back to the user in a GUI

    Upon launch of the program, a GUI will appear asking the user to choose the parameters to be used
    They are:
        -- The month, day, and year they would like weather data for, from 2000 to 2020
        -- The city that they would like weather data for, as long as it's a large enough place
        -- A selection if they would just that days observations, or a weekly/monthly breakdown

No direct arguments are needed for the program to run, as they are retrieved from the user.

The program outputs a GUI, but does not return any values
"""

import asyncio, json, time, PySimpleGUI as sg   # asyncio is for the dynamic page loading, and PySimpleGUI is for a GUI
from bs4 import BeautifulSoup                   # Needed for processing html data
from pyppeteer import launch                    # Needed for scraping website dynamically
from numpy import array                         # Just to transpose a matrix

def currentDate(returnType='tuple') -> None:
    # Get the current date and return it as a tuple.
    # To be used for default values if user does not select a timeframe
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

def clean_data() -> tuple[list, dict]:
    # opens airports-better.json file in ./resources and extracts the relevant parts
    # This function returns two objects
    #   1. An array, cities_display, that is used in the GUI to select a 
    #       city, country pair for weather data
    #   2. A Dictionary, lookup, that matches each city to its ICAO airport code
    #       Lookup is necessary to make the readable city name work in the 
    #       Weather Undergound url by changing to the airport code
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
            
        cities_display.sort()                              # Alphabetize list by City name
        return cities_display, lookup
            

def generate_url(cities_display: list, lookup: dict) -> tuple[str, bool]:
    # Make the GUI for the user to select the time frame
    # Arguments:
    #   - cities_display -> list of '{city}, {country}' to be display to user
    #   - lookup -> dictionary of form {'city': airport_code} 
    # Returns:
    #   - A URL as a str for Weather underground to scrape relevant data
    #       url --> https://www.wunderground.com/history/{filter}/{airport}/date/{year}-{month}-{day}
    #       example_url --> https://www.wunderground.com/history/monthly/EGPD/date/2020-6-15
    #   - A bool to let the user know if the filter is 'daily' or not. 
    #       the data is processed differently for 'daily' vs 'weekly' or 'monthly'
                               
    yearList = [i+1 for i in range(2000, 2023)]     # Generate appropriate ranges for years
    monthList = [i+1 for i in range (12)]           # ... months in a year
    dayList = [i+1 for i in range (31)]             # ... and days in a month

    sg.theme('Light Brown 10')                      # fun theme

    # layout of the GUI
    layout = [ 
            [sg.Text('Please enter your date')],
            [sg.Text('Year (2000-2023): ')], 
            [sg.Combo(yearList)], 
            [sg.Text('Month (1-12): ')], 
            [sg.Combo(monthList)], 
            [sg.Text('Day (1-31): ')], 
            [sg.Combo(dayList)],
            [sg.Text('city')], 
            [sg.Combo(cities_display)], 
            [sg.Text('Daily / Weekly / Monthly')], 
            [sg.Combo(['Daily', 'Weekly', 'Monthly'])], 
            [sg.OK()]
            ]

    # Read in values entered by the user
    window = sg.Window('Select Time and Location', layout, element_justification='left')
    event,values = window.read()    # save values entered in 'values'
    window.close()
    
    # Get current date in case needed for default values
    current_month,current_day,current_year = currentDate('tuple')   
    year = values[0] if values[0] else current_year                 # year selection, default: current year
    month = values[1] if values[1] else current_month               # month selection, default: current month
    day = values[2] if values[2] else current_day                   # day selection, default: current_day
    city = values[3].split(',')[0] if values[3] else 'New York'     # city selection, default: 'New York'
    airport = lookup[city]                                          # change city selection to relevant airport code
    filter = values[4].lower() if values[4] else 'daily'            # filter selection, default: 'daily'
    is_daily = (filter == 'daily')                                  # flag for processing data later

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, City: {city}")

    # Generate Url
    url = f'https://www.wunderground.com/history/{filter}/{airport}/date/{year}-{month}-{day}'
    return (url, is_daily)


async def scrape(url:str) -> str:
    # This program opens the relavent weather underground page and scrapes its html content
    # Arguments:
    #   - url generated by generate_url()
    # Returns:
    #   - data: the html content as a string called data

    browser = await launch()                                # launch Chrome Browser
    print("Launching Browser...")      
    page = await browser.newPage()

    print(f'Going to {url}')                                # go to url
    print('Please wait...')
    try:
        await page.goto(url)
        await page.waitForSelector('table',
                                    {'visible': True})      # will wait for tables to load or timeout
    except TimeoutError:                                    # restart if there's a TimeOut Error
        print('Recieved a TimeOut Error. Restarting page')
        return
    data = await page.content()                             # scrape page data
    await browser.close()                                   # close browser
    print('Website successfully scraped!')
    with open('./page.html', 'w', encoding='utf-8') as f:                     # save .html locally
        f.write(data)
    return data                                             # return the scraped page


def make_gui_table(page: str, is_daily=True)-> None:     
    # This program processes scraped page, extracts the table data
    # and displays it in a Table GUI
    # Arguments:
    #   - page (str) - the scrape website from scrape(), or a saved html file
    #   - is_daily(bool) - a flag for how to process the data
    # Returns:
    #   a GUI is displayed wiith the information, but no return value is given
    soup = BeautifulSoup(page, 'html.parser')           # load in the html to BeautifulSoup
    tables = soup.find_all('table')                     # find the tables on the page
    trs = tables[1].find_all('tr')                      # Find all the table rows in the second, relevant table

    data = []                                           # to hold the actual data from the data

    for row in trs:                                     # go through each table tow
        new_row = []                                    # make a new row
        for cell in row.findAll(['td', 'th']):          # find all the data or headers in the row
            new_row.append(cell.get_text().strip())     # append that data or header text to the new row
        data.append(new_row)                            # add the new row to the data

    keys = data.pop(0)                                  # save headers for table columns    


    if is_daily:                                         # clean data for table if it's a daily report
        records = data
        while [] in data:
            data.remove([])
    else:                                      # clean data for table if it's weekly or monthly
        data.pop(0)                                     # get rid of superfluous data

        records = []                                    # will hold final table rows
        temp_row = []                                   # generate each new row
        
        idx, count = 0, 0
        while len(data[idx]) == 1:                      # find out how may rows there will be
            count += 1
            idx += 1

        for stat in data:        
            temp_row.append(stat[0])                    # put data in row
            if len(temp_row) == count:
                records.append(temp_row)                # start new row
                temp_row = []        
        records = array(records).T.tolist()          # transpose to be enterable in PythonSimpleGUI


    sg.theme('LightBrown10')                            # create Table
    table = sg.Table(values=records,                    # table rows are from the records list
                    headings=keys,                     # table headers are from keys
                    auto_size_columns=True,            
                    display_row_numbers=False, 
                    justification='center',
                    alternating_row_color='lightyellow', 
                    expand_x=True, 
                    expand_y=True)
    layout = [[table],
            [sg.CloseButton('Exit')]]                # added an exit button
    window = sg.Window("Table Data", 
                    layout, 
                    size=(1200, 600), 
                    resizable=True)

    while True:                                         # Table stays open until you hit exit button
        event, values = window.read()                   # or just close the window at the table
        if event == sg.WIN_CLOSED:
            break
    window.close()
    
    sg.popup
    return


if __name__ == '__main__':
    cities_display, lookup = clean_data()                           # clean the aiport data
    url, is_daily = generate_url(cities_display, lookup)            # collect parameters from user
                                                                    #   and generate the URL and is_daily flag
    page = asyncio.get_event_loop().run_until_complete(scrape(url)) # scrape the webpage
    make_gui_table(page, is_daily)                                  # Display table GUI to user

 

