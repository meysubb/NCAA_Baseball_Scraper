#!/usr/bin/python
##############################################################
# Program name: NCAA Baseball Stats Scraper (Schedule Mapping Module)
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks:
##############################################################

# Import modules and libraries
import scraperfunctions
import scrapersettings
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd



if (scrapersettings.map_schedule == 1):
    print "Generating schedule mappings"

    # Grab data
    # Parse our mappings file to get our list of teams
    team_mapping = scraperfunctions.get_team_mappings()

    # Create the schedule
    schedule_list = [] # Create an empty list for storing all of our games
    for value, team in enumerate(team_mapping): # For each team in our dictionary
        if scrapersettings.debugmode == 1: print "Processing team " + str(team) + " (" + str(value+1) + " of " + str(len(team_mapping)) + ")"
        try:
            #team_mainpage_data = scraperfunctions.grabber(team_mapping[team][1], scrapersettings.params, scrapersettings.http_header) # Grab the main page for each team
            result = requests.get(team_mapping[team][1])
            c = result.content
        except:
            print "Error getting data. Moving on to next game."
            continue
        team_mainpage_data_soup = BeautifulSoup(c)
        gamelinks = [] # Create a blank list for each game
        for link in team_mainpage_data_soup.find_all('a'): # Locate all links in the document
            if "contests/" in link.get('href'): # If they contain a URL segment suggesting it is a game...
                if link.get('href') == "/contests/scoreboards" :
                    continue 
                game_link = str(scrapersettings.domain_base + link.get('href')).split("?")[0] # Strip out any URL variables since we don't need them
                try:
                    opponent_id = link.find_previous("td").find_previous("td").find("a").get('href').split("/teams/")[1]
                except:
                    opponent_id = 0
                opponent_text = link.find_previous("td").find_previous("td").get_text().encode('utf-8').strip()
                if "@" in opponent_text: # Checks if home or away; note: if it's in a neutral site, this distinction may not be accurate (but a neutral site is flagged). Assumes all games against non-D-I/III competition is at home.
                    home_team = opponent_id
                    away_team = team
                    if "<br/>" in str(link.find_previous("a").encode('utf-8').strip()):
                        neutral = "1"
                    else:
                        neutral = "0"
                else:
                    home_team = team
                    away_team = opponent_id
                    neutral = "0"
                date = link.find_previous("td").find_previous("td").find_previous("td").get_text() # Get the date for the game
                game_id = game_link.split("/")[-2] # Get the game ID from the URL (last set of digits)
                schedule_list.append([game_id, home_team, away_team, date, neutral, game_link]) # Append all of this information to our master schedule list
                

    schedule_dict = dict([(case[0], (case[1:])) for case in schedule_list]) # Create a dictionary from our list so we don't have any duplicate entries
    temp_df = pd.DataFrame.from_dict(
        schedule_dict, orient='index').reset_index()
    temp_df.columns = ['game_id', 'home_team_id',
                       'away_team_id', 'date', 'neutral_site', 'game_link']
    temp_df.to_csv(scrapersettings.schedule_mappingfile,index=False)
    print "Successfully generated schedule mappings"
