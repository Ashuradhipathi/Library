import streamlit as st
import pymongo
import os
from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient('', serverSelectionTimeoutMS=60000)
db = client['HacksForU']
Roadmaps = db['Roadmaps']

# Streamlit app
st.title('Roadmaps')

def show_roadmaps():
    return Roadmaps.find()

def create_roadmap(Title, Description, Image, Link):
    new_roadmap = {
        "Title": Title,
        "Description": Description,
        "Image": Image,
        "Link": Link
    }
    Roadmaps.insert_one(new_roadmap)

# Display existing roadmaps
st.header('Existing Roadmaps')
roadmaps = show_roadmaps()
for roadmap in roadmaps:
    st.subheader(roadmap['Title'])
    st.write(roadmap['Description'])
    if roadmap['Image']:
        st.image(roadmap['Image'], use_column_width=True)
    st.write(f"Link: [{roadmap['Link']}](roadmap['Link'])")

# Create a new roadmap
st.header('Create New Roadmap')
Title = st.text_input('Title')
Description = st.text_area('Description')
Image = st.text_input('Image URL')
Link = st.text_input('Roadmap URL')
if st.button('Create Roadmap'):
    create_roadmap(Title, Description, Image, Link)
    st.success('Roadmap created successfully!')


