import streamlit as st
import os
from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient(os.getenv('mongostr'), serverSelectionTimeoutMS=60000)
db = client['HacksForU']
Fellowships = db['Fellowships']

def main():
    # Streamlit app
    st.title('Fellowships')
    # Display existing Fellowships
    st.header('Existing Fellowships')
    All_Fellowships = show_Fellowships()
    for Fellowship in All_Fellowships:
        st.subheader(Fellowship['Title'])
        st.write(Fellowship['Description'])
        if Fellowship['Image']:
            st.image(Fellowship['Image'], use_column_width=True)
        st.write(f"Link: [{Fellowship['Link']}](Fellowship['Link'])")

# Create a new Fellowship
    st.header('Create New Fellowship')
    Title = st.text_input('Title')
    Description = st.text_area('Description')
    Image = st.text_input('Image URL')
    Link = st.text_input('Fellowship URL')
    if st.button('Create Fellowship'):
        create_Fellowships(Title, Description, Image, Link)
        st.success('Fellowship created successfully!')

def show_Fellowships():
    return Fellowships.find()

def create_Fellowships(Title, Description, Image, Link):
    new_fellowship = {
        "Title": Title,
        "Description": Description,
        "Image": Image,
        "Link": Link
    }
    Fellowships.insert_one(new_fellowship)




if __name__ == "__main__":
    main()