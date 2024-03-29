import streamlit as st
import pymongo
import os
from pymongo import MongoClient

client = MongoClient(os.getenv('mongostr'), serverSelectionTimeoutMS=60000)
db = client['HacksForU']
Courses = db['Courses']
def main():
# Streamlit app
    st.title('Courses')

    # Display existing FreeStuff
    st.header('Existing Courses')
    All_courses = show_Courses()
    for course in All_courses:
        st.subheader(course['Title'])
        st.write(course['Description'])
        if course['Image']:
            st.image(course['Image'], use_column_width=True)
        st.write(f"Link: [{course['Link']}](resource['Link'])")

# Create a new resource
    st.header('Create New resource')
    Title = st.text_input('Title')
    Description = st.text_area('Description')
    Image = st.text_input('Image URL')
    Link = st.text_input('resource URL')
    if st.button('Create resource'):
        create_Courses(Title, Description, Image, Link)
        st.success('resource created successfully!')

def show_Courses():
    return Courses.find()

def create_Courses(Title, Description, Image, Link):
    new_course = {
        "Title": Title,
        "Description": Description,
        "Image": Image,
        "Link": Link
    }
    Courses.insert_one(new_course)
    
if __name__ == "__main__":
    main()


