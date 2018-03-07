from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import bs4
import numpy as np


###################### Question 1  ##############################
# - Which team had the most homeruns in the regular season of 2015? Print the full team name.


# scrape data for question 1

######## start from here ########

# Using FireFox driver
driver = webdriver.Firefox(executable_path='./geckodriver')
#driver.close()

driver.get('http://www.mlb.com')
stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item-link--stats')
stats_header_bar.click()

# click again, sometimes it doesn't work so will have to double click.
stats_header_bar.click()

# get the season 2015, id:sp_hitting_season
season_element = driver.find_element_by_id('sp_hitting_season')
season_element.click()
season_select = Select(season_element)
season_select.select_by_value('2015')

# get the regular season id:sp_hitting_game_type
gametype_element = driver.find_element_by_id('sp_hitting_game_type')
gametype_element.click()
gametype_select = Select(gametype_element)
gametype_select.select_by_value("'R'")

# get team button
content_wrap_stats = driver.find_element_by_id('contentWrap')
# click team button
team_bar = content_wrap_stats.find_element_by_id('st_parent')
team_bar.click()

# get the data of all team and sort by the HR(home run)
hr_bottom = driver.find_element_by_tag_name('thead')
hr = hr_bottom.find_element_by_class_name('dg-hr')
hr.click()

# get the header
data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html,'html5lib')
soup_tr = soup.thead.tr
team_header = [t.text.replace('▼','') for t in soup_tr.findAll('th')]

# get the stats for each team
soup_tbody = soup.tbody
team_stats = []
soup_tbody_tr = soup_tbody.findAll('tr')
for tr in soup_tbody_tr:
    team_detail = [t.text for t in tr.findAll('td')]
    team_stats.append(team_detail)

# print the top1 team
df_hr = pd.DataFrame(data= team_stats, columns=team_header)
top1_hr = pd.DataFrame(df_hr[['Team','HR']].iloc[0])
# top1_hr[0][0]
# print (top1_hr[0][0])
# df_hr

# save the data into "Question_1.csv"
df_hr.to_csv('Question_1.csv', sep=',',index_label=True)

# scrape data for question 1
######## End from here ########


###### Q1. get answer from the csv stored #####

with open ('Question_1.csv', 'r') as q1:
    top1_hr = pd.read_csv(q1, sep= ',' )
        
top1_team_name = top1_hr.iloc[0]['Team']
print ('The answer for Q1:')
print ('The team had the most homeruns in the regular season of 2015 is', top1_team_name,'.')




########################### Question 2################################
# - Which league (AL or NL) had the greatest average number of homeruns…
#   1. in the regular season of 2015? Please give the league name and the average number of homeruns.
#   2. in the regular season of 2015 in the first inning? Please give the league name and the average number of homeruns.


### reade data to answer sub-question 1 of Question 2 #####
with open ('Question_1.csv', 'r') as q2_1:
    df_hr_q2= pd.read_csv(q2_1, sep=',')

al_df = df_hr_q2.loc[lambda df_hr: df_hr.League =='AL', :]
nl_df = df_hr_q2.loc[lambda df_hr: df_hr.League =='NL', :]
nl_mean = np.mean(nl_df['HR'].apply(int))
#print ('The average number of homeruns fo the NL:', nl_mean)
al_mean = np.mean(al_df['HR'].apply(int))
#print ('The average number of homeruns fo the AL:', al_mean)
print ('The answer for question 2.1:')
answer = '{} had the greatest average number of homeruns: {}'
if nl_mean > al_mean:
    print (answer.format('NL', nl_mean))
else:
    print (answer.format('AL', al_mean))



### scrape data to answer sub-question 2 of Question 2 #####
##################### start from here ######################
# get the data for the first inning, id:st_hitting_hitting_splits
split_element = driver.find_element_by_id('st_hitting_hitting_splits')
split_element.click()
split_select = Select(split_element)

# value for the first inning is 'i01'
split_select.select_by_value("i01")

data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html,'html5lib')
soup_thead_tr = soup.thead.tr
team_header_1stin = [t.text.replace('▼','') for t in soup_thead_tr.findAll('th')]
soup_tbody = soup.tbody
team_stats_1stin = []
#for t in soup_tbody:
    #print (t.tr)
soup_tbody_tr = soup_tbody.findAll('tr')
for tr in soup_tbody_tr:
    team_detail = [t.text for t in tr.findAll('td')]
    team_stats_1stin.append(team_detail)
    
df_1stin = pd.DataFrame(data= team_stats_1stin, columns=team_header_1stin)

####save the data for question2.2
df_1stin.to_csv('Question_2_2.csv', sep=',',index_label='INDEX')


### scrape data to answer sub-question 2 of Question 2 #####
##################### End  here ###########################

####### open the saved Question_2_2.csv to answer the sub-question 2 of Question 2
with open ('Question_2_2.csv', 'r') as q22:
    df_1stin= pd.read_csv(q22, sep=',')

al_df_1st = df_1stin.loc[lambda df_hr: df_hr.League =='AL', :]
nl_df_1st = df_1stin.loc[lambda df_hr: df_hr.League =='NL', :]
nl_mean = np.mean(nl_df_1st['HR'].apply(int))
#print (nl_mean)
al_mean = np.mean(al_df_1st['HR'].apply(int))
#print (al_mean)
print ('The answer for question 2.2:')
answer = '{} had the greatest average number of homeruns in the first inning: {}'
if nl_mean > al_mean:
    print (answer.format('NL', nl_mean))
else:
    print (answer.format('AL', al_mean))




############### Question 3 ####################
# - What is the name of the player with the best overall batting average in the 2017 regular season that played for the New York Yankees, who
#    1. had at least 30 at bats? Please give his full name and position.
#    2. played in the outfield (RF, CF, LF)? Please give his full name and position.


##########################
######## Question 3.1#####
######## scrape data for question 3.1 ###########
######## start from here ########################
# continue with the driver from previous status
# get the players page, id: sp_parent
player_element = driver.find_element_by_id('sp_parent')
player_element.click()

# get the Yankees, id:sp_hitting_team_id
yankees = driver.find_element_by_id('sp_hitting_team_id')
yankees.click()
yankees_select = Select(yankees)

# value for NY Yankees is '147'
yankees_select.select_by_value('147')

# get the season 2017
season_element = driver.find_element_by_id('sp_hitting_season')
season_element.click()
season_select = Select(season_element)
season_select.select_by_value('2017')

# get the split
split_element = driver.find_element_by_id('sp_hitting_hitting_splits')
split_element.click()
split_select = Select(split_element)
split_select.select_by_value('')

# player_header
data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html,'html5lib')
soup_thead_tr = soup.thead.tr
player_header = [t.text.replace('▼','').replace('▲', '') for t in soup_thead_tr.findAll('th')]

# player_stats
soup_tbody = soup.tbody
player_stats = []
soup_tbody_tr = soup_tbody.findAll('tr')
for tr in soup_tbody_tr:
    #print(tr)
    player_detail = [t.text for t in tr.findAll('td')]
    #print(team_detail)
    player_stats.append(player_detail)
    
df_player = pd.DataFrame(data= player_stats, columns=player_header)

### save data for all the player in NY Yankees
df_player.to_csv('Question_3.csv', sep=',',index_label=False)

### scrape data to answer Question 3.1 ####################
##################### End  here ###########################


####### open the saved Question_3.csv to answer the question 3.1 ##########

with open ('Question_3.csv', 'r') as q3:
    df_player= pd.read_csv(q3, sep=',')
    
df_player_top = df_player.loc[lambda df_hr: df_player.AB.astype(int) > 30, :]
df_player_top
# df_player_avg = df_player_top.convert_objects(convert_numeric=True)
df_player_top.AVG.astype(float)
df_player_avg = df_player_top.sort_values(['AVG'], ascending=False)
best_player_name = df_player_avg.iloc[0]['Player'].strip()
best_player_pos = df_player_avg.iloc[0]['Pos'].strip()
#df_player_avg
# get the name and position and avg of the top1 player, but we need the full name
player_index = best_player_name[0]
print (best_player_name, best_player_pos)

# get the full name of the best player
# this should be continuely with driver
# could not close the driver or start from the middle
cg = driver.find_element_by_link_text(best_player_name)
cg.click()


full_name = driver.find_element_by_class_name('full-name').text
print ('Full name:', full_name, ';', 'Position:',best_player_pos)
best_p = [[full_name, best_player_pos]]
answer_q3_1 = pd.DataFrame(best_p, columns=['Full Name', 'Position'])
answer_q3_1
# answer_q3.to_csv('Answer_q3.csv', sep=',',index_label=False)


##########################
######## Question 3.2#####

with open ('Question_3.csv', 'r') as q3:
    df_player_q3= pd.read_csv(q3, sep=',')

# df_player_q3= pd.read_csv('Question_3.csv', sep=',')
position = ['RF', 'CF', 'LF']
df_player_outfield = df_player_q3.loc[df_player_q3['Pos'].isin(position)]
df_player_outfield_avg = df_player_outfield.sort_values(['AVG'], ascending=False)
best_outfield_player_name = df_player_outfield_avg.iloc[0].Player.strip()
best_outfield_player_pos = df_player_outfield_avg.iloc[0]['Pos'].strip()
#pd.options.display.max_columns=99

driver.back()
#similar here, you have to continuely run the driver to run the following syntx
ga = driver.find_element_by_link_text(best_outfield_player_name)
ga.click()

full_name2 = driver.find_element_by_class_name('full-name').text
print ('Full name:', full_name2, ';', 'Position:',best_outfield_player_pos)
#driver.close()
best_p = [[full_name, best_player_pos], [full_name2, best_outfield_player_pos]]
answer_q3 = pd.DataFrame(best_p, columns=['Full Name', 'Position'])
#answer_q3 = pd.DataFrame(best_p, columns=['Full Name', 'Position'])

answer_q3.to_csv('Answer_3.csv', sep=',',index_label='INDEX')


################ Question 4 ################
# - Which player in the American League had the most at bats in the 2015 regular season? Please give his full name, full team name, and position.


######## scrape data for question 4 ###########
######## start from here ########################

import random
import time

#driver = webdriver.Firefox(executable_path=r'/Users/xusibocn/Desktop/SIT/Course/BIA 660 Web Analytics/BIA660D_master/Lecture_06/geckodriver')
driver = webdriver.Firefox(executable_path='./geckodriver')
driver.get('http://www.mlb.com')
wait = WebDriverWait(driver, 10)
stats_header_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'megamenu-navbar-overflow__menu-item--stats')))
print('The stats dropdown in the header was loaded successfully. The mouse will move over the element after a short delay')
normal_delay = random.normalvariate(2, 0.5)
stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item-link--stats')

stats_header_bar.click()
stats_header_bar.click()


# get the season 2015
time.sleep(normal_delay)
season_element = driver.find_element_by_id('sp_hitting_season')
season_element.click()
season_select = Select(season_element)
season_select.select_by_value('2015')

# get the regular season
time.sleep(normal_delay)
gametype_element = driver.find_element_by_id('sp_hitting_game_type')
gametype_element.click()
gametype_select = Select(gametype_element)
gametype_select.select_by_value("'R'")

# sort by 'AB'
time.sleep(normal_delay)
ab_bottom = driver.find_element_by_tag_name('thead')
ab = ab_bottom.find_element_by_class_name('dg-ab')
ab.click()

ab_tbody = driver.find_element_by_tag_name('tbody')
data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html,'html5lib')
soup_tbody_tr = soup.tbody.tr
#soup_tbody_tr
player_detail = [t.text.strip() for t in soup_tbody_tr.findAll('td')]
player_name_q4 = player_detail[1].strip()
player_pos = player_detail[5].strip()

# keep the driver open

###### save the scarpe data for the question 4 ####
player_detail = [player_detail]
player_detail_df = pd.DataFrame(player_detail)
player_detail_df.to_csv('Question_4.csv', sep=',',index_label='INDEX')

######## scrape data for question 4 ###########
######## End  here ############################

#get the full name of the team
q4_name = driver.find_element_by_link_text(player_name_q4)
q4_name.click()
team_name = driver.find_element_by_class_name('dropdown.team').text.split('\n')[0].strip()
full_name = driver.find_element_by_class_name('full-name').text
#print ('Full name:', full_name, ';', 'Team:',team_name,';', 'Pos:', player_pos)
best_p4 = [[full_name, team_name, player_pos]]
answer_q4 = pd.DataFrame(best_p4, columns=['Full Name','Team', 'Position'])
print ('The answer for question 4:')
answer_q4
answer_q4.to_csv('Answer_4.csv', sep = ',', index_label='INDEX')

driver.close()


# ## Question 5
# - Which players from the 2014 All-star game were born in Latin America (google a country list)? Please give their full name and the full name of the team they play for.


# latin_coun = '''Argentina;Belize;Bolivia;Brazil;Chile;Colombia;Costa Rica;Ecuador;El Salvador;Falkland Islands;French Guiana;Guatemala;Guyana;Honduras;Mexico;Nicaragua;Panama;Paraguay;Peru;Suriname;Uruguay;Venezuela'''


latin_coun ='''Argentina;Bolivia;Brazil;Chile;Colombia;Costa Rica;Cuba;Dominican Republic;Ecuador;El Salvador;French Guiana;Guadeloupe;Guatemala;Haiti;Honduras;Martinique;Mexico;Nicaragua;Panama;Paraguay;Peru;Puerto Rico;Saint Barthélemy;Saint Martin;Uruguay;Venezuela'''
driver = webdriver.Firefox(executable_path='./geckodriver')
driver.get('http://www.mlb.com')
wait = WebDriverWait(driver, 10)
stats_header_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'megamenu-navbar-overflow__menu-item--stats')))
print('The stats dropdown in the header was loaded successfully. The mouse will move over the element after a short delay')
normal_delay = random.normalvariate(2, 0.5)
stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item-link--stats')
time.sleep(normal_delay)
stats_header_bar.click()
stats_header_bar.click()

# get the season 2015
time.sleep(normal_delay)
season_element = driver.find_element_by_id('sp_hitting_season')
season_element.click()
season_select = Select(season_element)
season_select.select_by_value('2014')

# get the regular season
time.sleep(normal_delay)
gametype_element = driver.find_element_by_id('sp_hitting_game_type')
gametype_element.click()
gametype_select = Select(gametype_element)
gametype_select.select_by_value("'A'")


latin_countries = latin_coun.split(';')
latin_countries

# get the href for each all-star player
data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html,'html5lib')
soup_tbody = soup.tbody
player_name_link_list = []
soup_tbody_tr = soup_tbody.findAll('tr')
for tr in soup_tbody_tr:
    #t.get_attribute('href')
    names = [t.a for t in tr.findAll('td')][1]
    names_link = str(names['href'])
    #print (names_link)
    player_name_link_list.append(names_link)


href_link=[]
player_name_link_list[1]
for a in player_name_link_list:
    href_p = ''.join(["//a[contains(@href, '", a, "')]"])
    href_link.append(href_p)


# scrape the bio for each all-star player

p_detail = []
final = []
for p_name_href in href_link:
    #href= str(''.join(["//a[contains(@href, '", p_name_href, "')]"]))
    newpage_name = driver.find_element_by_xpath(p_name_href)
    #newpage_name = driver.find_element_by_link_text(p_name)
    newpage_name.click()
    wait = WebDriverWait(driver, 10)
    p_bio = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'player-bio'))).text
    #for c in latin_countries:
        #if c in p_bio:
    #p_born = p_bio.text.split('\n')[1]
    #p_full_name = p_bio.text.split('\n')[0]
            #normal_delay = random.normalvariate(2, 0.5)
            #wait = WebDriverWait(driver, 10)
            #p_bio = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'dropdown.team')))
            #p_team_name = driver.find_element_by_class_name('dropdown.team').text.split('\n')[0].strip()
            #p_detail = [p_bio, p_team_name]
            #final.append(p_detail)
    wait = WebDriverWait(driver, 10)
    p_team_name = driver.find_element_by_class_name('dropdown.team').text.split('\n')[0].strip()
    p_detail = [p_bio, p_team_name]
    final.append(p_detail)    
    time.sleep(normal_delay)
    driver.back()
    time.sleep(normal_delay)

# save the data of the question 5
df_final = pd.DataFrame(final , columns=['Bio', 'Team'])
df_final.to_csv('Question_5.csv', sep=',', index_label='Index')

df_final

driver.close()

####### answer question 5 #########
with open ('Question_5.csv') as q5:
    all_star_player = pd.read_csv(q5, sep=',')

latin_countries = latin_coun.split(';')
latin_countries
player_final = []
for a in final:
    for coun in latin_countries:
        if coun in a[0]:
        pp_name = a[0].split('\n')[0]
        pp_team = a[1]
        player_bio = [pp_name, pp_team]
        player_final.append(player_bio)


player_final
#print (final)
df_final = pd.DataFrame(player_final , columns=['Full Name', 'Team'])
df_final
# save the answer for question 5
#df_final.to_csv('Question_5.csv', sep=',',index_label=False)
df_final.to_csv('Answer_5.csv', sep=',', index_label='Index')




################ Question 6 #########################
# - Please print the 2016 regular season schedule for the Houston Astros in chronological order. Each line printed to the screen should be in the following format:
#     - opponent Team Name, game date, stadium name, city, state

############### use api to get all three jsons for extracting needed information

# json for 2016 scheduel
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'ff202b724b714dc3aa66aa292a78b964',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", "/v3/mlb/stats/json/Games/2016?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    #print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

#stat = json.loads(data)

# save json of team scheduel
with open('MLB_v3_Stats_Teams_Active_Schedules.json', 'w') as outfile:
    json.dump(stat, outfile)



#####  json for team

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'ff202b724b714dc3aa66aa292a78b964',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", "/v3/mlb/stats/json/AllTeams?%s" % params, "{body}", headers)
    response = conn.getresponse()
    team = response.read()
    # print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

team_detail = json.loads(team)

with open('MLB_v3_Stats_Teams_Active.json', 'w') as out:
    json.dump(team_detail, out)

# json for stadiums
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'ff202b724b714dc3aa66aa292a78b964',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", "/v3/mlb/stats/json/Stadiums?%s" % params, "{body}", headers)
    response = conn.getresponse()
    stadiums = response.read()
    # print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

with open('MLB_v3_Stats_stadium.json', 'w') as o:
    json.dump(stadium, o)


############################# Api end here ######################


###########################################################################
############# read data from json to get the answer for the question #######
# read json of team scheduel

with open('MLB_v3_Stats_Teams_Active_Schedules.json', 'r') as outfile:
    stat = json.load(outfile)

game = []
for item in stat:
    if item['HomeTeam']=='HOU':
        #team = item['HomeTeam']
        opn_team = item['AwayTeam']
        date= item['DateTime']
        stadium_ID = item['StadiumID']
        opn_ID = item['AwayTeamID']
        #status = item['Status']
        game_detail = [opn_team,opn_ID, date, stadium_ID]
        game.append(game_detail)
    elif item['AwayTeam'] == 'HOU':
        #team = item['AwayTeam']
        opn_team = item['HomeTeam']
        date= item['DateTime']
        stadium_ID = item['StadiumID']
        opn_ID = item['HomeTeamID']
        #status = item['Status']
        game_detail = [opn_team,opn_ID, date, stadium_ID]
        game.append(game_detail)

# get team lookup dict
with open('MLB_v3_Stats_Teams_Active.json', 'r') as out:
    team_detail=json.load(out)

team_lookup = {}
for item in team_detail:
    #print ({item['TeamID']: item['City'] + ' ' +item['Name']})
    ID = item['TeamID']
    Name = item['City'] + ' ' +item['Name']
    team_lookup[ID] = Name

for t in game:
    if t[1] in team_lookup:
        t.append(team_lookup[t[1]])


# get team lookup dict
with open('MLB_v3_Stats_stadium.json', 'r') as o:
    stadium = json.load(o)
    
#stadium = json.loads(stadiums)
stadium

stadium_address_lookup = {}
stadium_name_lookup = {}
for item in stadium:
    if item['Altitude']  != None:
        #print ({item['TeamID']: item['City'] + ' ' +item['Name']})
        ID = item['StadiumID']
        sta = item['City'] + ', ' +item['State']
        stadium_address_lookup[ID] = sta
        
for item in stadium:
    if item['Altitude']  != None:
        #print ({item['TeamID']: item['City'] + ' ' +item['Name']})
        ID = item['StadiumID']
        sta = item['Name']
        stadium_name_lookup[ID] = sta

stadium_name_lookup
for t in game:
    if t[3] in stadium_address_lookup:
        t.append(stadium_address_lookup[t[3]])
        t.append(stadium_name_lookup[t[3]])

# <opponent Team Name> <game date> <stadium name> <city>, <state>
HOU_schedule_list = []
for t in game:
   game_date = t[2][:(t[2].find('T'))]
   game_team = t[4]
   sta_name = t[6]
   location = t[5]
   Hou = [game_team, game_date, sta_name, location]
   HOU_schedule_list.append(Hou)
colname = ['Opponent Team Name', 'Game Date', 'Stadium Name', 'Location']
HOU_schedule = pd.DataFrame(HOU_schedule_list, columns=colname)

# HOU_schedule
HOU_schedule.to_csv('Answer_6.csv', sep=',',index_label=True)
print ('The answer for question 6:')
HOU_schedule

