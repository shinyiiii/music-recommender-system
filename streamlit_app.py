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

def saveUserPreferences(userName, prefs, database, fileName):
    """ saves user preferences to the fileName file"""
    
    userMap[userName] = prefs
    file = open(fileName, "w")
    for user in database:
        toSave = str(user) + ":" + ",".join(database[user])+ "\n"
        file.write(toSave)
    file.close()


def loadUsers(fileName):
    """ will store information from fileName file to database dictionary"""
    database = {}
    try:
        file = open(fileName, "r")
        for line in file:
            [userName, artists] = line.strip().split(":")
            artistList = artists.split(",")
            artistList.sort()
            database[userName] = artistList
        file.close()
    except:
        return database
    return database

    
def displayMenu(userName, database):
    """ presents display menu to user and gives options to user to lead them
    to different actions """
    while True:
        print("Enter a letter to choose an option:")
        print("e - Enter preferences")
        print("r - Get recommendations")
        print("p - Show most popular artists")
        print("h - How popular is the most popular")
        print("m - Which user has the most likes")
        print("q - Save and quit")

        option = input()
        if option == "e":
            getNewPreferences(userName, database)
        if option == "r":
            getRecommendations(userName, database)
        if option == "p":
            getMostPopularArtists(userName, database)
        if option == "h":
            getHowPopular(userName, database)
        if option == "m":
            userThatLikesMost(userName, database)
        if option == "q":
            saveUserPreferences(userName, database[userName], database, "musicrecplus.txt")
            break


def saveUserPreferences(userName, prefs, database, fileName):
    """saves and quits the program. writes updated prefs for userName from
    the database into the fileName file"""
    
    file = open(fileName, "w")
    for user in database:
        toSave = user + ":" + ",".join(database[user]) + "\n"
        file.write(toSave)
    file.close()
    
    
def userThatLikesMost(userName, database):
    """prints the name of the user that ilkes the most artists
    ignoring private users if there is a user that likes the most."""
    
    if findMostLikesUser(userName, database)[1] == 0:
        print("Sorry, no user found")
    else:
        print(findMostLikesUser(userName, database)[0])
        

def findMostLikesUser(userName, database):
    """returns a tuple of the user that likes the most amount of artists
    and the number of likes the user has (ignoring private users) """
    
    usersList = []
    for item in database:
        usersList+=[item]
    bestUser = []
    for user in usersList:
            if user[-1] != "$":
                bestUser = user
                break
            
    bestScore = len(database[bestUser])
    for user in usersList:
        score = len(database[user])
        if score > bestScore and user[-1] != "$":
            bestScore = score
            bestUser = user
            
    return (bestUser, bestScore)
    
    
def getHowPopular(userName, database):
    """prints how popular the most popular artist is (ignoring private users)"""
    freqdatabase = artistFrequencyDict(userName, database)
    e = tupilizeDict(freqdatabase)
    e.sort()
    if len(e) == 0:
        print("Sorry, no artists found.")
    else:
        print(freqdatabase[e[-1][1]])
    
def artistFrequencyDict(userName, database):
    '''returns a dictionary of the frequency of artists'''
    
    artistsFrequency = {}
    for item in database:
        for j in database[item]:
            if j in artistsFrequency and item[-1]!="$":
                artistsFrequency[j] += 1
            if j not in artistsFrequency and item[-1]!= "$":
                artistsFrequency[j] = 1
    return artistsFrequency

def getMostPopularArtists(userName, database):
    """prints the top three artists in the database of users and the artists
    they listen to. calculations ignore private users"""
    
    freqdatabase = artistFrequencyDict(userName, database)
    e = tupilizeDict(freqdatabase)
    e.sort()
    if len(e) == 0:
        print("Sorry, no artists found.")
    elif len(e) < 3:
        for i in range(-1, -len(e)-1, -1):
            print(e[i][1])
    else:
        print(e[-1][1])
        print(e[-2][1])
        print(e[-3][1])
    
def tupilizeDict(d):
    '''
    Changes dictionary to a list of tuples and also reverses the dictionary's key and value 
    '''
    LofTuples = []
    for thing in d:
        LofTuples += [(d[thing], thing)]
    return LofTuples

    
def getRecommendations(userName, database):
    """ provides a list of user recommendations (if they exist) to user"""
    bestUser = findBestUser(userName, database)
    if bestUser==None or database[userName]==[]:
        print("No recommendations available at this time")
    else:
        recommendations = exclusiveListTwo(database[userName], database[bestUser])
        for thing in recommendations:
            print(thing)

def findBestUser(userName, database):
    """ finds a user in the database with the most amount of matches with
    another user in the database (as long as the other user's preferences
    are not a subset of the user's preference. If there is a tie, the first
    other user is used as a match"""
    usersList = []
    for item in database:
        if item[-1] != "$" and item!=userName and database[item]!=database[userName]:
            usersList+=[item]
    bestUser = None
    bestScore = -1
    for user in usersList:
        score = numMatches(database[userName], database[user])
        if score > bestScore:
            bestScore = score
            bestUser = user
            
    return bestUser


def exclusiveListTwo(L1, L2):
    """ returns all the elements in L2 that are not in L1"""
    
    L3 = [x for x in L2 if x not in L1]
    return L3
        
def numMatches(L1, L2):
    """ returns the number of matches of elements between two lists"""
    
    matches = 0
    i = 0
    j = 0
    while i < len(L1) and j < len(L2):
        if L1[i] == L2[j]:
            matches+=1
            i+=1
            j+=1
        elif L1[i] < L2[j]:
            i+=1
        else:
            j+=1
    return matches

def removeDuplicates(L):
    """ returns a list same as L but without any duplicates"""
    final = []
    for item in L:
        if item not in final:
            final+=[item]
    return final

def intro(database):
    """ allows user to start inputting information"""
    
    userName = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private):" + "\n")
    if userName not in database:
        getPreferences(userName, database)
    displayMenu(userName, database)

def main():
    """main function, will perform entire project """

    database = loadUsers("musicrecplus.txt")
    intro(database)
    
if __name__ == "__main__": main()    
  
