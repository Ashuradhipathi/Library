import streamlit as st
import pymongo
import os
from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient('', serverSelectionTimeoutMS=60000)
db = client['HacksForU']
FreeStuff = db['FreeStuff']

# Streamlit app
st.title('FreeStuff')

def show_FreeStuff():
    return FreeStuff.find()

def create_FreeStuff(Title, Description, Image, Link):
    new_resource = {
        "Title": Title,
        "Description": Description,
        "Image": Image,
        "Link": Link
    }
    FreeStuff.insert_one(new_resource)

# Display existing FreeStuff
st.header('Existing FreeStuff')
Resources = show_FreeStuff()
for resource in Resources:
    st.subheader(resource['Title'])
    st.write(resource['Description'])
    if resource['Image']:
        st.image(resource['Image'], use_column_width=True)
    st.write(f"Link: [{resource['Link']}](resource['Link'])")

# Create a new resource
st.header('Create New resource')
Title = st.text_input('Title')
Description = st.text_area('Description')
Image = st.text_input('Image URL')
Link = st.text_input('resource URL')
if st.button('Create resource'):
    create_FreeStuff(Title, Description, Image, Link)
    st.success('resource created successfully!')


