#!/usr/bin/python
##############################################################
# Program name: NCAA Basketball Stats Scraper (Settings file)
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks:
# Refer to http://stats.ncaa.org/team/inst_team_list?sport_code=MBB&division=1 in setting these variables
##############################################################

# Select year for parsing
academic_year = "2019"
yearIndexDict = {"2019":"14781","2018":"12973","2017":"12560","2016":"12360","2015":"12080","2014":"11620","2013":"11320","2012":"10942","2011":"10561","2010":"10240"}
year_index = yearIndexDict[academic_year]

# What do you want to do? (Note: Lower tiers need higher tiers, i.e., ind_game_stats requires map_players (Tier 2), which requires map_teams (Tier 1).)
map_teams = 1 # Create a team mapping (0 = no, 1 = yes) -- TIER 1
map_schedule = 1 # Create schedule mapping (0 = no, 1 = yes)
map_players = 1 # Create a player mapping (0 = no, 1 = yes)
summary_teams = 1 # Get summary statistics for each team (0 = no, 1 = yes)
summary_players = 1 # Get summary statistics for each player (0 = no, 1 = yes)
ind_game_stats = 1 # Get individual game statistics (0 = no, 1 = yes)
ind_player_stats = 1 # Get individual player statistics (0 = no, 1 = yes)
ind_team_stats = 1 # Get individual team statistics (a line per team, such that each game will have two lines (one for away team, one for home team)) (0 = no, 1 = yes)


# Where do you want to save the data?
team_mappingfile = "mappings/team_mappings.tsv" # Data file for team mappings
player_mappingfile = "mappings/player_mappings.tsv" # Data file for player mappings
schedule_mappingfile = "mappings/schedule_mappings.csv" # Data file for schedule mappings
summary_hitting_data = "data/summary_hitting_data.tsv" # Data file for individual player summary statistics
summary_pitching_data = "data/summary_pitching_data.tsv"
summary_team_hitting_data = "data/summary_team_hitting_data.tsv" # Data file for team summary statistics
summary_team_pitching_data = "data/summary_team_pitching_data.tsv"
game_data = "data/game_data.tsv" # Data file for each game
player_data = "data/player_data.tsv" # Data file for each player
team_data = "data/team_data.tsv" # Data file for each team


#### The variables below could be set, but probably don't need any modification #####
debugmode = 1 # Output program steps (0 = off, 1 = on)
params = { } # Any POST parameters that need to be sent (default)
http_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://stats.ncaa.org/team/inst_team_list?academic_year=2016&conf_id=-1&division=1&sport_code=MBA",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
            } # Variables from the HTTP header (default)

start_url = 'http://stats.ncaa.org/team/inst_team_list?academic_year=' + str(academic_year) + "&conf_id=-1&division=1&sport_code=MBA" # URL to start from (Change this for different years). You can get this URL from http://stats.ncaa.org/team/inst_team_list?sport_code=MBB&division=1. This URL is for the 2011-2012 season.
domain_base = 'http://stats.ncaa.org' # Base domain
