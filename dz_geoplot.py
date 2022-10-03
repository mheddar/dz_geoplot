import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import json
import requests
import os


st.sidebar.title('DZ Geographical Plotting')
st.sidebar.subheader("Designed by: Mohamed Heddar")
st.sidebar.markdown("Ref: [GeoJson files](https://github.com/fr33dz/Algeria-geojson)")

@st.cache
def load_data():
    directory = "Algeria-geojson/"
    with open(os.path.join(directory, 'all-wilayas.geojson'), encoding="utf8") as f:
        d = json.load(f)

    total_df = pd.read_csv("Algeria-geojson/wilaya_naming.csv", encoding= "latin")
    return d, total_df

@st.cache
def convert_df(df):
   return df.to_csv(index = False).encode('latin')

d, total_df = load_data()

csv = convert_df(total_df)

st.sidebar.download_button(
   "Press to Download",
   csv,
   "wilaya_table.csv",
   "text/csv",
   key='download-csv'
)
input_text = st.sidebar.text_input('Label', 'Succes Rate of BAC2015')
ctitle = "Succes Rate"

if input_text:
    ctitle = input_text

uploaded_file = st.sidebar.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    total_df = pd.read_csv(uploaded_file, encoding= "latin")

fig = px.choropleth_mapbox(
    total_df, geojson=d, locations='Wilaya', color='Value',
    color_continuous_scale="bupu",
    # range_color=(0, 12),
    featureidkey = "properties.name",
    mapbox_style="carto-positron",
    zoom=4.2, center = {"lat": 28.6 , "lon": 1.6666663},
    opacity=0.8,
    height = 600,
    labels={'Value':ctitle},
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)