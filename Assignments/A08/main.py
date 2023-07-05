"""
Marcos Lopez - 5443 Software Tools
A08 - API - Covid Data

Create a RESTful API using FastAPI that provides access to COVID-19 data. 
The API will fetch the data from a publicly available data source and expose 
endpoints to retrieve various statistics related to COVID-19 cases.

The data source is a CSV file that contains COVID-19 data from 2020-2023.

If program gives error: Error loading ASGI app. Could not import module "api" 
    then run this command: uvicorn main:app --reload --port 5000

------------------------------------------------------------
#	Column	Description
0	Date_reported	date in yyyy-mm-dd format
1	Country_code	A unique 2 digit country code           (not used)
2	Country	Name of the country
3	WHO_region	World Health Organization region
4	New_cases	Number of new cases on this date
5	Cumulative_cases	Cumulative cases up to this date    (not used)
6	New_deaths	Number of new deaths on this date
7	Cumulative_deaths	Cumulative deaths up to this date   (not used)
------------------------------------------------------------

Github Copilot was used to help write the comments in this file to keep them consistent 
between the API routes and between the functions.

"""


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import csv

description = """
## Marcos Lopez - 5443 Software Tools
### A08 - API - Covid Data
Where code break less often than you'd think👌
But not more than you'd like 😔
"""

app = FastAPI(
    description=description,
)

db = []

# Open the CSV file
with open('data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    i = 0
    # Read each row in the CSV file
    for row in reader:
        if i == 0:
            header = row
            i += 1
            continue
        db.append(row)

##### Helper Functions

def getUniqueCountries():
    """
    This function will return a list of unique countries in the data set.
    - **Params:**
        - None
    - **Returns:**
        - A list of unique countries in the data set.
    """
    global db
    countries = {}
    for row in db:                      # Loop through each row in the data set
        if not row[2] in countries:     # If the country is not in the dictionary
            countries[row[2]] = 0       # Add it to the dictionary

    return list(countries.keys())       # Return the list of countries

def getUniqueWhos():
    """
    This function will return a list of unique WHO regions in the data set.
    - **Params:**
        - None
    - **Returns:**
        - A list of unique WHO regions in the data set.
    """
    global db
    whos = {}

    for row in db:              # Loop through each row in the data set
        if not row[3] in whos:  # If the WHO region is not in the dictionary
            whos[row[3]] = 0    # Add it to the dictionary
   
    return list(whos.keys())    # Return the list of WHO regions

##### Generic Routes
@app.get("/")
async def docs_redirect():
    """## Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/countries/")
async def countries():
    """
    ## This method returns a list of unique countries in the data set.
    - **Params:**
        - None
    - **Returns:**
        - A list of unique countries in the data set.

    #### Example 1:
    [https://localhost:5000/countires/](https://localhost:5000/countires/)

    #### Response 1:
    {
        "countries": [
            "Afghanistan",
            "Albania",
            ...
            "Zimbabwe"
        ]
    }     
    """
    return {"countries":getUniqueCountries()} # Return the list of countries


@app.get("/whos/")
async def whos():
    """
    ## This method returns a list of unique WHO regions in the data set.
    - **Params:**
        - None
    - **Returns:**
        - A list of unique WHO regions in the data set.

    #### Example 1:
    [https://localhost:5000/whos/](https://localhost:5000/whos/)

    #### Response 1:
    {
        "whos": [
            "AFRO",
            "AMRO",
            ...
            "WPRO"
        ]
    }
    
    #### Note:
    These are the WHO regions and their corresponding names:
    - AFRO  -> "Africa"
    - AMRO  -> "Region of the Americas"
    - SEARO -> "South-East Asian Region"
    - EURO  -> "European Region"
    - EMRO  -> "Eastern Mediterranean Region"
    - WPRO  -> "Western Pacific Region"
    """
    return {"whos":getUniqueWhos()} # Return the list of WHO regions

######## Case Routes
@app.get("/cases/")
async def cases():
    """
    ## This method returns a list total cases in the world by year and also the total number of cases.
    - **Params:**
        - None
    - **Returns:**
        - A list total cases in the world by year and also the total number of cases.

    #### Example 1:
    [https://localhost:5000/cases/](https://localhost:5000/cases/)

    #### Response 1:
    {
        "Cases By Year": {
            "2020": 82853510,
            "2021": 204177273,
            "2022": 443412916,
            "2023": 37743397,
            "total": 768187096
        },
    "success": true,
    "message": "Cases by Year",
    "size": 5
    }
    """
    cases = {       # Create a dictionary to hold the cases by year
        "2020":0,
        "2021":0,
        "2022":0,
        "2023":0,
        "total":0
    }
    for row in db:                          # Loop through each row in the data set
        cases[row[0][:4]] += int(row[4])    # Add the number of cases to the corresponding year
        cases["total"] += int(row[4])       # Add the number of cases to the total
    
    return {"Cases By Year":cases,"success":True,"message":"Cases by Year","size":len(cases)} # Return the dictionary of cases by year

@app.get("/cases_by_country/")
async def cases_by_country(country:str = None, year:int = None):
    """
    ##This method returns the number of cases by country.
    - If a country is specified, it will only pull the data from that country.
        - Valid countries are listed in the countries route.
        - An empty string will list all countries.
    - If a year is specified, it will only pull the data from that year.
        - Valid years are 2020-2023.
        - An empty year will list total cases for the entire date range.

    - **Params:**
        - country (optional):str The country to pull data from.
        - year (optional):int The year to pull data from.
    - **Returns:**
        - The number of cases by country.

    #### Example 1:
    [https://localhost:5000/cases_by_country/](https://localhost:5000/cases_by_country/)

    #### Response 1:
    {
        "Cases By Country": {
            "Afghanistan": 222954,
            "Albania": 334090,
            ...
            "Zimbabwe": 265413
        },
    "success": true,
    "message": "Cases by Country",
    "size": 194,
    "country": null,
    "year": null
    }

    #### Example 2:
    [https://localhost:5050/cases_by_country/?country=Brazil](https://localhost:5050/cases_by_country/?country=Brazil)

    #### Response 2:

    {
        "Cases By Country": {
            "Brazil": 37639324
        },
    "success": true,
    "message": "Cases by Country",
    "size": 1,
    "country": "Brazil",
    "year": null
    
    #### Example 3:
    [http://localhost:5000/cases_by_country/?country=Brazil&year=2021](http://localhost:5000/cases_by_country/?country=Brazil&year=2021)

    #### Response 3:

    {
        "Cases By Country": {
            "Brazil": 14700283,
        },
    "success": true,
    "message": "Cases by Country",
    "size": 1,
    "country": "Brazil",
    "year": 2021
    }
    """


    cases = {}
    
    for row in db:                                      # Loop through each row in the data set
        if country != None and country != row[2]:       # If a country is specified and it doesn't match the row's country, skip it
            continue
        if year != None and year != int(row[0][:4]):    # If a year is specified and it doesn't match the row's year, skip it
            continue
            
        if not row[2] in cases:                         # If the country isn't in the dictionary, add it
            cases[row[2]] = 0
        cases[row[2]] += int(row[4])                    # Add the number of cases to the country's total           

    return {"Cases By Country":cases,"success":True,"message":"Cases by Country","size":len(cases),"country":country,"year":year}

@app.get("/cases_by_region/")
async def cases_by_region(region:str = None, year:int = None):
    """
    ## This method returns the number of cases by region.
    - If a region is specified, it will only pull the data from that region.
        - Valid regions are listed in the whos route.
        - An empty string will list all regions.
    - If a year is specified, it will only pull the data from that year.
        - Valid years are 2020-2023.
        - An empty year will list total cases for the entire date range.

    - **Params:**
        - region (optional):str The region to pull data from. 
        - year (optional):int The year to pull data from.
    - **Returns:**
        - The number of cases by region.

    #### Example 1:
    [https://localhost:5000/cases_by_region/](https://localhost:5000/cases_by_region/)

    #### Response 1:
    {
        "Cases By Region": {
            "AFRO": 9538679,
            "AMR": 193056651,
            ...
            "WPRO": 204478043
        },
        "success": true,
        "message": "Cases by Region",
        "size": 7,
        "year": null
    }
    """

    cases = {}
    
    for row in db:                                      # Loop through each row in the data set
        if region != None and region != row[3]:         # If a region is specified and it doesn't match the row's region, skip it
            continue
        if year != None and year != int(row[0][:4]):    # If a year is specified and it doesn't match the row's year, skip it      
            continue
            
        if not row[3] in cases:                         # If the region isn't in the dictionary, add it
            cases[row[3]] = 0
        cases[row[3]] += int(row[4])                    # Add the number of cases to the region's total

    return {"Cases By Region":cases,"success":True,"message":"Cases by Region","size":len(cases),"year":year}

######## Death Routes
@app.get("/deaths/")
async def deaths():
    """
    ## This method returns the number of deaths by year for the whole world.
    **Params**
        - None
    **Returns**
        - A dictionary of deaths by year.

    #### Example 1:
    [https://localhost:5000/deaths/](https://localhost:5000/deaths/)

    #### Response 1:
    {
        "Total Deaths": {
            "2020": 1946775,
            "2021": 3531524,
            "2022": 1238186,
            "2023": 229229,
            "total": 6945714
        },
    "success": true,
    "message": "Deaths by Year",
    "size": 5
    }
    """
    deaths = {                              # Create a dictionary to hold the deaths by year
        "2020":0,   
        "2021":0,
        "2022":0,
        "2023":0,
        "total":0
    }
    for row in db:                          # Loop through each row in the data set
        deaths[row[0][:4]] += int(row[6])   # Add the number of deaths to the year's total
        deaths["total"] += int(row[6])      # Add the number of deaths to the total
    
    return {"Total Deaths":deaths,"success":True,"message":"Deaths by Year","size":len(deaths)}

@app.get("/deaths_by_country/")
async def deaths_by_country(country:str = None, year:int = None):
    """
    ## This method returns the number of deaths by country.
    - If a country is specified, it will only pull the data from that country.
        - Valid countries are listed in the countries route.
        - An empty string will list all countries.
    - If a year is specified, it will only pull the data from that year.
        - Valid years are 2020-2023.
        - An empty year will list total deaths for the entire date range.

    - **Params:**
        - country (optional):str The country to pull data from.
        - year (optional):int The year to pull data from.
    - **Returns:**
        - The number of deaths by country.

    #### Example 1:
    [https://localhost:5000/deaths_by_country/](https://localhost:5000/deaths_by_country/)

    #### Response 1:
    {
        "Deaths by Country": {
            "Afghanistan": 7922,
            "Albania": 3604,
            ...
            "Zimbabwe": 5707
        },
    "success": true,
    "message": "Deaths by Country",
    "size": 194,
    "country": null,
    "year": null
    }

    #### Example 2:
    [https://localhost:5050/deaths_by_country/?country=Brazil](https://localhost:5050/deaths_by_country/?country=Brazil)

    #### Response 2:
    {
        "Deaths by Country": {
            "Brazil": 703399
        },
        "success": true,
        "message": "Deaths by Country",
        "size": 1,
        "country": "Brazil",
        "year": null
    }

    #### Example 3:
    [https://localhost:5050/deaths_by_country/?country=Brazil&year=2021](https://localhost:5050/deaths_by_country/?country=Brazil&year=2021)

    #### Response 3:
    {
        "Deaths by Country": {
            "Brazil": 426136
        },
        "success": true,
        "message": "Deaths by Country",
        "size": 1,
        "country": "Brazil",
        "year": 2021
    }
    """
    deaths = {}
    
    for row in db:                                      # Loop through each row in the data set
        if country != None and country != row[2]:       # If a country is specified and it doesn't match the row's country, skip it
            continue
        if year != None and year != int(row[0][:4]):    # If a year is specified and it doesn't match the row's year, skip it       
            continue
            
        if not row[2] in deaths:                        # If the country isn't in the dictionary, add it
            deaths[row[2]] = 0
        deaths[row[2]] += int(row[6])                   # Add the number of deaths to the country's total

    return {"Deaths by Country":deaths,"success":True,"message":"Deaths by Country","size":len(deaths),"country":country,"year":year}

@app.get("/deaths_by_region/")
async def deaths_by_region(region:str = None, year:int = None):
    """
    ## This method returns the number of deaths by region.
    - If a region is specified, it will only pull the data from that region.
        - Valid regions are listed in the WHOS route.
        - An empty string will list all regions.
    - If a year is specified, it will only pull the data from that year.
        - Valid years are 2020-2023.
        - An empty year will list total deaths for the entire date range.

    - **Params:**
        - region (optional):str The region to pull data from. 
        - year (optional):int The year to pull data from.
    - **Returns:**
        - The number of deaths by region.

    #### Example 1:
    [https://localhost:5000/deaths_by_region/](https://localhost:5000/deaths_by_region/)

    #### Response 1:

    {
        "Deaths By Region": {
            "EMRO": 351329,
            "EURO": 2242877,
            "AFRO": 175394,
            "WPRO": 413525,
            "AMRO": 2956210,
            "SEARO": 806366,
            "Other": 13
        },
    "success": true,
    "message": "Deaths by Region",
    "size": 7,
    "year": null
    }

    #### Example 2:
    [https://localhost:5050/deaths_by_region/?region=EMRO](https://localhost:5050/deaths_by_region/?region=EMRO)

    #### Response 2:
    {
        "Deaths By Region": {
            "EMRO": 351329
        },
    "success": true,
    "message": "Deaths by Region",
    "size": 1,
    "year": null
    }

    #### Example 3:
    [https://localhost:5050/deaths_by_region/?region=EMRO&year=2021](https://localhost:5050/deaths_by_region/?region=EMRO&year=2021)

    #### Response 3:
    {
        "Deaths By Region": {
            "EMRO": 195342
        },
    "success": true,
    "message": "Deaths by Region",
    "size": 1,
    "year": 2021
    }

    """

    deaths = {}
    
    for row in db:                                          # Loop through each row in the data set                           
        if region != None and region != row[3]:             # If a region is specified and it doesn't match the row's region, skip it
            continue
        if year != None and year != int(row[0][:4]):        # If a year is specified and it doesn't match the row's year, skip it
            continue
            
        if not row[3] in deaths:                            # If the region isn't in the dictionary, add it     
            deaths[row[3]] = 0
        deaths[row[3]] += int(row[6])                       # Add the number of deaths to the region's total

    return {"Deaths By Region":deaths,"success":True,"message":"Deaths by Region","size":len(deaths),"year":year}

######## Aggregate Routes
@app.get("/max_deaths/")
async def max_deaths(year:int = None):
    """
    ## This method returns the country with the most deaths and the number of deaths for that country.
    - If a year is specified, it will only pull the data from that year.
        - Valid years are 2020-2023.
        - An empty year will list total deaths for the entire date range of the data set.

    - **Params:**
        - year (optional):int The year to pull data from.
    - **Returns:**
        - The country with the most deaths and the number of deaths for that country.

    #### Example 1:
    [https://localhost:5000/max_deaths/](https://localhost:5000/max_deaths/)

    #### Response 1:
    {
        "Max Deaths": 1127152,
        "Country": "United States of America",
        "success": true,
        "message": "Max Deaths by Country",
        "size": 1,
        "year": null
    }
    
    #### Example 2:
    [https://localhost:5050/max_deaths/?year=2021](https://localhost:5050/max_deaths/?year=2021)

    #### Response 2:
    {
        "Max Deaths": 467051,
        "Country": "United States of America",
        "success": true,
        "message": "Max Deaths by Country",
        "size": 1,
        "year": 2021
    }
    """
    max_deaths = 0
    max_country = ""
    countries = getUniqueCountries()                            # Get a list of all the countries in the data set
    for country in countries:                                   # Loop through each country    
        if year != None:                                        # If a year is specified, only pull data from that year      
            deaths = await deaths_by_country(country,year)      
        else:                                                   # If no year is specified, pull data from the entire data set                          
            deaths = await deaths_by_country(country)
        deaths = deaths["Deaths by Country"][country]           # Get the number of deaths for the country
        if deaths > max_deaths:                                 # If the number of deaths is greater than the current max, update the max
            max_deaths = deaths
            max_country = country

    return {"Max Deaths":max_deaths,"Country":max_country,"success":True,"message":"Max Deaths by Country","size":1,"year":year}

@app.get("/max_deaths_date_range/")
async def max_deaths_date_range(start_date:str = '2020-01-01', end_date:str = '2023-06-21'):
    """
    ## This method returns the country with the most deaths and the number of deaths for that country during the given date range.
    - If a start date is specified, it will only pull the data from after that date.
        - If no start date is specified, it will default to 2020-01-01.
        - Valid dates are 2020-01-01 to 2023-06-21.
    - If an end date is specified, it will only pull the data from before that date.
        - If no end date is specified, it will default to 2023-06-21.
        - Valid dates are 2020-01-01 to 2023-06-21.

    - **Params:**
        - start_date (optional):str in the format YYYY-MM-DD. The start date to pull data from.
        - end_date (optional):str in the format YYYY-MM-DD. The end date to pull data from.
    - **Returns:**
        - The country with the most deaths and the number of deaths for that country during the given date range.

    #### Example 1:
    [https://localhost:5000/max_deaths_date_range/?start_date=2021-06-15&end_date=2021-08-15](https://localhost:5000/max_deaths_date_range/?start_date=2021-06-15&end_date=2021-08-15)

    #### Response 1:
    {
        "Max Deaths": 81590,
        "Country": "Brazil",
        "success": true,
        "message": "Max Deaths by Country",
        "size": 1,
        "start_date": "2021-06-15",
        "end_date": "2021-08-15"
    }
    """
    begin = datetime.strptime(start_date, '%Y-%m-%d')       # Convert the start date to a datetime object
    end = datetime.strptime(end_date, '%Y-%m-%d')           # Convert the end date to a datetime object
    if begin > end:                                         # If the start date is after the end date, return an error                   
        return {"success":False,"message":"Start date must be before end date.","size":0,"start_date":start_date,"end_date":end_date}

    max_deaths = 0
    max_country = ""
    countries = getUniqueCountries()                        # Get a list of all the countries in the data set
    for country in countries:                               # Loop through each country            
        deaths = 0
        for row in db:                                      # Loop through each row in the data set
            if country != row[2]:                           # If the country doesn't match the current country, continue
                continue
            date = datetime.strptime(row[0], '%Y-%m-%d')    # Convert the date to a datetime object
            if date >= begin and date <= end:               # If the date is within the given range, add the number of deaths to the total
                deaths += int(row[6])
        if deaths > max_deaths:                              # If the number of deaths is greater than the current max, update the max
            max_deaths = deaths
            max_country = country

    return {"Max Deaths":max_deaths,"Country":max_country,"success":True,"message":"Max Deaths by Country","size":1,"start_date":start_date,"end_date":end_date}

@app.get("/min_deaths/")
async def min_deaths(year:int = None):
    """
    ## This method returns the country with the least deaths and the number of deaths for that country.
    - If a year is specified, it will only pull the data from that year.
        - Valid years are 2020-2023.    
        - An empty year will list total deaths for the entire date range of the data set.

    - **Params:**
        - year (optional):int The year to pull data from.
    - **Returns:**
        - The country with the most deaths and the number of deaths for that country.

    #### Example 1:
    [https://localhost:5000/min_deaths/year=2021](https://localhost:5000/min_deaths/year=2021)

    #### Response 1:
    {
        "Min Deaths": 0,
        "Country": "American Samoa",
        "success": true,
        "message": "Min Deaths by Country",
        "size": 1,
        "year": 2021
    }
    """
    min_deaths = float('inf')                               # Set the min deaths to infinity       
    min_country = ""
    countries = getUniqueCountries()                        # Get a list of all the countries in the data set
    for country in countries:                               # Loop through each country    
        if year != None:                                    # If a year is specified, get the deaths for that year
            deaths = await deaths_by_country(country,year)
        else:                                               # If no year is specified, get the total deaths for the entire data set
            deaths = await deaths_by_country(country)
        deaths = deaths["Deaths by Country"][country]       # Get the number of deaths for the current country
        if deaths < min_deaths:                             # If the number of deaths is less than the current min, update the min
            min_deaths = deaths
            min_country = country

    return {"Min Deaths":min_deaths,"Country":min_country,"success":True,"message":"Min Deaths by Country","size":1,"year":year}

@app.get("/min_deaths_date_range/")
async def min_deaths_date_range(start_date:str = '2020-01-01', end_date:str = '2023-06-21'):
    """
    ## This method returns the country with the least deaths and the number of deaths for that country during the given date range.
    - If a start date is specified, it will only pull the data from after that date.
        - If no start date is specified, it will default to 2020-01-01.
        - Valid dates are 2020-01-01 to 2023-06-21.
    - If an end date is specified, it will only pull the data from before that date.
        - If no end date is specified, it will default to 2023-06-21.
        - Valid dates are 2020-01-01 to 2023-06-21.

    - **Params:**
        - start_date (optional):str in the format YYYY-MM-DD. The start date to pull data from.
        - end_date (optional):str in the format YYYY-MM-DD. The end date to pull data from.
    - **Returns:**
        - The country with the least deaths and the number of deaths for that country during the given date range.
        - If multiple countries have the same number of deaths, the first country alphabetically will be returned.

    #### Example 1:
    [https://localhost:5000/min_deaths_date_range/?start_date=2021-06-15&end_date=2021-08-15](https://localhost:5000/min_deaths_date_range/?start_date=2021-06-15&end_date=2021-08-15)
    
    #### Response 1:
    {
        "Min Deaths": 0,
        "Country": "American Samoa",
        "success": true,
        "message": "Min Deaths by Country",
        "size": 1,
        "start_date": "2021-06-15",
        "end_date": "2021-08-15"
    }

    """
    begin = datetime.strptime(start_date, '%Y-%m-%d')           # Convert the start date to a datetime object
    end = datetime.strptime(end_date, '%Y-%m-%d')               # Convert the end date to a datetime object
    min_deaths = float('inf')                                   # Set the min deaths to infinity
    min_country = ""
    countries = getUniqueCountries()                            # Get a list of all the countries in the data set
    for country in countries:                                   # Loop through each country
        deaths = 0
        for row in db:                                          # Loop through each row in the data set
            if country != row[2]:                               # If the country doesn't match the current country, skip the row
                continue
            date = datetime.strptime(row[0], '%Y-%m-%d')        # Convert the date to a datetime object
            if date >= begin and date <= end:                   # If the date is within the given date range, add the number of deaths to the total
                deaths += int(row[6])
        if deaths < min_deaths:                                 # If the number of deaths is less than the current min, update the min
            min_deaths = deaths
            min_country = country

    return {"Min Deaths":min_deaths,"Country":min_country,"success":True,"message":"Min Deaths by Country","size":1,"start_date":start_date,"end_date":end_date}

@app.get("/avg_deaths/")
async def avg_deaths(year:int = None):
    """
    ## This method returns the average number of deaths per country.
    - If a year is specified, it will only pull the data from that year.
        - Valid years are 2020-2023.
        - An empty year will list total deaths for the entire date range of the data set.

    - **Params:**
        - year (optional):int The year to pull data from.
    - **Returns:**
        - The average number of deaths per country.

    #### Example 1:
    [https://localhost:5000/avg_deaths/?year=2021](https://localhost:5000/avg_deaths/?year=2021)

    #### Response 1:
    {
       "Average Deaths": 14900.945147679326,
        "success": true,
        "message": "Average Deaths by Country",
        "size": 1,
        "year": 2021
    }
    """
    total_deaths = 0
    countries = getUniqueCountries()                            # Get a list of all the countries in the data set
    for country in countries:                                   # Loop through each country            
        if year != None:                                        # If a year is specified, get the deaths for that year
            deaths = await deaths_by_country(country,year)
        else:                                                   # If no year is specified, get the total deaths for the entire data set
            deaths = await deaths_by_country(country)
        deaths = deaths["Deaths by Country"][country]           # Get the number of deaths for the current country
        total_deaths += deaths                                  # Add the number of deaths to the total

    avg_deaths = total_deaths/len(countries)                    # Calculate the average number of deaths per country
    return {"Average Deaths":avg_deaths ,"success":True,"message":"Average Deaths by Country","size":1,"year":year}

@app.get("/avg_deaths_date_range/")
async def avg_deaths_date_range(start_date:str = '2020-01-01', end_date:str = '2023-06-21'):
    """
    ## This method returns the average number of deaths per country during the given date range.
    - If a start date is specified, it will only pull the data from after that date.
        - If no start date is specified, it will default to 2020-01-01.
        - Valid dates are 2020-01-01 to 2023-06-21.
    - If an end date is specified, it will only pull the data from before that date.
        - If no end date is specified, it will default to 2023-06-21.
        - Valid dates are 2020-01-01 to 2023-06-21.

    - **Params:**
        - start_date (optional):str in the format YYYY-MM-DD. The start date to pull data from.
        - end_date (optional):str in the format YYYY-MM-DD. The end date to pull data from.
    - **Returns:**
        - The average number of deaths per country during the given date range.

    #### Example 1:
    [https://localhost:5000/avg_deaths_date_range/?start_date=2021-06-15&end_date=2021-08-15](https://localhost:5000/avg_deaths_date_range/?start_date=2021-06-15&end_date=2021-08-15)

    #### Response 1:
    {
        "Average Deaths": 2304.9620253164558,
        "success": true,
        "message": "Average Deaths by Country",
        "size": 1,
        "start_date": "2021-06-15",
        "end_date": "2021-08-15"
    }
    """
    begin = datetime.strptime(start_date, '%Y-%m-%d')           # Convert the start date to a datetime object
    end = datetime.strptime(end_date, '%Y-%m-%d')               # Convert the end date to a datetime object
    total_deaths = 0
    countries = getUniqueCountries()                            # Get a list of all the countries in the data set
    for country in countries:                                   # Loop through each country            
        deaths = 0
        for row in db:                                          # Loop through each row in the data set
            if country != row[2]:                               # If the country doesn't match the current country, skip the row
                continue
            date = datetime.strptime(row[0], '%Y-%m-%d')        # Convert the date to a datetime object
            if date >= begin and date <= end:                   # If the date is within the given date range, add the number of deaths to the total
                deaths += int(row[6])                           
        total_deaths += deaths                                  # Add the number of deaths to the total

    avg_deaths = total_deaths/len(countries)                    # Calculate the average number of deaths per country
    return {"Average Deaths":avg_deaths,"success":True,"message":"Average Deaths by Country","size":1,"start_date":start_date,"end_date":end_date}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, log_level="debug", reload=True) #host="127.0.0.1"