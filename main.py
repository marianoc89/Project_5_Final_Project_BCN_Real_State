import joblib
import os
import streamlit as st
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
import numpy as np
from st_pages import Page, show_pages, add_page_title

########## Tab-Title ##########

st.set_page_config(
    page_title="BCN - Barcelona Real Estate",
    page_icon="🏘️",
)
########## Pages and sidebar ##########

st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.ibb.co/6rMFTd3/Logo-only.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Barcelona Real Estate";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("main.py", "ML App", "🏠"),
        Page("pages/dashboard.py", "Analytics", "📊"),
        Page("pages/about.py", "About", "💼"),
    ]
)

########## Boddy Logo ##########

st.markdown(
    '<center><img src="https://i.ibb.co/tMjd8Zq/Logo-2-removebg-preview-ps.png" style="width:549px;height:174px;"></center>',
    unsafe_allow_html=True
)
st.divider()

st.write("\n")

########## Boddy 1 ##########

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the model file
model_path = os.path.join(current_dir, 'models', 'habitaclia_final_model.sav')

# Load the model
model = joblib.load(model_path)

# Title and Description
st.header("Try :blue[for free] the best Machine Learning App for quoting properties in Barcelona")
st.write("\n")
st.divider()

st.subheader('Please, select the specifications of your property 🚀')
st.write("\n")
st.write("\n")

########## Features selection ##########

# Input Fields
rooms = st.slider('Rooms', 1, 10, 1)
bathrooms = st.slider('Bathrooms', 1, 10, 1)
size_m2 = st.slider('Size (m2)', 1, 1000, 1)
neighborhood = st.selectbox('Neighborhood', ['Baró de Viver',
'Can Baró', 'Can Peguera', 'Canyelles',
'Ciutat Meridiana',
'Diagonal Mar i el Front Marítim del Poblenou',
'el Barri Gòtic', 'el Baix Guinardó', 'el Besòs i el Maresme',
'el Bon Pastor',
"el Camp de l'Arpa del Clot", 'el Carmel',
"el Camp d'en Grassot i Gràcia Nova",
'el Clot', 'el Coll',
'el Congrés i els Indians', 'el Fort Pienc',
'el Guinardó', 'el Parc i la Llacuna del Poblenou',
'el Poble-sec', 'el Poblenou',
'el Putxet i el Farró', 'el Raval',
'el Turó de la Peira',
'Horta', 'Hostafrancs', 'Montbau',
"l'Antiga Esquerra de l'Eixample", 'la Barceloneta',
"la Dreta de l'Eixample", "la Font d'en Fargues",
"la Nova Esquerra de l'Eixample", 'la Prosperitat',
"la Vall d'Hebron", 'la Verneda i la Pau',
'la Bordeta', 'la Clota',
'la Font de la Guatlla', 'la Guineueta',
'la Marina de Port', 'la Marina del Prat Vermell',
'la Maternitat i Sant Ramon',
'la Sagrada Família', 'la Sagrera',
'la Salut', 'la Teixonera',
'la Trinitat Nova', 'la Trinitat Vella',
'la Vila de Gràcia', 'les Corts',
'la Vila Olímpica del Poblenou',
'les Roquetes', 'les Tres Torres',
'Navas', 'Pedralbes', 'Porta',
'Provençals del Poblenou', 'Sant Andreu',
'Sant Antoni', 'Sant Genís dels Agudells',
'Sant Gervasi - la Bonanova',
'Sant Martí de Provençals',
'Sant Pere, Santa Caterina i la Ribera', 'Sants',
'Sants - Badal', 'Sarrià', 'Torre Baró',
'Vallbona', 'Vallcarca i els Penitents',
'Vallvidrera, el Tibidabo i les Planes', 'Verdun',
'Vilapicina i la Torre Llobeta'])

property_type = st.selectbox('Property Type', [
    'APARTMENT','DUPLEX', 'FLAT', 'GROUND_FLOOR', 'HOUSE', 'LOFT', 'PAIRED_HOUSE', 'PENTHOUSE', 'SINGLE_FAMILY_SEMI_DETACHED',   
     'STUDIO', 'TRIPLEX'
])

########## DB and Model ##########

# Create a DataFrame for the user inputs
inputs_df = pd.DataFrame({'Rooms': [rooms],
                          'Bathrooms': [bathrooms],
                          'Size_m2': [size_m2],
                          'nom_barri': [neighborhood],
                          'Property_type': [property_type]})

# Loading the original DF before encoding
df_hab = pd.read_csv('data/final_data/habitaclia_bcn_all_data_combined_20230623_with_districts.csv', encoding='utf-8-sig')
df_hab.drop(columns=['ID', 'Address', 'City', 'Neightbourhood', 'Links', 'Description','Date_Scraped', 'District', 'Price_€', 'Price_m2'], inplace=True)
df_new = pd.concat([df_hab, inputs_df], ignore_index=True)

# Encoding and Scaling
scaler = StandardScaler()
min_max_scaler = MinMaxScaler()
df_new = pd.get_dummies(df_new, columns=['nom_barri', 'Property_type'], dtype="int")
df_new["Rooms"] = scaler.fit_transform(df_new["Rooms"].values.reshape(-1, 1))
df_new["Bathrooms"] = scaler.fit_transform(df_new["Bathrooms"].values.reshape(-1, 1))
df_new["Size_m2"] = min_max_scaler.fit_transform(df_new["Size_m2"].values.reshape(-1, 1))
df_new = df_new.tail(1)

st.write("\n")
########## Boddy 2 ##########
st.subheader('Finally, click on the :red[**"Predict"**] button below 👇🏻 to get the live quotation for the property.')

# Make predictions using the encoded inputs
prediction = model.predict(df_new)
st.write("\n")
st.divider()

########## Prediction Button ##########

# Prediction
# Display the prediction result
col1, col2,col3, col4, col5 = st.columns(5)

with col3:
    bot = st.button(':red[**Predict**]')
    
if bot:
    st.subheader(f'Predicted Price per m2: € {round(prediction[0],2)}')

########## Bottom ##########

st.divider()

st.markdown(
    '<center><img src="https://www.lavanguardia.com/files/image_948_465/files/fp/uploads/2023/07/03/64a2779743850.r_d.1273-473-4554.jpeg" style="width:720px;height:300px;"></center>',
    unsafe_allow_html=True
)