import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from datetime import date
import random
import time
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import glob
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from geopy.geocoders import Nominatim


#List of the different features needed to be scrapped
id_ = []
dir_ = []
price= []
room = []
bathroom = []
mt2 = []
price_m2 = []
prop_type = []
seller_type = []
city = []
neightbourhood = []
link = []
description = []

#Dictionary containing all the different values from previous list of features with it's corresponding Column name.
web_dict = {
        'ID': id_,
        'Address': dir_,
        'Price_€': price,
        'Rooms': room,
        'Bathrooms': bathroom,
        'Size_m2': mt2,
        'Price_m2': price_m2,
        'Property_type': prop_type,
        'Seller_type': seller_type,
        'City': city,
        'Neightbourhood': neightbourhood,
        'Links': link,
        'Description': description
    }

def habitaclia_scrape_v4(from_,to_):
    driver = uc.Chrome()
    # iterating in a range from_ and to_ which will be determined by the user (how many pages to be scraped from habitaclia)
    for x in range(from_, to_):
        url = f'https://www.habitaclia.com/viviendas-barcelona-{x}.htm?hab=1&ban=1'
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(random.randint(5, 16))

        # Iterating on the same dir_data element to obtain all the information for each post        
        dir_data = soup.find_all('article', attrs={'class': 'js-list-item list-item-container js-item-with-link gtmproductclick'})
        for i in dir_data:
            try:
                id_value = i.get('id')
                dir_value = i.find('div', attrs={'class': 'list-item'}).find('h3', class_='list-item-title').text.strip()
                price_value = int(i.find('div', attrs={'class': 'list-item'}).find('span', class_='font-2').text.strip().split('€')[0].strip().replace('.', ''))
                room_value = int(i.find('div', attrs={'class': 'list-item'}).find('p', class_='list-item-feature').text.strip().split('\n')[1].strip().split('-')[1].strip().split(' ')[0])
                bathroom_value = int(i.find('div', attrs={'class': 'list-item'}).find('p', class_='list-item-feature').text.strip().split('\n')[1].strip().split('-')[2].strip().split(' ')[0])
                mt2_value = i.find('div', attrs={'class': 'list-item'}).find('p', class_='list-item-feature').text.strip().split('\n')[0].split('m2')[0]
                price_m2_value = int(i.find('div', attrs={'class': 'list-item'}).find('p', class_='list-item-feature').text.strip().split('\n')[1].strip().split('-')[3].strip().split('€')[0].replace('.', ''))
                prop_type_value = i.get('data-propertysubtype')
                seller_type_value = i.get('data-selltype')
                city_value = i.find('div', attrs={'class': 'list-item'}).find('p', class_='list-item-location').text.strip().split('\n')[0].split(' - ')[0]
                neightbourhood_value = i.find('div', attrs={'class': 'list-item'}).find('p', class_='list-item-location').text.strip().split('\n')[0].split(' - ')[1]
                link_value = i.get('data-href')
                description_value = i.find('div', attrs={'class': 'list-item'}).find('p', class_='list-item-description').text.strip()

                # Append the values to the lists only after all attributes have been successfully obtained
                id_.append(id_value)
                dir_.append(dir_value)
                price.append(price_value)
                room.append(room_value)
                bathroom.append(bathroom_value)
                mt2.append(mt2_value)
                price_m2.append(price_m2_value)
                prop_type.append(prop_type_value)
                seller_type.append(seller_type_value)
                city.append(city_value)
                neightbourhood.append(neightbourhood_value)
                link.append(link_value)
                description.append(description_value)
            except AttributeError or IndexError:
                # Skip appending values and continue to the next iteration
                continue
    
    #Creating a DataFrame from the Dictionary
    df = pd.DataFrame(web_dict)
    #Creating a column with the date scraped
    df['Date_Scraped'] = pd.to_datetime('today')
    #Normalizing the date to have only date without time
    df.Date_Scraped = pd.to_datetime(df.Date_Scraped).dt.normalize()
    #Drop Column Seller_type as it is always the same and does not ad value
    df.drop(columns='Seller_type', inplace=True)
    #Creating a today function to save the file with the date
    today = str(pd.to_datetime('today'))[:10].replace('-','')
    #Saving the dataframe into a csv file
    df.to_csv(f'../data/habitaclia/habitaclia_bcn_scrape_{today}.csv', encoding='utf-8-sig', index=False)
    return df

#Creating a funciton to scrape the ayuntamiento of Barcelona website with the historical Data from Barcelona and returning a DF
def ayuntamiento_scrape():
    url_ayuntamiento = 'https://ajuntament.barcelona.cat/estadistica/angles/Estadistiques_per_temes/Habitatge_i_mercat_immobiliari/Mercat_immobiliari/Preu_oferta_habitatge_segona_ma/evo/t2mab.htm'
    req2 = requests.get(url_ayuntamiento)
    soup2 = BeautifulSoup(req2.content, 'lxml')
    table = soup2.find_all('table')[0]
    #Slicing upto 20 results as requested in lab:
    df_a = pd.read_html(table.prettify())[0]
    #Reducing the number of col (excluding 10 and 15 that does not have data)
    df_a = df_a[[3,4,5,6,7,8,9,11,12,13,14]]
    #Converting row 4 as headers
    df_a.columns = df_a.iloc[4]
    df_a = df_a[9:82]
    df_a.rename(columns={"Dto. Barrios":"Barrios"}, inplace=True)
    df_a['Barrios'] = df_a['Barrios'].str.split('.').str[1].str.strip().str.capitalize()
    #Replacing vaolues to int
    for i in range(2013,2023):
        df_a[f'{i}'] = df_a[f'{i}'].str.replace('.','').replace('-',0).astype(int)
    #Saving the dataframe into a csv file
    df_a.to_csv(f'../data/ayuntamiento_scrape_with_BarcelonaCiutat_Barris.csv', encoding='utf-8-sig', index=False)
    return df_a

#Creating a funciton to scrape the historical euribor rate from Idealista website and returning a DF
def euribor_historico():
    driver2 = uc.Chrome()
    url2 = 'https://www.idealista.com/news/euribor/historico-diario/'
    driver2.get(url2)
    html2 = driver2.page_source
    soup2 = BeautifulSoup(html2, 'lxml')

    #Finding the table       
    table = soup2.find_all('table')[0]
    #Creating the DF
    df_e = pd.read_html(table.prettify())[0]
    df_e['Valor'] = df_e['Valor'].str.replace(',','.').str.replace('%','').astype(float)
    #Normalizing the date in the datafram
    df_e.Fecha = pd.to_datetime(df_e.Fecha).dt.normalize()
    #Saving the dataframe
    df_e.to_csv(f'../data/idealista_euribor_monthly_until_june_2023.csv', encoding='utf-8-sig', index=False)
    return df_e

#Creating a funciton to combine all the data scraped from habitalica (if it was run more than 1 time) into 1 single DataFrame combined
def scrape_combine():
    # Define the file pattern
    file_pattern = 'habitaclia_*.csv'
    # Get the list of file paths matching the pattern
    file_paths = glob.glob(file_pattern)
    # Initialize an empty list to store DataFrames
    dfs = []
    # Iterate over each file path
    for file_path in file_paths:
    # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
    # Append the DataFrame to the list
        dfs.append(df)
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    #Delete duplicates where the ID is repeted (as the scraped was run multiple times)
    combined_df.drop_duplicates(subset='ID', inplace=True)
    # Reset the index
    combined_df.reset_index(drop=True, inplace=True)
    #Normalizing the date scraped as to avoid issues with the date
    combined_df.Date_Scraped = pd.to_datetime(combined_df.Date_Scraped).dt.normalize()
    today = str(pd.to_datetime('today'))[:10].replace('-','')
    #Saving the dataframe combined into 1 single csv with 
    combined_df.to_csv(f'../data/habitaclia_bcn_all_data_combined_{today}.csv', encoding='utf-8-sig', index=False)
    return combined_df


#Creating a funciton that standarizes and adds lat and long to neightborhood and districts data
def barrios_districtos():
    driver2 = uc.Chrome()
    url2 = 'https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-925a-fa5afdb1ed41/resource/576bc645-9481-4bc4-b8bf-f5972c20df3f/download'
    driver2.get(url2)
    #The data frame needs to be downloaded first - file needs to be downloaded into data folder
    df = pd.read_csv('../data/BarcelonaCiutat_Barris.csv', encoding='utf-8-sig')
    #Creating 1 df for Neightborhoods only
    df_barr = df.drop(columns=['codi_districte','codi_barri','geometria_etrs89','geometria_wgs84', 'nom_districte'])
    #Creating 1 df for Districts only
    df_districtos = df.drop(columns=['codi_districte','codi_barri','geometria_etrs89','geometria_wgs84', 'nom_barri'])
    df_districtos.drop_duplicates(inplace=True)
    # Create a geocoder instance
    geolocator = Nominatim(user_agent='my_geocoder')

    # Function to get latitude and longitude given a location string
    def get_lat_long(location):
        try:
            location = geolocator.geocode(location)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except:
            return None, None

    # Apply the function to the district column and create district_lat and district_long columns
    df_districtos['District_lat'], df_districtos['District_long'] = zip(*df_districtos['nom_districte'].map(get_lat_long))

    # Apply the function to the neighborhood column and create neighborhood_lat and neighborhood_long columns
    df_barr['Neighborhood_lat'], df_barr['Neighborhood_long'] = zip(*df_barr['nom_barri'].map(get_lat_long))
    #Saving the Barrios dataframe with Coordinates to csv file
    df_barr.to_csv(f'../data/BarcelonaCiutat_Barris_coordinates.csv', encoding='utf-8-sig', index=False)
    #Saving the Districts dataframe with Coordinates to csv file
    df_districtos.to_csv(f'../data/BarcelonaCiutat_Districtes_coordinates.csv', encoding='utf-8-sig', index=False)
    print('File successfully created')
    return

#Creating a funciton to add district and barrio name from ayuntamiento data
def habitaclia_barri_district():
    # Define the file pattern
    file_pattern = 'habitaclia_bcn_all_data_combined*.csv'
    # Get the list of file paths matching the pattern
    file_paths = glob.glob(file_pattern)
    # Initialize an empty list to store DataFrames
    dfs = []
    # Iterate over each file path
    for file_path in file_paths:
    # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
    # Append the DataFrame to the list
        dfs.append(df)
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    #Delete duplicates where the ID is repeted (as the scraped was run multiple times)
    combined_df.drop_duplicates(subset='ID', inplace=True)
    # Reset the index
    combined_df.reset_index(drop=True, inplace=True)
    #Normalizing the date scraped as to avoid issues with the date
    combined_df.Date_Scraped = pd.to_datetime(combined_df.Date_Scraped).dt.normalize()
    #creating a dataframe from the file downloaded from 'https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-925a-fa5afdb1ed41/resource/576bc645-9481-4bc4-b8bf-f5972c20df3f/download'
    df_barrios = pd.read_csv('../data/BarcelonaCiutat_Barris.csv', encoding='utf-8-sig')

    # Create empty lists to store the district, nom_barri, geometria_etrs89, and geometria_wgs84 values
    districts = []
    nom_barri_values = []

    # Iterate over each neighborhood in the combined_df dataframe
    for neighborhood in combined_df['Neightbourhood']:
        # Find the best match for the neighborhood in the df_barrios dataframe
        best_match = process.extractOne(neighborhood, df_barrios['nom_barri'])
        
        # Get the index of the best match
        index = best_match[2]
        
        # Get the corresponding district, nom_barri, geometria_etrs89, and geometria_wgs84 from the df_barrios dataframe using the index
        district = df_barrios.loc[index, 'nom_districte']
        nom_barri = df_barrios.loc[index, 'nom_barri']
        
        # Append the district, nom_barri, geometria_etrs89, and geometria_wgs84 to their respective lists
        districts.append(district)
        nom_barri_values.append(nom_barri)

    # Create a new column 'District' in the combined_df dataframe and assign the districts list to it
    combined_df['District'] = districts

    # Create a new column 'nom_barri' in the combined_df dataframe and assign the nom_barri_values list to it
    combined_df['nom_barri'] = nom_barri_values

    today = str(pd.to_datetime('today'))[:10].replace('-','')
    #Saving the dataframe combined into 1 single csv with 
    combined_df.to_csv(f'../data/habitaclia_bcn_all_data_combined_{today}_with_districts.csv', encoding='utf-8-sig', index=False)
    print('File successfully created')
    return


#Funciton to create a melt file from ayuntamiento data for prediction purposes
def ayuntamiento_melt():
    df_ayu=pd.read_csv(f'../data/final_data/ayuntamiento_scrape_with_BarcelonaCiutat_Barris.csv', encoding='utf-8-sig')
    # Reshape the dataframe
    df_new = pd.melt(df_ayu, id_vars='Barrios', var_name='Year', value_name='Price_m2')
    # Sort the dataframe by neighborhood and year
    df_new = df_new.sort_values(['Barrios', 'Year'])
    # Reset the index
    df_new = df_new.reset_index(drop=True)
    df_new.Year = df_new.Year.astype(int)
    df_new.to_csv(f'../data/ayuntamiento_scrape_with_BarcelonaCiutat_Barris_melt.csv', encoding='utf-8-sig', index=False)
    print('Melted file created succesfully')
    return