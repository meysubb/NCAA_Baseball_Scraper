=============================
NCAA Baseball Stats Scraper
Author: Meyappan 
Version: 1.3

1. Updated the create_ind_stats.py function.
2. Added a year Index Dictionary to match year id's 
3. Updated the pitching url for team stats. 

=======
Version: 1.2 
Author: Meyappan 
=======

Author: Meyappan (Edited code by Rodrigo Zamith)

The initial script was written by Rodrigo Zamith for NCAA basketball. I made changes to his script recently when using it to develop my NCAA app (hosted on the shiny website). See other repo.

But most recently, I used the exact structure that Rodrigo used to scrape NCAA baseball data. The NCAA website has the same structure for all sports. 

Currently, the only code that has not been updated yet is create_ind_stats.py



=======
Author: Rodrigo Zamith  
Version: 1.1
=======

Usage
-----
First, edit the scraper settings in `scrapersettings.py`. In particular, be sure to change the two variables at the top, `academic_year` and `year_index`, using the information provided in that file. You can also set what kind of data you'd like saved, and where you'd like it saved.

Then, execute either `ncaab_stats_scraper.sh` or `ncaab_stats_scraper.bat`, depending on your operating system. Alternatively, you can just execute the python files, preferably in this order:

1. create_team_mappings.py
2. create_schedule_mappings.py
3. create_player_mappings_and_agg_stats.py
4. create_ind_stats.py


Requirements
------------
This script requires Python, as well as the urllib2 and BeautifulSoup libraries.


License
--------
This script is licensed under the Mozilla Public License Version 2.0 (see LICENSE file in root folder). TL;DR: feel free to use it commercially, modify it, and distribute it, provided you disclose both the source code and any modifications you make to it.
