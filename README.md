# Nikke_UR_Bot
Discord Bot that can save Teams for Union members, Data acquisition using Google Sheets and Discord interactions. Notifications for Union Raid

# Commands
**-start:** command to be put in the list for the current boss<br>
**-hitter:** lists all hitters for current boss<br>
**-boss:** shows information about current boss; HP remaining and hits left<br>
**-notify:** notifies users which boss they want to be pinged/notified about<br>
**-unleashed:** deletes all hitters in the current boss list<br>
**-delete:** deletes one hitter in current boss list<br>
**-add:** Appends data to google sheet<br>
**-teamcheck:** checks which members have available teams<br>
**-profile:** view members' team1, team2, and team3<br>
**-setteam:** set members' team1, team2, and team3<br>
**-use:** command to label which member has used a team. indicated by a strikeout<br>
**-default:** sets all users and their teams to normal/default. no strikeout<br>
**-pvp:** view members' pvp teams<br>
**-pvpteam:** set members' pvp teams<br>
**-clear:** clears members' teams<br>
**-reset:** drops all database tables and recreates them<br>
**-check:** checks which googlesheet is linked and lists current bosses in use<br>
**-r_bot:** restarts the discord bot<br>


# How to set up Google API
<t>**Visit:** https://console.cloud.google.com/ <br>
  __Sign up__ and go to Service Accounts: [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) <br>
  __Create__ a service account. Then go to Actions of that Service account click Manage Keys.<br>
  __Click Add Key__. Create a new key. This will then give you a .json file with information you need for your code.<br>
  Also dont forget to __install__ [GoogleSheetAPI Install](https://console.cloud.google.com/apis/api/sheets.googleapis.com/) and [GoogleDriveAPI Install](https://console.cloud.google.com/apis/api/drive.googleapis.com/) <br>
  
# How to set up the Google Sheet
<t>Ideally you can set up the Google sheet how you want but might have to redo most of the code that is in union_raid.py<br>
  If you would like to avoid that please include these tabs into your Google Sheet with the respected columns<br>
  __Tabs needed:__ **[Config] [Accounts] and [Hits D1]** <--- this can be changed to [UnionRaid] or [Day 1] ...etc. <br>
  Here are some examples below:<br>
  ![Example of Accounts and Google Sheets Tabs!](https://i.gyazo.com/c2cb86b6e754b593b2cf51bf4f663cca.png) "***Notice the Tab Names above***"
  <br>
  ![Example of Column Names!](https://i.gyazo.com/5b6cefe979f5271909d2de34e9851e6d.png)"**Example of Column Names**"
  <br>
  <br>
  <br>
  
# Things to change in the code
<li>First thing to change is the .env file. TOKEN,COMMAND_PREFIX,DB_HOST,DB_PORT,DB_USER,DB_PASSWD,DB_NAME<br></li>
<li>In main.py, union_raid.py, and profile.py: Change all user.id's and channel.id's. Change name_mappings.txt and characters.txt path in profile.py<br></li>
<li>Change the .json file with your path to your key from setting up Google API. The place to replace it is in union_raid.py<br></li>
<li>If you changed Tab Names in the google sheet. Change anything associated with the day and DataFrames from pandas to the respective columns or names. This should be in union_raid.py<br></li>
<li>If you adjust the Google Sheet. Check the Views, menu.py. to adjust for anything you have changed.<br></li>
  
  
# How to set up a service
Assuming that you are in Linux, (which you should be)....To set up a service so that your code auto-starts due to any power off/unexpected crash you should set up a service<br>
To do this follow this format: <br>
  <t>Create a file in the /etc/systemd/system folder with sudo su.<br>
    Name it nikke.service or nikke_bot.service<br>
 __The following should be in the file:__<br>
     `
    
    
     [Unit]
     Description=Nikke UR Bot
     After=multi-user.target

     [Service]
     User="YOUR USERNAME FOR THE SYSTEM"
     Type=idle
     WorkingDirectory=/PATH/TO/Nikke_UR_Bot
     ExecStart=/usr/bin/python /PATH/TO/Nikke_UR_Bot/main.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
    
    
    `   

# Packages




