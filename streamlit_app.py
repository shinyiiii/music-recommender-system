import streamlit as st
import pandas as pd

def main():
    st.title("Music Recommendation App")

    # Text input for song selection
    song_name = st.text_input("Enter a song name:")

    # Button to generate recommendations
    if st.button("Generate Recommendations"):
      
        recommendations = generate_recommendations(song_name)
        st.write(recommendations)
   
