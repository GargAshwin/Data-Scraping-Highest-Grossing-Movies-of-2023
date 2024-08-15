from bs4 import BeautifulSoup
import requests
import pandas as pd

website = 'https://www.boxofficemojo.com/year/world/2023/'
request = requests.get(website) #allow us to send requests to the website
text = request.text #get website elements
soup = BeautifulSoup(text, 'lxml') #get all the HTML code for the website for data scraping

#get HTML of the data table of the data in question
data_chart = soup.find('table', class_='a-bordered a-horizontal-stripes a-size-base a-span12 mojo-body-table mojo-table-annotated')
world_titles = data_chart.find_all('th') #all the data column titles are in blocks with the tags <th> ...... <\th>

list_titles = [title.text.strip() for title in world_titles] #put those titles in world_titles into a list
data_frame = pd.DataFrame(columns = list_titles) #make a data frame with those data titles
data_rows = data_chart.find_all('tr') #all the actual data is in blocks with the tags <tr> ..... <\tr> in the table chart

for row in data_rows[1:]: #for each row in thw websites data table starting at row index 1 (row index 0 are the world titles, which we already have)
    data_elements = [] #create an empty list to which we will add all the individual data of each movie
    for data in row: #for every data piece in the row
        if(data.text == '-'): #if the data is a '-', then there is no data for this movie in this specific column of data
            data_elements.append('')
        else: #otherwise add the data to the data_elements list
            data_elements.append(data.text)
    data_frame.loc[len(data_frame)] = data_elements #add the data_elements list to the data frame
    #repeat the process for ALL rows in the table

#When we have all of our data in the data frame, we will use the .to_csv() function to export the data to an Excel sheet or Numbers sheet for further data analysis/graphing
#to the desktop
data_frame.to_csv(r'/Users/ashwingarg/Desktop/TopMoviesOf2023Data.csv', index=False)