import streamlit as st
import pandas as pd

# Define the Streamlit app
def getPreferences(userName, database):
    """ prompts user to enter their artist preferences.
    Saves user and their preferences to database dictionary """
    
    newPref = ""
    if userName in database:
        prefs = database[userName]
    else:
        prefs = []
        newPref = input("Enter an artist that you like (Enter to finish):" + "\n")

    while newPref!= "":
        prefs+= [newPref.strip().title()]
        newPref = input("Enter an artist that you like (Enter to finish):" + "\n")

    prefs.sort()
    prefs = removeDuplicates(prefs)
    for thing in database:
                database[thing] = removeDuplicates(database[thing])
    prefs.sort()
    database[userName] = prefs

def getNewPreferences(userName, database):
    """ does same as getpreferences, but only if prompted in menu by inputting
    e """
    prefs = []
    newPref = input("Enter an artist that you like (Enter to finish):" + "\n")

    while newPref!= "":
        prefs+= [newPref.strip().title()]
        newPref = input("Enter an artist that you like (Enter to finish):" + "\n")

    prefs.sort()
    prefs = removeDuplicates(prefs)
    for thing in database:
                database[thing] = removeDuplicates(database[thing])
    prefs.sort()
    database[userName] = prefs

    
def displayMenu(userName, database):
    """ presents display menu to user and gives options to user to lead them
    to different actions """
    while True:
        print("Enter a letter to choose an option:")
        print("e - Enter preferences")
        print("r - Get recommendations")
        
        option = input()
        if option == "e":
            getNewPreferences(userName, database)
        if option == "r":
            getRecommendations(userName, database)
  
    
def getRecommendations(userName, database):
    """ provides a list of user recommendations (if they exist) to user"""
    bestUser = findBestUser(userName, database)
    if bestUser==None or database[userName]==[]:
        print("No recommendations available at this time")
    else:
        recommendations = exclusiveListTwo(database[userName], database[bestUser])
        for thing in recommendations:
            print(thing)

def main():
    """main function, will perform entire project """

    database = loadUsers("musicrecplus.txt")
    intro(database)
    
if __name__ == "__main__": main()    
  
