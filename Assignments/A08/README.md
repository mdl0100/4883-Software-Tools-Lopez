# A08 - Faswt API with Covid Data
# Marcos Lopez


## Description
Create a RESTful API using FastAPI that provides access to COVID-19 data. The API will fetch the data from a publicly available data source and expose endpoints to retrieve various statistics related to COVID-19 cases.

The assigment will accomplish the following goals:
- It will use FastAPI to build the API 
- The API has the endpoints listed below
- Errors are handled gracefully. 
  - For example, if a parameter that is passed in causes an error, simply return {'success':False} or return the parameters passed in as well {'success':False,'param1':value1,'param(n):value(n)}. This helps for debugging.
- Proper API documentation using FastAPI's built-in support for OpenAPI (Swagger UI) is implemented. 
  - This means functions are commented with markdown syntax for readability.

## Folder Contents
  
|   #   | File                 | Description                             |
| :---: | -------------------- | :-------------------------------------- |
|  01   | [data.csv](data.csv) | COVID data set that we are pulling from |

### Deliverables
- [X] Create a folder called `A08` to place all of the assignment files in.
- [ ] Include Python code for the FastAPI application and any additional files.
- [ ] A README.md Document explaining the API endpionts and their usage
  - [ ] if the functions are commented well, you could almost cut and past your readme.
- [ ] A brief report summarizing the implementation process, challenges faced, and any additional functionalities you may have added. 
- [ ] Any instructions should be included in your ream (how to run your code)
  
> Note: Ensure proper code organization, documentations, and adherence to best practices in software development.