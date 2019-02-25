# crawl
crawling website using packages beautifulsoup and webdriver  

it is developed for user who want to get infomation of certain website(randered by js).  
Before runnung this file, please download `chrome driver` in [here](http://chromedriver.chromium.org/downloads) with same directory.

This python file consists of 2 functions. 1. `get_link`, 2. `get_info `  
First of all, extract links of products using webdriver.  
After that, extract infoamation of product(company, contact, email) using bs4 package. 

---
### How to use  
```$ scrap_company.py ```  
there are two **input values**  
- choose type of sort (5 types - 1:추천순, 2:인기순, 3:펀딩액순, 4:마감임박순, 5:최신순, 6:응원참여자순 )
- number of scroll
