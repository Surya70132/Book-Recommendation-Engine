import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import pickle
import random

book_similarity_df = pd.read_pickle('book_similarity_df.pkl')
filtered_df = pd.read_pickle('filtered_df.pkl')


# Function to display the top 50 books
def top_50_books():
    st.markdown('<h1 style="font-size: 20px; white-space: nowrap;">Top 50 Popular Books</h1>', unsafe_allow_html=True)

    # Load the DataFrame from the pickle file
    with open('popular.pkl', 'rb') as file:
        book_data = pd.read_pickle(file)

    # Get the top 50 records
    top_50 = book_data.head(50)

    # Split the records into three columns
    col1, col2, col3 = st.columns(3)

    # Iterate over each book in the top 50 records
    for i, book in top_50.iterrows():
        # Display book image
        col_num = i % 3  # Determine the column number based on the iteration index
        col = col1 if col_num == 0 else col2 if col_num == 1 else col3
        with col:
            st.image(book['Image-URL-M'], caption=book['Book-Title'], width=150)

            # Display book details
            st.write(f"Book-Title: {book['Book-Title']}")
            st.write(f"Book-Author: {book['Book-Author']}")
            st.write(f"Avg_Rating: {round(book['Avg_Rating'], 2)}")  # Format average rating to two decimal points
            # Add more details as needed

            # Add a separator between books
            st.write("---")


# Function to get book recommendations
def get_recommendation(book_name):

    filtered_df = pd.read_pickle('filtered_df.pkl')
    book_similarity_df = pd.read_pickle('book_similarity_df.pkl')


    # Taking the index of user_book_matrix and matching with book_similarity_df
    index_number = book_similarity_df.index.get_loc(book_name)
    
        
    # Adding the similar books index to a list
    similar_books = book_similarity_df.iloc[index_number].sort_values(ascending=False).head(6).index[1:].tolist()
        
    # Finding the book name from the user_book_matrix
    top_similar_books = book_similarity_df.iloc[similar_books].index.tolist()
            
    data = []
    for i in top_similar_books:
        item = []
        temp_df = filtered_df[filtered_df['Book-Title'] == i]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Rating'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
            
        data.append(item)

    data = pd.DataFrame(data=data)       

    #st.table(data)

    # Split the records into two columns
    col1, col2 = st.columns(2)

    # Iterate over each book in the top 50 records
    for i, book in data.iterrows():
        # Determine the column number based on the iteration index
        col = col1 if i % 2 == 0 else col2

        # Display book image and details in the column
        with col:
            # Display the book image
            st.image(book[2], caption=book[0], width=150)

            # Display the book name
            st.write(f"Book-Title:- {book[0]}")

            # Display the other details
            st.write(f"Book-Author:- {book[1]}")
            st.write(f"Publisher:- {book[4]}")
            st.write(f"Book-Rating:- {book[3]}")

            # Add a separator between books
            st.write("---")

    else:
        st.write("No More data available")

        #st.write("Book_Name", book_name)
        #st.write('index_number', index_number)
        #st.write('similar_books', similar_books)
        #st.write('top_similar_books', top_similar_books)
        #st.write(data)

st.markdown('<h1 style="font-size: 30px; white-space: nowrap;">Book Recommendation System</h1>', unsafe_allow_html=True)

st.write(
    "<p style='font-size: 15px;'>Hello..",
    "<p style='font-size: 15px;'>Welcome All to our Book Recommendation.",
    "<p style='font-size: 15px;'>Here we recommend you Popular Books or the Books according to your preferences.",
    "<p style='font-size: 15px;'>To begin with select your category below..</p>",
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

if col1.button('Top 50 Popular Books'):
    top_50_books()

if col2.button('Get Book Recommendation'):
    book_name = st.text_input("Enter Book Name", value='', key='book_name_input')
    if book_name:
        book_name = get_recommendation(book_name)
        if book_name:
            st.write(data)
