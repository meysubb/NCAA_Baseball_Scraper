#!/usr/bin/python
##############################################################
# Program name: NCAA Baseball Stats Scraper
# Version: 1.3
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks:
##############################################################

# Import modules and libraries
import os
import dropbox
import scraperfunctions
import scrapersettings
import csv
import re
from bs4 import BeautifulSoup
import requests

if (scrapersettings.ind_game_stats == 1):
    # Create the file headings
    game_data_w = open(scrapersettings.game_data, "w")
    game_data_w.writelines("game_id\tgame_date\taway_team_id\taway_team_name\taway_g\taway_r\taway_ab\taway_h\taway_two_b\taway_three_b\taway_total_b\taway_hr\taway_rbi\taway_bb\taway_hbp\taway_sf\taway_sh\taway_k\taway_dp\taway_sb\taway_cs\taway_picked\thome_team_id\thome_team_name\thome_g\thome_r\thome_ab\thome_h\thome_two_b\thome_three_b\thome_total_b\thome_hr\thome_rbi\thome_bb\thome_hbp\thome_sf\thome_sh\thome_k\thome_dp\thome_sb\thome_cs\thome_picked\tneutral\n")

if (scrapersettings.ind_player_stats == 1):
    # Create the file headings
    player_data_w = open(scrapersettings.player_data, "w")
    #player_data_w.writelines("player_id\tplayer_name\tteam_id\tteam_name\tgame\tpos\tminutes\tfgm\tfga\tthree_fgm\tthree_fga\tft\tfta\tpts\toffreb\tdefreb\ttotreb\tast\tto\tstl\tblk\tfouls\tgame_date\tneutral_site\n")

if (scrapersettings.ind_team_stats == 1):
    # Create the file headings
    team_data_w = open(scrapersettings.team_data, "w")
    #team_data_w.writelines("game_id\tgame_date\tsite\tteam_id\tteam_name\tteam_minutes\tteam_fgm\tteam_fga\tteam_three_fgm\tteam_three_fga\tteam_ft\tteam_fta\tteam_pts\tteam_offreb\tteam_defreb\tteam_totreb\tteam_ast\tteam_to\tteam_stl\tteam_blk\tteam_fouls\n")


if (scrapersettings.ind_game_stats == 1) or (scrapersettings.ind_player_stats == 1) or (scrapersettings.ind_team_stats == 1):
    print "Generating individual statistics for players and/or teams"

    # Grab data
    # Parse our mappings file to get our list of teams
    team_mapping = scraperfunctions.get_team_mappings()

    # Parse our schedule file to get a list of games
    game_mapping = scraperfunctions.get_game_mappings()

    # Parse the stats tables
    team_stats_total = [] # Create an empty list for storing the team stats
    alphanum = re.compile(r'[^\w\s:]+')
    for value, game in enumerate(game_mapping): # For each game in our dictionary
        if scrapersettings.debugmode == 1: print "Processing game " + str(game) + " (" + str(value+1) + " of " + str(len(game_mapping)) + ")"
        game_url = game_mapping[game][4]
        # from the game_url grab box_score 
        try:
            result = requests.get(game_url)
            game_page_data = result.content
        except:
            print "Error getting data. Moving on to next game."
            continue
        game_page_data_soup = BeautifulSoup(game_page_data)
        game_urls = game_page_data_soup.find_all('a')
        valid_links = []
        for val in game_urls:
            if "box_score/" in val.get('href'):
                valid_links.append(val.get('href'))
        # proper url
        game_url = "http://stats.ncaa.org" + valid_links[0]
        print 'NEW URL \n'
        print(game_url)
        try:
            result = requests.get(game_url)
            game_page_data = result.content
        except:
            print "Error getting data. Moving on to next game."
            continue
        game_page_data_soup = BeautifulSoup(game_page_data)
        
        ### Wait to do something else here 
        neutral = game_mapping[game][3]
        tables = game_page_data_soup.findAll('table', class_='mytable')
        headertable = tables[0]
        awaystats = tables[1]
        homestats = tables[2]
        # Dynamically write column headers
        if value == 0:
            ind_col_headers = ["player_id","player_name","team_id","team_name","game_date"]
            team_col_headers = ["game_id,game_date,site,team_id,team_name"]
            for rowno, row in enumerate(awaystats.findAll('th')):
                ind_col_headers.append(row.text)
                team_col_headers.append(row.text)
        # Dynamically write column headers
        if value == 0:
            ind_col_headers = ["player_id","player_name","team_id","team_name","game_date"]
            team_col_headers = ["game_id,game_date,site,team_id,team_name"]
            for rowno, row in enumerate(awaystats.findAll('th')):
                ind_col_headers.append(row.text)
                team_col_headers.append(row.text)
            for item in ind_col_headers:
                if item == ind_col_headers[len(ind_col_headers)-1]:
                    player_data_w.write(item + "\n")
                else:
                    if item == "Player":
                        pass
                    else:
                        player_data_w.write("%s\t" % item)
            for row,item in enumerate(team_col_headers):
                if row == 0:
                    game_list = [x.strip() for x in item.split(',')]
                    for val in game_list:
                        team_data_w.write("%s\t" % item)
                elif item == team_col_headers[len(team_col_headers)-1]:
                    team_data_w.write(item + "\n")
                else:
                    team_data_w.writelines("%s\t" % item)


        # Get Participants
        away_team_header = headertable.findAll('tr')[1]
        tds = away_team_header.findAll('td')
        try:
            away_team =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
        except:
            away_team = 0
        try:
            away_team_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
        except:
            try:
                away_team_name = str(tds[0].get_text().encode('utf-8').strip())
            except:
                away_team_name = "Not Available"
        home_team_header = headertable.findAll('tr')[2]
        tds = home_team_header.findAll('td')
        try:
            home_team =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
        except:
            home_team = 0
        try:
            home_team_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
        except:
            try:
                home_team_name = str(tds[0].get_text().encode('utf-8').strip())
            except:
                home_team_name = "Not Available"

        # Get date
        date_locator = re.compile(r'Game Date:')
        date_pattern = re.compile(r'\d+/\d+/\d+')
        try:
            gamedate = re.search(date_pattern, game_page_data_soup.find('td', text=date_locator).find_next('td').get_text()).group(0)
        except:
            gamedate = "ERROR!"

        # Get Away Team Data - Ind stats
        for rowno, row in enumerate(awaystats.findAll('tr', class_='smtext')):
            tds = row.findAll('td')
            try:
                player_id =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
            except:
                player_id = 0
            try:
                player_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
            except:
                try:
                    player_name = str(tds[0].get_text().encode('utf-8').strip())
                except:
                    player_name = "Not Available"
            try:
                pos = str(tds[1].get_text().encode('utf-8').strip())
                pos = alphanum.sub('', pos)
            except:
                pos = "ERROR!"
            try:
                # G
                g = str(tds[2].get_text().encode('utf-8').strip())
                g = alphanum.sub('', g)
            except:
                g = "ERROR!"
            try:
                # R
                r = str(tds[3].get_text().encode('utf-8').strip())
                r = alphanum.sub('', r)
            except:
                r = "ERROR!"
            try:
                # AB
                ab = str(tds[4].get_text().encode('utf-8').strip())
                ab = alphanum.sub('', ab)
            except:
                ab = "ERROR!"
            try:
                # H
                h = str(tds[5].get_text().encode('utf-8').strip())
                h = alphanum.sub('', h)
            except:
                h = "ERROR!"
            try:
                # TWO-B
                two_b = str(tds[6].get_text().encode('utf-8').strip())
                two_b = alphanum.sub('', two_b)
            except:
                two_b = "ERROR!"
            try:
                # Three - B
                three_b = str(tds[7].get_text().encode('utf-8').strip())
                three_b = alphanum.sub('', three_b)
            except:
                three_b = "ERROR!"
            try:
                total_b = str(tds[8].get_text().encode('utf-8').strip())
                total_b = alphanum.sub('', total_b)
            except:
                total_b = "ERROR!"
            try:
                hr = str(tds[9].get_text().encode('utf-8').strip())
                hr = alphanum.sub('', hr)
            except:
                hr = "ERROR!"
            try:
                rbi = str(tds[10].get_text().encode('utf-8').strip())
                rbi = alphanum.sub('', rbi)
            except:
                rbi = "ERROR!"
            try:
                bb = str(tds[11].get_text().encode('utf-8').strip())
                bb = alphanum.sub('', bb)
            except:
                bb = "ERROR!"
            try:
                hbp = str(tds[12].get_text().encode('utf-8').strip())
                hbp = alphanum.sub('', hbp)
            except:
                hbp = "ERROR!"
            try:
                sf = str(tds[13].get_text().encode('utf-8').strip())
                sf = alphanum.sub('', sf)
            except:
                sf = "ERROR!"
            try:
                sh = str(tds[14].get_text().encode('utf-8').strip())
                sh = alphanum.sub('', sh)
            except:
                sh = "ERROR!"
            try:
                k = str(tds[15].get_text().encode('utf-8').strip())
                k = alphanum.sub('', k)
            except:
                k = "ERROR!"
            try:
                dp = str(tds[16].get_text().encode('utf-8').strip())
                dp = alphanum.sub('', dp)
            except:
                dp = "ERROR!"
            try:
                sb = str(tds[17].get_text().encode('utf-8').strip())
                sb = alphanum.sub('', sb)
            except:
                sb = "ERROR!"
            try:
                cs = str(tds[18].get_text().encode('utf-8').strip())
                cs = alphanum.sub('', cs)
            except:
                cs = "ERROR!"
            try:
                picked = str(tds[19].get_text().encode('utf-8').strip())
                picked = alphanum.sub('', picked)
            except:
                picked = "ERROR!"
            try:
                rbi2 = str(tds[20].get_text().encode('utf-8').strip())
                rbi2 = alphanum.sub('', rbi2)
            except:
                rbi2 = "ERROR!"
            ind_stats = [player_id, player_name, away_team, away_team_name, gamedate ,pos,g, r, ab, h, two_b, three_b, total_b, hr, rbi, bb, hbp, sf, sh, k, dp,cs, picked, sb, rbi2]
            if (scrapersettings.ind_player_stats == 1):
                writeline = ""
                for item in ind_stats:
                    writeline += str(item) + "\t"
                #str(gamedate) +
                writeline +=  "\t" + str(neutral)
                #writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                player_data_w.writelines(writeline)

        # Get Home Team Data - Ind stats
        for rowno, row in enumerate(homestats.findAll('tr', class_='smtext')):
            tds = row.findAll('td')
            try:
                player_id =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
            except:
                player_id = 0
            try:
                player_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
            except:
                try:
                    player_name = str(tds[0].get_text().encode('utf-8').strip())
                except:
                    player_name = "Not Available"
            try:
                pos = str(tds[1].get_text().encode('utf-8').strip())
                pos = alphanum.sub('', pos)
            except:
                pos = "ERROR!"
            try:
                # G
                g = str(tds[2].get_text().encode('utf-8').strip())
                g = alphanum.sub('', g)
            except:
                g = "ERROR!"
            try:
                # R
                r = str(tds[3].get_text().encode('utf-8').strip())
                r = alphanum.sub('', r)
            except:
                r = "ERROR!"
            try:
                # AB
                ab = str(tds[4].get_text().encode('utf-8').strip())
                ab = alphanum.sub('', ab)
            except:
                ab = "ERROR!"
            try:
                # H
                h = str(tds[5].get_text().encode('utf-8').strip())
                h = alphanum.sub('', h)
            except:
                h = "ERROR!"
            try:
                # TWO-B
                two_b = str(tds[6].get_text().encode('utf-8').strip())
                two_b = alphanum.sub('', two_b)
            except:
                two_b = "ERROR!"
            try:
                # Three - B
                three_b = str(tds[7].get_text().encode('utf-8').strip())
                three_b = alphanum.sub('', three_b)
            except:
                three_b = "ERROR!"
            try:
                total_b = str(tds[8].get_text().encode('utf-8').strip())
                total_b = alphanum.sub('', total_b)
            except:
                total_b = "ERROR!"
            try:
                hr = str(tds[9].get_text().encode('utf-8').strip())
                hr = alphanum.sub('', hr)
            except:
                hr = "ERROR!"
            try:
                rbi = str(tds[10].get_text().encode('utf-8').strip())
                rbi = alphanum.sub('', rbi)
            except:
                rbi = "ERROR!"
            try:
                bb = str(tds[11].get_text().encode('utf-8').strip())
                bb = alphanum.sub('', bb)
            except:
                bb = "ERROR!"
            try:
                hbp = str(tds[12].get_text().encode('utf-8').strip())
                hbp = alphanum.sub('', hbp)
            except:
                hbp = "ERROR!"
            try:
                sf = str(tds[13].get_text().encode('utf-8').strip())
                sf = alphanum.sub('', sf)
            except:
                sf = "ERROR!"
            try:
                sh = str(tds[14].get_text().encode('utf-8').strip())
                sh = alphanum.sub('', sh)
            except:
                sh = "ERROR!"
            try:
                k = str(tds[15].get_text().encode('utf-8').strip())
                k = alphanum.sub('', k)
            except:
                k = "ERROR!"
            try:
                dp = str(tds[16].get_text().encode('utf-8').strip())
                dp = alphanum.sub('', dp)
            except:
                dp = "ERROR!"
            try:
                sb = str(tds[17].get_text().encode('utf-8').strip())
                sb = alphanum.sub('', sb)
            except:
                sb = "ERROR!"
            try:
                cs = str(tds[18].get_text().encode('utf-8').strip())
                cs = alphanum.sub('', cs)
            except:
                cs = "ERROR!"
            try:
                picked = str(tds[19].get_text().encode('utf-8').strip())
                picked = alphanum.sub('', picked)
            except:
                picked = "ERROR!"
            try:
                rbi2 = str(tds[20].get_text().encode('utf-8').strip())
                rbi2 = alphanum.sub('', rbi2)
            except:
                rbi2 = "ERROR!"
            ind_stats = [player_id, player_name, home_team, home_team_name, gamedate ,pos,g, r, ab, h, two_b, three_b, total_b, hr, rbi, bb, hbp, sf, sh, k, dp,cs, picked, sb, rbi2]
            if (scrapersettings.ind_player_stats == 1):
                writeline = ""
                for item in ind_stats:
                    writeline += str(item) + "\t"
                writeline += str(gamedate) + "\t" + str(neutral)
                #writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                player_data_w.writelines(writeline)

        # Get Away Team Data
        away_results = awaystats.findAll('tr', class_='grey_heading')[-1:]
        tds = away_results[0].findAll('td')
        try:
            # G
            g = str(tds[2].get_text().encode('utf-8').strip())
            g = alphanum.sub('', g)
        except:
            g = "ERROR!"
        try:
            # R
            r = str(tds[3].get_text().encode('utf-8').strip())
            r = alphanum.sub('', r)
        except:
            r = "ERROR!"
        try:
            # AB
            ab = str(tds[4].get_text().encode('utf-8').strip())
            ab = alphanum.sub('', ab)
        except:
            ab = "ERROR!"
        try:
            # H
            h = str(tds[5].get_text().encode('utf-8').strip())
            h = alphanum.sub('', h)
        except:
            h = "ERROR!"
        try:
            # TWO-B
            two_b = str(tds[6].get_text().encode('utf-8').strip())
            two_b = alphanum.sub('', two_b)
        except:
            two_b = "ERROR!"
        try:
            # Three - B
            three_b = str(tds[7].get_text().encode('utf-8').strip())
            three_b = alphanum.sub('', three_b)
        except:
            three_b = "ERROR!"
        try:
            total_b = str(tds[8].get_text().encode('utf-8').strip())
            total_b = alphanum.sub('', total_b)
        except:
            total_b = "ERROR!"
        try:
            hr = str(tds[9].get_text().encode('utf-8').strip())
            hr = alphanum.sub('', hr)
        except:
            hr = "ERROR!"
        try:
            rbi = str(tds[10].get_text().encode('utf-8').strip())
            rbi = alphanum.sub('', rbi)
        except:
            rbi = "ERROR!"
        try:
            bb = str(tds[11].get_text().encode('utf-8').strip())
            bb = alphanum.sub('', bb)
        except:
            bb = "ERROR!"
        try:
            hbp = str(tds[12].get_text().encode('utf-8').strip())
            hbp = alphanum.sub('', hbp)
        except:
            hbp = "ERROR!"
        try:
            sf = str(tds[13].get_text().encode('utf-8').strip())
            sf = alphanum.sub('', sf)
        except:
            sf = "ERROR!"
        try:
            sh = str(tds[14].get_text().encode('utf-8').strip())
            sh = alphanum.sub('', sh)
        except:
            sh = "ERROR!"
        try:
            k = str(tds[15].get_text().encode('utf-8').strip())
            k = alphanum.sub('', k)
        except:
            k = "ERROR!"
        try:
            dp = str(tds[16].get_text().encode('utf-8').strip())
            dp = alphanum.sub('', dp)
        except:
            dp = "ERROR!"
        try:
            sb = str(tds[17].get_text().encode('utf-8').strip())
            sb = alphanum.sub('', sb)
        except:
            sb = "ERROR!"
        try:
            cs = str(tds[18].get_text().encode('utf-8').strip())
            cs = alphanum.sub('', cs)
        except:
            cs = "ERROR!"
        try:
            picked = str(tds[19].get_text().encode('utf-8').strip())
            picked = alphanum.sub('', picked)
        except:
            picked = "ERROR!"
        away_team_stats = [away_team, away_team_name, g, r, ab, h, two_b, three_b, total_b, hr, rbi, bb, hbp, sf, sh, k, dp, sb, cs, picked]

        # Get Home Team Data
        home_results = homestats.findAll('tr', class_='grey_heading')[-1:]
        tds = home_results[0].findAll('td')
        try:
            # G
            g = str(tds[2].get_text().encode('utf-8').strip())
            g = alphanum.sub('', g)
        except:
            g = "ERROR!"
        try:
            # R
            r = str(tds[3].get_text().encode('utf-8').strip())
            r = alphanum.sub('', r)
        except:
            r = "ERROR!"
        try:
            # AB
            ab = str(tds[4].get_text().encode('utf-8').strip())
            ab = alphanum.sub('', ab)
        except:
            ab = "ERROR!"
        try:
            # H
            h = str(tds[5].get_text().encode('utf-8').strip())
            h = alphanum.sub('', h)
        except:
            h = "ERROR!"
        try:
            # TWO-B
            two_b = str(tds[6].get_text().encode('utf-8').strip())
            two_b = alphanum.sub('', two_b)
        except:
            two_b = "ERROR!"
        try:
            # Three - B
            three_b = str(tds[7].get_text().encode('utf-8').strip())
            three_b = alphanum.sub('', three_b)
        except:
            three_b = "ERROR!"
        try:
            total_b = str(tds[8].get_text().encode('utf-8').strip())
            total_b = alphanum.sub('', total_b)
        except:
            total_b = "ERROR!"
        try:
            hr = str(tds[9].get_text().encode('utf-8').strip())
            hr = alphanum.sub('', hr)
        except:
            hr = "ERROR!"
        try:
            rbi = str(tds[10].get_text().encode('utf-8').strip())
            rbi = alphanum.sub('', rbi)
        except:
            rbi = "ERROR!"
        try:
            bb = str(tds[11].get_text().encode('utf-8').strip())
            bb = alphanum.sub('', bb)
        except:
            bb = "ERROR!"
        try:
            hbp = str(tds[12].get_text().encode('utf-8').strip())
            hbp = alphanum.sub('', hbp)
        except:
            hbp = "ERROR!"
        try:
            sf = str(tds[13].get_text().encode('utf-8').strip())
            sf = alphanum.sub('', sf)
        except:
            sf = "ERROR!"
        try:
            sh = str(tds[14].get_text().encode('utf-8').strip())
            sh = alphanum.sub('', sh)
        except:
            sh = "ERROR!"
        try:
            k = str(tds[15].get_text().encode('utf-8').strip())
            k = alphanum.sub('', k)
        except:
            k = "ERROR!"
        try:
            dp = str(tds[16].get_text().encode('utf-8').strip())
            dp = alphanum.sub('', dp)
        except:
            dp = "ERROR!"
        try:
            sb = str(tds[17].get_text().encode('utf-8').strip())
            sb = alphanum.sub('', sb)
        except:
            sb = "ERROR!"
        try:
            cs = str(tds[18].get_text().encode('utf-8').strip())
            cs = alphanum.sub('', cs)
        except:
            cs = "ERROR!"
        try:
            picked = str(tds[19].get_text().encode('utf-8').strip())
            picked = alphanum.sub('', picked)
        except:
            picked = "ERROR!"
        home_team_stats = [home_team, home_team_name, g, r, ab, h, two_b, three_b, total_b, hr, rbi, bb, hbp, sf, sh, k, dp, sb, cs, picked]

        total_team_stats = [game, gamedate] + away_team_stats + home_team_stats

        if (scrapersettings.ind_game_stats == 1):
            writeline = ""
            for item in total_team_stats:
                writeline += str(item) + "\t"
            writeline += str(neutral)
            #writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            game_data_w.writelines(writeline)

        if (scrapersettings.ind_team_stats == 1):
            writeline = str(game) + "\t" + str(gamedate) + "\t"
            if neutral == "1":
                writeline += "Neutral" + "\t"
            else:
                writeline += "Away" + "\t"
            for item in away_team_stats:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            writeline += str(game) + "\t" + str(gamedate) + "\t"
            if neutral == "1":
                writeline += "Neutral" + "\t"
            else:
                writeline += "Home" + "\t"
            for item in home_team_stats:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            team_data_w.writelines(writeline)

    print "Successfully generated individual statistics for players and/or teams"


token = os.environ['DROPBOX_TOKEN']
dbx = dropbox.Dropbox(token)

f5 = open('data/game_data.tsv', 'rb')
response = dbx.files_upload(f5.read(),
'/Heroku_NCAA_D1_Baseball_Data/game_data.tsv', mode=dropbox.files.WriteMode("overwrite"))
f5.close()

f6 = open('data/player_data.tsv', 'rb')
response = dbx.files_upload(f6.read(),
'/Heroku_NCAA_D1_Baseball_Data/player_data.tsv', mode=dropbox.files.WriteMode("overwrite"))
f6.close()

f7 = open('data/team_data.tsv','rb')
response = dbx.files_upload(f7.read(),
'/Heroku_NCAA_D1_Baseball_Data/team_data.tsv', mode=dropbox.files.WriteMode("overwrite"))
f7.close()
