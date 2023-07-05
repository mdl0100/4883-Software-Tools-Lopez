# Marcos Lopez
## A08 - API Project Report

### Summary
As stated by Dr. Griffin in class, this project would have a decent amount of copy and pasting from the examples that he laid out in his assignment. Many of the API routes were as simple to build as changing the which index in the row of the `.csv` file was being used, or changing from the country column to the region column. 

However, there were many roadblocks and challenges to overcome in implementing this API. Below I will discuss some of those challenges.

### Aggregate Routes
When starting to put together the route `/max_deaths/`, I knew that I wanted to use the provided function `getUniqueCountries()`, because we needed to loop through the each country.

 I thought after calling this function I would loop through the list and use the previously defined function `deaths_by_country(country, year)` that was made for the route `/deaths_by_country/`, but I kept getting and error when trying to retrieve data from there. 

There error stated that a coroutine processes was not subscriptable, and I was unsure what that meant and how to fix it. After some time, I was able to get it down to the fact that `deaths_by_country(country, year)` is an *asyncronous* function, and all I needed to do was place  `await`  in front of its call to get the actual data I was going for. It does noticeably increase the run time whenever I use the await function. That's something that I'd try to speed up if I return to this project.

### Date ranges
There were two routes that needed to have a range of dates to consider. With year it was easier, because you only needed to match the year, and we could find that at the beginning of each row. 

To do the date ranges, it was necessary to convert the year-month-day entry at the beginning of each row to a dateObject through date time. Once this was done it wasn't too difficult to go through the dates with simple comparisons, but understanding out the datetime module worked took a little time. 

### Comments
There are so many comments explaining the functions and API routes in the `main.py` file. They are often almost identical, and it was tedious to change the very small parts for each of the 14 routes that are in this API. I used CoPilot to help fill out the more mundane, repetitive comments which made that task easier. 

`main.py` is over 800 lines long, and I'm positive that 650+ of those lines are blank or comments.