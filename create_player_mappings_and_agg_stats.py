#!/usr/bin/python
##############################################################
# Program name: NCAA Basetball Stats Scraper (Player Mapping and Summary Stats Module)
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks:
##############################################################

# Import modules and libraries
#import dropbox
import os
import scraperfunctions
import scrapersettings
import csv
import re
from bs4 import BeautifulSoup

if (scrapersettings.map_players == 1):
    # Create the file headings
    player_mappingfile_w = open(scrapersettings.player_mappingfile, "w")
    player_mappingfile_w.writelines("player_id\tteam_id\tplayer_name\n")

if (scrapersettings.summary_players == 1):
    # Create the file headings
    summary_hitting_data_w = open(scrapersettings.summary_hitting_data, "w")
    summary_pitching_data_w = open(scrapersettings.summary_pitching_data, "w")
    pit_headers = ['player_id','team_id','team_name']
    pit_b = True
    hit_headers = ['player_id','team_id','team_name']
    hit_b = True

if (scrapersettings.summary_teams == 1):
    # Create the file headings
    summary_team_hitting_data_w = open(scrapersettings.summary_team_hitting_data, "w")
    summary_team_hitting_data_w.writelines("team_id\tteam_name\tteam_games\tteam_BA\tteam_OBPpct\tteam_SLGpct\tteam_AB\tteam_R\tteam_H\tteam_2B\tteam_3B\tteam_TB\tteam_HR\tteam_RBI\tteam_BB\tteam_HBP\tteam_SF\tteam_SH\tteam_K\tteam_DP\tteam_SB\tteam_CS\tteam_Picked\topp_team_games\topp_team_BA\topp_team_OBPpct\topp_team_SLGpct\topp_team_AB\topp_team_R\topp_team_H\topp_team_2B\topp_team_3B\topp_team_TB\topp_team_HR\topp_team_RBI\topp_team_BB\topp_team_HBP\topp_team_SF\topp_team_SH\topp_team_K\topp_team_DP\topp_team_SB\topp_team_CS\topp_team_Picked\n")    
    summary_team_pitching_data_w = open(scrapersettings.summary_team_pitching_data,"w")
    summary_team_pitching_data_w.writelines("team_id\tteam_name\tteam_ERA\tteam_IP\tteam_H\tteam_R\tteam_ER\tteam_BB\tteam_SO\tteam_SHO\tteam_BF\tteam_POAB\tteam_2BA\tteam_3BA\tteam_BK\tteam_HRA\tteam_WP\tteam_HB\tteam_IBB\tteam_SHA\tteam_SFA\tteam_GO\tteam_FO\tteam_KL\topp_team_ERA\topp_team_IP\topp_team_H\topp_team_R\topp_team_ER\topp_team_BB\topp_team_SO\topp_team_SHO\topp_team_BF\topp_team_POAB\topp_team_2BA\topp_team_3BA\topp_team_BK\topp_team_HRA\topp_team_WP\topp_team_HB\topp_team_IBB\topp_team_SHA\topp_team_SFA\topp_team_GO\topp_team_FO\topp_team_KL\n")


if (scrapersettings.map_players == 1) or (scrapersettings.summary_players == 1) or (scrapersettings.summary_teams == 1):
    print "Generating player mappings and/or summary data for players and/or summary data for teams"
    # Grab data
    # Parse our mappings file to get our list of teams
    team_mapping = scraperfunctions.get_team_mappings()
    # Parse the stats table
    player_list = [] # Create an empty list for storing all of our players
    pitching_list = []
    team_stats_total = []
    for value, team in enumerate(team_mapping): # For each team in our dictionary
        if scrapersettings.debugmode == 1: print "Processing team " + str(team) + " (" + str(value+1) + " of " + str(len(team_mapping)) + ")"
        roster_url = str(scrapersettings.domain_base) + "/team/" + team + "/stats/" + str(scrapersettings.year_index)
        team_name = team_mapping[team][0]
        roster_page_data = scraperfunctions.grabber(roster_url, scrapersettings.params, scrapersettings.http_header) # Grab the main page for each team
        roster_page_data_soup = BeautifulSoup(roster_page_data)
        stat_grid = roster_page_data_soup.select('#stat_grid')

        for row,val in enumerate(roster_page_data_soup.select('th')):
            hit_headers.append(val.get_text())

        if hit_b:
            writeline = ""
            for item in hit_headers:
                writeline += str(item.encode('utf-8')) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            summary_hitting_data_w.writelines(writeline)
            hit_b=False

        # Get Player Data
        for rowno, row in enumerate(stat_grid[0].find('tbody').findAll('tr')):
            tds = row.findAll('td')
            player_id = tds[1].find('a').get('href').split('=')[-1]
            indstats=[player_id,team,team_name]
            for val, row in enumerate(tds):
                if val == 1:
                    result = scraperfunctions.run_safely(row.find('a').get_text().encode('utf-8').strip())
                else:
                    result = scraperfunctions.run_safely(row.get_text().strip())
                indstats.append(result)
                player_list.append(indstats)

            if (scrapersettings.summary_players == 1):
                writeline = ""
                for item in indstats:
                    writeline += str(item) + "\t"
                writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                summary_hitting_data_w.writelines(writeline)

        # Get Pitching Data
        pitching_roster_url = str(scrapersettings.domain_base) + "/team/" + team + "/stats?id=" + str(scrapersettings.year_index) + "&year_stat_category_id=14644"
        pitching_team_name = team_mapping[team][0]
        pitching_page_data = scraperfunctions.grabber(pitching_roster_url,scrapersettings.params,scrapersettings.http_header)
        pitching_page_data_soup = BeautifulSoup(pitching_page_data)
        pitching_stat_grid = pitching_page_data_soup.select('#stat_grid td , .sorting_asc , .sorting')

        ## Get pitching header names
        for row,val in enumerate(pitching_page_data_soup.select('th')):
            pit_headers.append(val.get_text())

        if pit_b:
            writeline = ""
            for item in pit_headers:
                writeline += str(item.encode('utf-8')) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            summary_pitching_data_w.writelines(writeline)
            pit_b=False

        #for rownum, raw in enumerate(pitching_stat_grid):
        pit_tds = pitching_stat_grid
        pit_player_id = pit_tds[1].find('a').get('href').split('=')[-1]
        pitstats = [pit_player_id,team,pitching_team_name]
        for val, row in enumerate(pit_tds):
            if val == 1:
                result = scraperfunctions.run_safely(row.find('a').get_text().encode('utf-8').strip())
            else:
                result = scraperfunctions.run_safely(row.get_text().strip())
            pitstats.append(result)
            pitching_list.append(pitstats)

            if (scrapersettings.summary_players == 1):
                writeline = ""
                for item in pitstats:
                    if isinstance(item,unicode):
                        writeline += str(item.encode('utf-8')) + "\t"
                    else:
                        writeline += str(item) + "\t"
                writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                summary_pitching_data_w.writelines(writeline)

        # Get Team Data
        team_tds    = stat_grid[0].find('tfoot').findAll('tr')[0].findAll('td')
        team_games  = str(team_tds[6].get_text().encode('utf-8').strip())
        team_BA     = str(team_tds[7].get_text().encode('utf-8').strip())
        team_OBPpct = str(team_tds[8].get_text().encode('utf-8').strip())
        team_SLGpct = str(team_tds[9].get_text().encode('utf-8').strip())
        team_R      = str(team_tds[10].get_text().encode('utf-8').strip())
        team_AB     = str(team_tds[11].get_text().encode('utf-8').strip())
        team_H      = str(team_tds[12].get_text().encode('utf-8').strip())
        team_DBL    = str(team_tds[13].get_text().encode('utf-8').strip())
        team_TRP    = str(team_tds[14].get_text().encode('utf-8').strip())
        team_TOT    = str(team_tds[15].get_text().encode('utf-8').strip())
        team_HR     = str(team_tds[16].get_text().encode('utf-8').strip())
        team_RBI = str(team_tds[17].get_text().encode('utf-8').strip())
        team_BB = str(team_tds[18].get_text().encode('utf-8').strip())
        team_HBP = str(team_tds[19].get_text().encode('utf-8').strip())
        team_SF  = str(team_tds[20].get_text().encode('utf-8').strip())
        team_SH  = str(team_tds[21].get_text().encode('utf-8').strip())
        team_K  = str(team_tds[22].get_text().encode('utf-8').strip())
        team_DP  = str(team_tds[23].get_text().encode('utf-8').strip())
        team_CS  = str(team_tds[24].get_text().encode('utf-8').strip())
        team_Picked = str(team_tds[25].get_text().encode('utf-8').strip())
        team_SB  = str(team_tds[26].get_text().encode('utf-8').strip())
        team_stats 	= [team_games, team_BA, team_OBPpct, team_SLGpct, team_AB, team_R, team_H, team_DBL, team_TRP, team_TOT, team_HR, team_RBI, team_BB, team_HBP, team_SF, team_SH, team_K, team_DP, team_SB, team_CS, team_Picked]

        # Get Opposing Team Data
        opp_team_tds  = stat_grid[0].find('tfoot').findAll('tr')[1].findAll('td')
        opp_team_games  = str(opp_team_tds[6].get_text().encode('utf-8').strip())
        opp_team_BA  = str(opp_team_tds[7].get_text().encode('utf-8').strip())
        opp_team_OBPpct  = str(opp_team_tds[8].get_text().encode('utf-8').strip())
        opp_team_SLGpct  = str(opp_team_tds[9].get_text().encode('utf-8').strip())
        opp_team_R  = str(opp_team_tds[10].get_text().encode('utf-8').strip())
        opp_team_AB  = str(opp_team_tds[11].get_text().encode('utf-8').strip())
        opp_team_H  = str(opp_team_tds[12].get_text().encode('utf-8').strip())
        opp_team_DBL = str(opp_team_tds[13].get_text().encode('utf-8').strip())
        opp_team_TRP = str(opp_team_tds[14].get_text().encode('utf-8').strip())
        opp_team_TOT = str(opp_team_tds[15].get_text().encode('utf-8').strip())
        opp_team_HR = str(opp_team_tds[16].get_text().encode('utf-8').strip())
        opp_team_RBI = str(opp_team_tds[17].get_text().encode('utf-8').strip())
        opp_team_BB = str(opp_team_tds[18].get_text().encode('utf-8').strip())
        opp_team_HBP = str(opp_team_tds[19].get_text().encode('utf-8').strip())
        opp_team_SF = str(opp_team_tds[20].get_text().encode('utf-8').strip())
        opp_team_SH = str(opp_team_tds[21].get_text().encode('utf-8').strip())
        opp_team_K = str(opp_team_tds[22].get_text().encode('utf-8').strip())
        opp_team_DP = str(opp_team_tds[23].get_text().encode('utf-8').strip())
        opp_team_CS = str(opp_team_tds[24].get_text().encode('utf-8').strip())
        opp_team_Picked = str(opp_team_tds[25].get_text().encode('utf-8').strip())
        opp_team_SB = str(opp_team_tds[26].get_text().encode('utf-8').strip())
        opp_team_stats = [opp_team_games, opp_team_BA, opp_team_OBPpct, opp_team_SLGpct, opp_team_AB, opp_team_R, opp_team_H, opp_team_DBL, opp_team_TRP, opp_team_TOT, opp_team_HR, opp_team_RBI, opp_team_BB, opp_team_HBP, opp_team_SF, opp_team_SH, opp_team_K, opp_team_DP, opp_team_SB, opp_team_CS, opp_team_Picked]

        team_stats_total = [team, team_name] + team_stats + opp_team_stats
        if (scrapersettings.summary_teams == 1):
            writeline = ""
            for item in team_stats_total:
                writeline += str(item.encode('utf-8')) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            summary_team_hitting_data_w.writelines(writeline)

       # Get Pitching Team Data
        pit_team_tds = pitching_page_data_soup.find('tfoot').findAll('tr')[0].findAll('td')
        pit_team_ERA = str(pit_team_tds[9].get_text().encode('utf-8').strip())
        pit_team_IP = str(pit_team_tds[10].get_text().encode('utf-8').strip())
        pit_team_H = str(pit_team_tds[12].get_text().encode('utf-8').strip())
        pit_team_R = str(pit_team_tds[13].get_text().encode('utf-8').strip())
        pit_team_ER = str(pit_team_tds[14].get_text().encode('utf-8').strip())
        pit_team_BB = str(pit_team_tds[15].get_text().encode('utf-8').strip())
        pit_team_SO = str(pit_team_tds[16].get_text().encode('utf-8').strip())
        pit_team_SHO = str(pit_team_tds[17].get_text().encode('utf-8').strip())
        pit_team_BF = str(pit_team_tds[18].get_text().encode('utf-8').strip())
        pit_team_POAB = str(pit_team_tds[19].get_text().encode('utf-8').strip())
        pit_team_2BA = str(pit_team_tds[20].get_text().encode('utf-8').strip())
        pit_team_3BA = str(pit_team_tds[21].get_text().encode('utf-8').strip())
        pit_team_BK = str(pit_team_tds[22].get_text().encode('utf-8').strip())
        pit_team_HRA = str(pit_team_tds[23].get_text().encode('utf-8').strip())
        pit_team_WP = str(pit_team_tds[24].get_text().encode('utf-8').strip())
        pit_team_HB = str(pit_team_tds[25].get_text().encode('utf-8').strip())
        pit_team_IBB = str(pit_team_tds[26].get_text().encode('utf-8').strip())
        pit_team_SHA = str(pit_team_tds[29].get_text().encode('utf-8').strip())
        pit_team_SFA = str(pit_team_tds[30].get_text().encode('utf-8').strip())
        pit_team_GO = str(pit_team_tds[32].get_text().encode('utf-8').strip())
        pit_team_FO = str(pit_team_tds[33].get_text().encode('utf-8').strip())
        pit_team_KL = str(pit_team_tds[37].get_text().encode('utf-8').strip())
        pit_team_stats = [pit_team_ERA,pit_team_IP,pit_team_H,pit_team_R,pit_team_ER,pit_team_BB,pit_team_SO,pit_team_SHO,pit_team_BF,pit_team_POAB,pit_team_2BA,pit_team_3BA,pit_team_BK,pit_team_HRA,pit_team_WP,pit_team_HB,pit_team_IBB,pit_team_SHA,pit_team_SFA,pit_team_GO,pit_team_FO,pit_team_KL]
       # Get Pitching Opposing Team Data
        opp_pit_team_tds = pitching_page_data_soup.find('tfoot').findAll('tr')[1].findAll('td')
        opp_pit_team_ERA = str(opp_pit_team_tds[9].get_text().encode('utf-8').strip())
        opp_pit_team_IP = str(opp_pit_team_tds[10].get_text().encode('utf-8').strip())
        opp_pit_team_H = str(opp_pit_team_tds[12].get_text().encode('utf-8').strip())
        opp_pit_team_R = str(opp_pit_team_tds[13].get_text().encode('utf-8').strip())
        opp_pit_team_ER = str(opp_pit_team_tds[14].get_text().encode('utf-8').strip())
        opp_pit_team_BB = str(opp_pit_team_tds[15].get_text().encode('utf-8').strip())
        opp_pit_team_SO = str(opp_pit_team_tds[16].get_text().encode('utf-8').strip())
        opp_pit_team_SHO = str(opp_pit_team_tds[17].get_text().encode('utf-8').strip())
        opp_pit_team_BF = str(opp_pit_team_tds[18].get_text().encode('utf-8').strip())
        opp_pit_team_POAB = str(opp_pit_team_tds[19].get_text().encode('utf-8').strip())
        opp_pit_team_2BA = str(opp_pit_team_tds[20].get_text().encode('utf-8').strip())
        opp_pit_team_3BA = str(opp_pit_team_tds[21].get_text().encode('utf-8').strip())
        opp_pit_team_BK = str(opp_pit_team_tds[22].get_text().encode('utf-8').strip())
        opp_pit_team_HRA = str(opp_pit_team_tds[23].get_text().encode('utf-8').strip())
        opp_pit_team_WP = str(opp_pit_team_tds[24].get_text().encode('utf-8').strip())
        opp_pit_team_HB = str(opp_pit_team_tds[25].get_text().encode('utf-8').strip())
        opp_pit_team_IBB = str(opp_pit_team_tds[26].get_text().encode('utf-8').strip())
        opp_pit_team_SHA = str(opp_pit_team_tds[29].get_text().encode('utf-8').strip())
        opp_pit_team_SFA = str(opp_pit_team_tds[30].get_text().encode('utf-8').strip())
        opp_pit_team_GO = str(opp_pit_team_tds[32].get_text().encode('utf-8').strip())
        opp_pit_team_FO = str(opp_pit_team_tds[33].get_text().encode('utf-8').strip())
        opp_pit_team_KL = str(opp_pit_team_tds[37].get_text().encode('utf-8').strip())
        opp_pit_team_stats = [opp_pit_team_ERA,opp_pit_team_IP,opp_pit_team_H,opp_pit_team_R,opp_pit_team_ER,opp_pit_team_BB,opp_pit_team_SO,opp_pit_team_SHO,opp_pit_team_BF,opp_pit_team_POAB,opp_pit_team_2BA,opp_pit_team_3BA,opp_pit_team_BK,opp_pit_team_HRA,opp_pit_team_WP,opp_pit_team_HB,opp_pit_team_IBB,opp_pit_team_SHA,opp_pit_team_SFA,opp_pit_team_GO,opp_pit_team_FO,opp_pit_team_KL]
        pit_stats_total = [team, team_name] + pit_team_stats + opp_pit_team_stats
        if (scrapersettings.summary_teams == 1):
             writeline = ""
             for item in pit_stats_total:
                 writeline += str(item.encode('utf-8')) + "\t"
             writeline = re.sub('\t$', '', writeline)
             writeline += "\n"
             summary_team_pitching_data_w.writelines(writeline)
    print "Successfully generated player mappings and/or summary data for players and/or summary data for teams"


if (scrapersettings.map_players == 1):
    player_dict = dict([(case[0], (case[1:])) for case in player_list]) # Create a dictionary from our list so we don't have any duplicate entries
    for item in player_dict: # For each item on that list
        player_mappingfile_w.writelines(str(item) + "\t" + player_dict[item][1] + "\t" + player_dict[item][0] + "\n")


#token = os.environ['DROPBOX_TOKEN']
#dbx = dropbox.Dropbox(token)

#f = open('data/summary_hitting_data.tsv', 'rb')
#response = dbx.files_upload(f.read(), 
#'/Heroku_NCAA_D1_Baseball_Data/summary_hitting_data.tsv', mode=dropbox.files.WriteMode("overwrite"))
#f.close()

#f2 = open('data/summary_pitching_data.tsv', 'rb')
#response = dbx.files_upload(f2.read(), 
#'/Heroku_NCAA_D1_Baseball_Data/summary_pitching_data.tsv', mode=dropbox.files.WriteMode("overwrite"))
#f2.close()

#f3 = opem('data/summary_hitting_data.tsv','rb')
#response = dbx.files_upload(f3.read(),
#'/Heroku_NCAA_D1_Baseball_Data/summary_team_hitting_data.tsv', mode=dropbox.files.WriteMode("overwrite"))
#f3.close()

#f4 = open('data/summary_pitching_data.tsv','rb')
#response = dbx.files_upload(f4.read(),
#'/Heroku_NCAA_D1_Baseball_Data/summary_team_pitching_data.tsv', mode=dropbox.files.WriteMode("overwrite"))
#f4.close()
