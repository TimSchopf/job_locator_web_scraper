# job_locator_web_scraper
A web scraper that searches corporate websites for job postings related to specific keywords.  

I search for thesis offers in the area of Data Science/Machine Learning/AI near Stuttgart, Germany at the moment . Therefore I scrape the larger and well-known companies in this area, which always have a few thesis offers on their websites. The results are stored in a SQLite database with one table. Only new entries will be added to the database, in addition currently valid and new job offers will be marked. 

To get regular updates about job offers, I create an executable file from the `job_locator_web_scraper.py` script, which runs automatically on a daily basis using Windows Task Scheduler. 

The `job_locator_web_scraper.ipynb` Notebook is used to explore new websites and create the code for the `job_locator_web_scraper.py` script.  

## SQLite database:
##### Database name:  
`db_name = 'thesis_offers.db'`  

##### Table name:  
`db_table_name = 'thesis_offers'`  

##### Column names:  
`columns=['Title','Company','Location','Business_Unit','Description','Qualifications','ApplyURL','Release_Date','Valid','Interesting','New']`

* Title: title and short description
* Comany: company name
* Loction: location 
* Business_Unit: business unit
* Description: long and detailed description
* Qualifications: required qualifications
* ApplyURL: url link to job postig with the opportunity to apply for the job (PRIMARY KEY)
* Release_Date: release date 
* Valid: flag wheter the job posting is currently valid or not. 0 = not valid/not on website any more, 1 = valid/currently on website
* Interesting: flag wheter the job posting is interesting for me or not (will be manually flagged by me to train a recommender). 0 = not interesting, 1 = interesting
* New: flag whether the entry was added during the last run of the scraper. 0 = old entry that was already contained in db before the last run of the scraper, 1 = new entry that was added during the last run of the scraper  

## Usefull websites:

Create a rotating proxy crawler in Python 3 https://codelike.pro/create-a-crawler-with-rotating-ip-proxy-in-python/  
Advanced Scraping - Form Submission http://jonathansoma.com/lede/foundations-2017/classes/adv-scraping/advanced-scraping-form-submission/  
Web Scraping 201: finding the API http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/  
Build a Jobs Database using Indeed’s API https://medium.com/@alberto_moura/build-a-jobs-database-using-indeeds-api-8f95316be842  
Run Programs Automatically Using Windows Task Scheduler https://www.makeuseof.com/tag/how-to-automate-windows-programs-on-a-schedule/  
Making a Stand Alone Executable from a Python Script using PyInstaller https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263  
