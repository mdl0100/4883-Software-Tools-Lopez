""" 
Description:
    This is an example gui that allows you to enter the appropriate parameters to get the weather from wunderground.
TODO:
"""
import PySimpleGUI as sg      

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

def buildWeatherURL(month=None, day=None, year=None, airport=None, filter=None):
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month,current_day,current_year = currentDate('tuple')
    
    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year
    
    # Create the gui's layout using text boxes that allow for user input without checking for valid input
    layout = [
        [sg.Text('Month')],[sg.InputText(month)],
        [sg.Text('Day')],[sg.InputText(day)],
        [sg.Text('Year')],[sg.InputText(year)],
        [sg.Text('Code')],[sg.InputText()],
        [sg.Text('Daily / Weekly / Monthly')],[sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]      

    window = sg.Window('Get The Weather', layout, element_justification='left')    

    event, values = window.read()
    window.close()
        
    month = values[0]
    day = values[1]
    year = values[2]
    code = values[3]
    filter = [4]

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, Code: {code}, Filter: {filter}")

    # return the URL to pass to wunderground to get appropriate weather data

if __name__=='__main__':
    buildWeatherURL()
