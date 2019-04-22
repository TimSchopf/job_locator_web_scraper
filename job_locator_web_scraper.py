# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:39:56 2019

@author: Tim Schopf
"""

import undercover_request # custom module, install: pip install git+https://github.com/TimSchopf/undercover_request
import pandas as pd
import sqlite3
import os

# construct empty DataFrame, where scraped data gets temporary stored
data = pd.DataFrame(columns=['Title','Company','Location','Business_Unit','Description','Qualifications','ApplyURL','Release_Date','Valid','Interesting','New'])

# Scrape Daimler Career Website

# Daimler uses an API to send the data to the client.
# The Daimler Carrer Website itself is just a HTML template without data.
# Data and template render client side and are sent seperately to the client.
# In this case we must find the API URL that returns the raw data (the Daimler API sends JSON).
# The API URL already conatins the searched keywords, we don't need to append the daimler_keywords additionally
# searched keywords: thesis
daimler_keywords = {'_': 1555512030476} 
daimler_api_url = 'https://global-jobboard-api.daimler.com/v3/search/%7B%22LanguageCode%22%3A%22DE%22%2C%22ScoreThreshold%22%3A80%2C%22SearchParameters%22%3A%7B%22MatchedObjectDescriptor%22%3A%5B%22PositionID%22%2C%22PositionTitle%22%2C%22PositionURI%22%2C%22LogoURI%22%2C%22OrganizationName%22%2C%22Organization%22%2C%22Organization.MemberCode%22%2C%22ParentOrganization%22%2C%22PositionLocation.CityName%22%2C%22PositionLocation.Longitude%22%2C%22PositionLocation.Latitude%22%2C%22PositionIndustry.Name%22%2C%22JobCategory.Name%22%2C%22JobCategory.Code%22%2C%22CareerLevel.Name%22%2C%22CareerLevel.Code%22%2C%22Facet%3AParentOrganization%22%2C%22Facet%3APositionLocation.CityName%22%2C%22Facet%3APositionLocation.CountryName%22%2C%22PublicationStartDate%22%2C%22ParentOrganizationGenesisID%22%5D%2C%22FirstItem%22%3A0%2C%22CountItem%22%3A1000000%7D%2C%22SearchCriteria%22%3A%5B%7B%22CriterionName%22%3A%22PublicationLanguage.Code%22%2C%22CriterionValue%22%3A%5B%22DE%22%5D%7D%2C%7B%22CriterionName%22%3A%22PublicationChannel.Code%22%2C%22CriterionValue%22%3A%5B%2212%22%5D%7D%2C%7B%22CriterionName%22%3A%22CareerLevel.Code%22%2C%22CriterionValue%22%3A%5B%2240%22%5D%7D%5D%7D?_=1555512030476'
daimler_req = undercover_request.request(daimler_api_url, request_type='get')


# parse data
daimler_data = daimler_req.json()

# number of total hits for Daimler API
daimler_hits = daimler_data['SearchResult']['SearchResultCountAll']

# extract data from JSON and add it to DataFrame
for i in range(daimler_hits):
    # job title
    daimler_title = daimler_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']

    # company name
    daimler_company_logo_str = daimler_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['LogoURI'][0]
    daimler_company = 'Daimler AG: ' + daimler_company_logo_str[25:len(daimler_company_logo_str)-14]

    # location
    daimler_location = daimler_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['CityName']

    # business unit
    daimler_business_unit = daimler_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['JobCategory'][0]['Name']

    # no detailed job description and qualifications in Daimler JSON file
    daimler_description = float('NaN')
    daimler_qualifications = float('NaN')

    # url to detailed job descrition and application possibility
    daimler_applyURL = daimler_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionURI']

    # release date of job offer
    daimler_releaseDate = daimler_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PublicationStartDate']
    
    # append to 'data' DataFrame
    df = pd.DataFrame(data={'Title':[daimler_title],'Company':[daimler_company],'Location':[daimler_location],'Business_Unit':[daimler_business_unit],'Description':[daimler_description],'Qualifications':[daimler_qualifications],'ApplyURL':[daimler_applyURL],'Release_Date':[daimler_releaseDate],'Valid':[1],'Interesting':[float('NaN')],'New':[1]})
    data = data.append(df, ignore_index=True)

# Scrape Bosch Career Website
    
# Bosch also uses an API, returns JSON and expects JSON post parameter
# The Bosch API only delivers 9 results at a time, but more results can be loaded on the website via load more button

# searched keywords: thesis
bosch_keywords = {"from":0,"size":9,"sort":[{"releasedDate":{"order":"desc"}}],"query":{"query_string":{"query":"thesis*","default_operator":"and"}}}

bosch_req = undercover_request.request('https://ro-dyn-backend.bosch.com/c-corpweb-tc/es/bosch-ro-backend*/ro_bosch_backend__job_posting/_search', request_type='post', json=bosch_keywords)

# parse data
bosch_data = bosch_req.json()

# number of total hits for Bosch API
bosch_hits = bosch_data['hits']['total']

# set size of post request parameter to number of total hits and get all hits at once, not only 9
bosch_keywords_test = {"from":0,"size":bosch_hits,"sort":[{"releasedDate":{"order":"desc"}}],"query":{"query_string":{"query":"thesis*","default_operator":"and"}}}
bosch_req = undercover_request.request('https://ro-dyn-backend.bosch.com/c-corpweb-tc/es/bosch-ro-backend*/ro_bosch_backend__job_posting/_search', request_type='post', json=bosch_keywords_test)

# parse data
bosch_data = bosch_req.json()

# number of total hits for Bosch API
bosch_hits = bosch_data['hits']['total']

# extract data from JSON and add it to DataFrame
for i in range(bosch_hits):
    
    # job title 
    bosch_title = bosch_data['hits']['hits'][i]['_source']['name']

    # company name
    bosch_company = bosch_data['hits']['hits'][i]['_source']['company']['name']

    # loaction 
    bosch_city = bosch_data['hits']['hits'][i]['_source']['location']['city']
    bosch_country = bosch_data['hits']['hits'][i]['_source']['location']['country']
    bosch_postalCode = bosch_data['hits']['hits'][i]['_source']['location']['postalCode']
    bosch_region = bosch_data['hits']['hits'][i]['_source']['location']['region']
    bosch_location = str(bosch_postalCode) + ', ' + bosch_city + ', ' + bosch_country + ', ' + bosch_region

    # business unit
    bosch_business_unit = bosch_data['hits']['hits'][i]['_source']['function']['label']

    # detailed job description
    bosch_description = bosch_data['hits']['hits'][i]['_source']['jobAd']['sections']['jobDescription']['text']

    # job qualifications
    bosch_qualifications = bosch_data['hits']['hits'][i]['_source']['jobAd']['sections']['qualifications']['text']

    # url to detailed job descrition and application possibility
    bosch_applyURL = bosch_data['hits']['hits'][i]['_source']['applyUrl']

    # release date of job offer
    bosch_releaseDate = bosch_data['hits']['hits'][i]['_source']['releasedDate']
    
    # append to 'data' DataFrame
    df = pd.DataFrame(data={'Title':[bosch_title],'Company':[bosch_company],'Location':[bosch_location],'Business_Unit':[bosch_business_unit],'Description':[bosch_description],'Qualifications':[bosch_qualifications],'ApplyURL':[bosch_applyURL],'Release_Date':[bosch_releaseDate],'Valid':[1],'Interesting':[float('NaN')],'New':[1]})
    data = data.append(df, ignore_index=True)
    
# Scrape Porsche Career 

# Posrsche also uses an API
# The API URL already conatins the searched keywords, we don't need to append the porsche_keywords additionally
# The API sends 10 results at a time, we need to modify the 'CountItem' Parameter or the url string to get all results/hits
porsche_keywords = '{"LanguageCode":"DE","SearchParameters":{"FirstItem":1,"CountItem":10,"Sort":[{"Criterion":"PublicationStartDate","Direction":"DESC"}],"MatchedObjectDescriptor":["ID","PositionTitle","PositionURI","PositionLocation.CountryName","PositionLocation.CityName","PositionLocation.Longitude","PositionLocation.Latitude","PositionLocation.PostalCode","PositionLocation.StreetName","PositionLocation.BuildingNumber","PositionLocation.Distance","JobCategory.Name","PublicationStartDate","ParentOrganizationName","ParentOrganization","OrganizationShortName","CareerLevel.Name","JobSector.Name","PositionIndustry.Name","PublicationCode","PublicationChannel.Id"]},"SearchCriteria":[{"CriterionName":"PublicationChannel.Code","CriterionValue":["12"]},{"CriterionName":"CareerLevel.Code","CriterionValue":["6"]}]}'
porsche_api_url = 'https://api-jobs.porsche.com/search/?data=%7B%22LanguageCode%22%3A%22DE%22%2C%22SearchParameters%22%3A%7B%22FirstItem%22%3A1%2C%22CountItem%22%3A10%2C%22Sort%22%3A%5B%7B%22Criterion%22%3A%22PublicationStartDate%22%2C%22Direction%22%3A%22DESC%22%7D%5D%2C%22MatchedObjectDescriptor%22%3A%5B%22ID%22%2C%22PositionTitle%22%2C%22PositionURI%22%2C%22PositionLocation.CountryName%22%2C%22PositionLocation.CityName%22%2C%22PositionLocation.Longitude%22%2C%22PositionLocation.Latitude%22%2C%22PositionLocation.PostalCode%22%2C%22PositionLocation.StreetName%22%2C%22PositionLocation.BuildingNumber%22%2C%22PositionLocation.Distance%22%2C%22JobCategory.Name%22%2C%22PublicationStartDate%22%2C%22ParentOrganizationName%22%2C%22ParentOrganization%22%2C%22OrganizationShortName%22%2C%22CareerLevel.Name%22%2C%22JobSector.Name%22%2C%22PositionIndustry.Name%22%2C%22PublicationCode%22%2C%22PublicationChannel.Id%22%5D%7D%2C%22SearchCriteria%22%3A%5B%7B%22CriterionName%22%3A%22PublicationChannel.Code%22%2C%22CriterionValue%22%3A%5B%2212%22%5D%7D%2C%7B%22CriterionName%22%3A%22CareerLevel.Code%22%2C%22CriterionValue%22%3A%5B%226%22%5D%7D%5D%7D'
porsche_req = undercover_request.request(porsche_api_url, request_type='get')

# parse data
porsche_data = porsche_req.json()

# total number of hits from Porsche API
porsche_hits = porsche_data['SearchResult']['SearchResultCountAll']

# modify API url string to get all search results at once
porsche_api_url = porsche_api_url[0:145] + str(porsche_hits) + porsche_api_url[147:len(porsche_api_url)]

porsche_req = undercover_request.request(url=porsche_api_url, request_type='get')

# parse data
porsche_data = porsche_req.json()

# total number of hits from Porsche API
porsche_hits = porsche_data['SearchResult']['SearchResultCountAll']

# extract data from JSON and add it to DataFrame
for i in range(porsche_hits):

    # job title
    porsche_title = porsche_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']

    # company name
    porsche_company = porsche_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['ParentOrganizationName']

    # location
    porsche_city = porsche_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['CityName']
    porsche_country = porsche_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['CountryName']
    porsche_location = porsche_city + ', ' + porsche_country

    #business unit 
    porsche_business_unit = porsche_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['JobCategory'][0]['Name']

    # no detailed job description and qualifications in Porsche JSON file
    porsche_description = float('NaN')
    porsche_qualifications = float('NaN')

    # url to detailed job descrition and application possibility
    porsche_applyURL = porsche_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionURI']

    # release date of job offer
    porsche_releaseDate = porsche_data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PublicationStartDate']
    
    # append to 'data' DataFrame
    df = pd.DataFrame(data={'Title':[porsche_title],'Company':[porsche_company],'Location':[porsche_location],'Business_Unit':[porsche_business_unit],'Description':[porsche_description],'Qualifications':[porsche_qualifications],'ApplyURL':[porsche_applyURL],'Release_Date':[porsche_releaseDate],'Valid':[1],'Interesting':[float('NaN')],'New':[1]})
    data = data.append(df, ignore_index=True)

# Store Scraped results in SQLite database

# save 'data' DataFrame to persistent sqlite db 

db_name = 'thesis_offers.db'
db_table_name = 'thesis_offers'

# if db does not exist, create new db
if not os.path.exists('./' + db_name):
    conn = sqlite3.connect(db_name)
    data.to_sql(name=db_table_name, con=conn, index=False)
    
# if db exists, write only new elements in db (which are not already in db) and check which job offer elements are currently valid
else:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # set all Valids in db to 0
    notValid = 0
    Valid = 1
    c.execute('UPDATE '+db_table_name+' SET Valid = ? WHERE Valid != ?', (notValid, notValid))
    
    # set all New values in db to 0
    c.execute('UPDATE '+db_table_name+' SET New = ? WHERE New != ?', (0, 0))
    for i in range (data.shape[0]):

        # use ApplyURL as PRIMARY KEY
        t = (data['ApplyURL'][i],)
        c.execute('SELECT * FROM thesis_offers WHERE ApplyURL=?', t)
        df = data.iloc[i]

        # insert row of 'data' DataFrame if it is not in db
        if len(c.fetchall()) == 0:    
            insert = [(df['ApplyURL'],df['Business_Unit'],df['Company'],df['Description'],df['Interesting'],df['Location'],df['Qualifications'],df['Release_Date'],df['Title'],df['Valid']),]
            c.executemany('INSERT INTO '+db_table_name+' VALUES (?,?,?,?,?,?,?,?,?,?)', insert)

        # set db Valid value to 1 if element is currently in 'data' DataFrame
        else:
            c.execute('UPDATE '+db_table_name+' SET Valid = ? WHERE ApplyURL=?', (Valid, df['ApplyURL']))

    # save db changes
    conn.commit()

# close db connection    
conn.close()
print('database updates finished')