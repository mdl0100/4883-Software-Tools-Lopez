# A08 - Faswt API with Covid Data
# Marcos Lopez


## Description
Create a RESTful API using FastAPI that provides access to COVID-19 data. The API will fetch the data from a publicly available data source and expose endpoints to retrieve various statistics related to COVID-19 cases.

The assigment will accomplish the following goals:
- It will use FastAPI to build the API 
- The API has the endpoints listed below
- Proper API documentation using FastAPI's built-in support for OpenAPI (Swagger UI) is implemented. 
  - This means functions are commented with markdown syntax for readability.

## Folder Contents
  
|   #   | File                                 | Description                             |
| :---: | ------------------------------------ | :-------------------------------------- |
|  01   | [data.csv](data.csv)                 | COVID data set that we are pulling from |
|  02   | [main.py](main.py)                   | File to run for API                     |
|  03   | [requirements.txt](requirements.txt) | Packages used in virtual environment    |

### Deliverables
- [X] Create a folder called `A08` to place all of the assignment files in.
- [X] Include Python code for the FastAPI application and any additional files.
- [X] A README.md Document explaining the API endpionts and their usage
- [X] A brief report summarizing the implementation process, challenges faced, and any additional functionalities you may have added. 
- [X] Any instructions should be included in your readme (how to run your code)
  
### Instructions
1. Install the packages in the [requirements.txt](requirements.txt) file

2. Run `./main.py` to start the API. The API will be hosted on `localhost:5000`. The API can be accessed through a browser. 
     - If program gives error: Error loading ASGI app. Could not import module "api" 
  
        then run command: 
    `uvicorn main:app --reload --port 5000`

3. Use the following API routes to access the data you are interested in.


### API Routes and Examples
Here is a list of the API Routes and how they can be accessed:
<details>
<summary>/countries/</summary>
  This method returns a list of unique countries in the data set.
  
  - **Params:**
      - None
  
  - **Returns:**
      - A list of unique countries in the data set.

  ### Example 1:
  [https://localhost:5000/countires/](https://localhost:5000/countires/)

  ### Response 1:

`  {
      "countries": [
          "Afghanistan",
          "Albania",
          ...
          "Zimbabwe"
      ]
  }    ` 
</details>

<details>
<summary>/whos/</summary>
 This method returns a list of unique WHO regions in the data set.

  - **Params:**
      - None
  
  - **Returns:**
      - A list of unique WHO regions in the data set.

  #### Example 1:
  [https://localhost:5000/whos/](https://localhost:5000/whos/)

  #### Response 1:
`  {
      "whos": [
          "AFRO",
          "AMRO",
          ...
          "WPRO"
      ]
  }`
  
  #### Note:
  These are the WHO regions and their corresponding names:
  - AFRO  -> "Africa"
  - AMRO  -> "Region of the Americas"
  - SEARO -> "South-East Asian Region"
  - EURO  -> "European Region"
  - EMRO  -> "Eastern Mediterranean Region"
  - WPRO  -> "Western Pacific Region"
</details>

<details>
<summary>/cases/</summary>
This method returns a list total cases in the world by year and also the total number of cases.

- **Params:**
    - None
- **Returns:**
    - A list total cases in the world by year and also the total number of cases.

#### Example 1:
[https://localhost:5000/cases/](https://localhost:5000/cases/)

#### Response 1:
`{
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
}`
</details>

<details>
  <summary>/cases_by_country/</summary>
This method returns the number of cases by country.

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
`{
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
}`

#### Example 2:
[https://localhost:5050/cases_by_country/?country=Brazil](https://localhost:5050/cases_by_country/?country=Brazil)

#### Response 2:

`{
    "Cases By Country": {
        "Brazil": 37639324
    },
"success": true,
"message": "Cases by Country",
"size": 1,
"country": "Brazil",
"year": null
}`

#### Example 3:
[http://localhost:5000/cases_by_country/?country=Brazil&year=2021](http://localhost:5000/cases_by_country/?country=Brazil&year=2021)

#### Response 3:

`{
    "Cases By Country": {
        "Brazil": 14700283,
    },
"success": true,
"message": "Cases by Country",
"size": 1,
"country": "Brazil",
"year": 2021
}`
</details>

<details>
  <summary>/cases_by_region/</summary>
This method returns the number of cases by region.

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
`{
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
}`
</details>

<details>
  <summary>/deaths/</summary>
This method returns the number of deaths by year for the whole world.

**Params**
- None
  
**Returns**
- A dictionary of deaths by year.

#### Example 1:
[https://localhost:5000/deaths/](https://localhost:5000/deaths/)

#### Response 1:
`{
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
}`
</details>

<details>
  <summary>/deaths_by_country/</summary>
This method returns the number of deaths by country.

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
`{
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
}`

#### Example 2:
[https://localhost:5050/deaths_by_country/?country=Brazil](https://localhost:5050/deaths_by_country/?country=Brazil)

#### Response 2:
`{
  "Deaths by Country": {
      "Brazil": 703399
  },
  "success": true,
  "message": "Deaths by Country",
  "size": 1,
  "country": "Brazil",
  "year": null
}`

#### Example 3:
[https://localhost:5050/deaths_by_country/?country=Brazil&year=2021](https://localhost:5050/deaths_by_country/?country=Brazil&year=2021)

#### Response 3:
`{
  "Deaths by Country": {
      "Brazil": 426136
  },
  "success": true,
  "message": "Deaths by Country",
  "size": 1,
  "country": "Brazil",
  "year": 2021
}`
</details>

<details>
  <summary>/deaths_by_region/</summary>
 This method returns the number of deaths by region.

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

  `{
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
`
  #### Example 2:
  [https://localhost:5050/deaths_by_region/?region=EMRO](https://localhost:5050/deaths_by_region/?region=EMRO)

  #### Response 2:
 ` {
      "Deaths By Region": {
          "EMRO": 351329
      },
  "success": true,
  "message": "Deaths by Region",
  "size": 1,
  "year": null
  }`

  #### Example 3:
  [https://localhost:5050/deaths_by_region/?region=EMRO&year=2021](https://localhost:5050/deaths_by_region/?region=EMRO&year=2021)

  #### Response 3:
  `{
      "Deaths By Region": {
          "EMRO": 195342
      },
  "success": true,
  "message": "Deaths by Region",
  "size": 1,
  "year": 2021
  }`

</details>

<details>
  <summary>/max_deaths/</summary>
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
`  {
      "Max Deaths": 1127152,
      "Country": "United States of America",
      "success": true,
      "message": "Max Deaths by Country",
      "size": 1,
      "year": null
  }`
  
  #### Example 2:
  [https://localhost:5050/max_deaths/?year=2021](https://localhost:5050/max_deaths/?year=2021)

  #### Response 2:
`  {
      "Max Deaths": 467051,
      "Country": "United States of America",
      "success": true,
      "message": "Max Deaths by Country",
      "size": 1,
      "year": 2021
  }`
</details>

<details>
  <summary>/max_deaths_date_range/</summary>
 This method returns the country with the most deaths and the number of deaths for that country during the given date range.

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
`  {
      "Max Deaths": 81590,
      "Country": "Brazil",
      "success": true,
      "message": "Max Deaths by Country",
      "size": 1,
      "start_date": "2021-06-15",
      "end_date": "2021-08-15"
  }`
</details>

<details>
  <summary>/min_deaths/</summary>
  This method returns the country with the least deaths and the number of deaths for that country.

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
` {
      "Min Deaths": 0,
      "Country": "American Samoa",
      "success": true,
      "message": "Min Deaths by Country",
      "size": 1,
      "year": 2021
  }`
</details>

<details>
  <summary>/avg_deaths/</summary>
This method returns the country with the least deaths and the number of deaths for that country during the given date range.

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
`  {
      "Min Deaths": 0,
      "Country": "American Samoa",
      "success": true,
      "message": "Min Deaths by Country",
      "size": 1,
      "start_date": "2021-06-15",
      "end_date": "2021-08-15"
  }`
</details>

<details>
  <summary>/avg_deaths/</summary>
 This method returns the average number of deaths per country.
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
  ` {
      "Average Deaths": 14900.945147679326,
      "success": true,
      "message": "Average Deaths by Country",
      "size": 1,
      "year": 2021
  }`
</details>

<details>
  <summary>/avg_deaths_date_rage</summary>
  This method returns the average number of deaths per country during the given date range.

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
`{
    "Average Deaths": 2304.9620253164558,
    "success": true,
    "message": "Average Deaths by Country",
    "size": 1,
    "start_date": "2021-06-15",
    "end_date": "2021-08-15"
}`
</details>

