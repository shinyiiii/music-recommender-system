import streamlit as st
import pandas as pd

# Define the Streamlit app
def main():
    st.title("Music Recommendation App")

    # Text input for song selection
    song_name = st.text_input("Enter a song name:")

    # Button to generate recommendations
    if st.button("Generate Recommendations"):
        # Generate and display recommendations
        recommendations = generate_recommendations(song_name)
        st.write(recommendations)
        
# Function to generate recommendations
def getRecommendations(userName, database):
    #provides a list of user recommendations (if they exist) to user"""
    bestUser = findBestUser(userName, database)
    if bestUser==None or database[userName]==[]:
        print("No recommendations available at this time")
    else:
        recommendations = exclusiveListTwo(database[userName], database[bestUser])
        for thing in recommendations:
            print(thing)

# Filter songs by favorite artists
    filtered_songs = df[df['artists'].apply(lambda x: any(artist in x for artist in user_input["favorite_artists"]))]
        
if __name__ == "__main__":
    main()        
  
