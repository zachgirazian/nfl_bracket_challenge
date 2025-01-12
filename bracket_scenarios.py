import numpy as np
import xlsxwriter
from pdb import set_trace as stop
import pandas as pd


def load_brackets():
    brackets = pd.read_csv('nfl_brackets.csv')
    N = brackets.shape[1] # of brackets
    
    # Add columns for total bracket points and stirp all text
    for a in brackets.columns:
        brackets[a + 'Pts'] = np.zeros(13)
        for key in brackets:
            brackets[a] = brackets[a].str.strip()
    
    return N, brackets


# Zach Girazian
# z.girazian@gmail.com
# This program calculates all scenarios from the Divisional round on for our annual NFL bracket Challenge
# INPUTS: - Manually enter Wildcard game winners, bye teams, and upcoming divisional games for the year below 
#         - Put all brackets into a csv for loading


# Load everyone's barckets
N, brackets = load_brackets()

# Bye Teams
afcByeTeam = 'Chiefs'
nfcByeTeam = 'Lions'

#Wildcard Games winners
wcGames = ['Texans',  
           'Ravens',
            'Bills',  #Broncos']  
            'Eagles', #,'Eagles']  
            'Rams',  #,'Vikings']
            'Commanders']  #,'Commanders']

# Give points for wildcard weekend
dic = {}
for i, a in enumerate(brackets.columns[0:5]):
    score = 0
    for b in wcGames:
        print(score, a, b)
        if b in brackets[a].str.strip().loc[0:5].values:
            score = score + 1
            dic[a + 'Pts'] = score

# Set divisional matchups based on wildcard winners and seeding
Game1 = ['Eagles','Bucs']
Game2 = ['Lions','Rams']              
Game3 = ['Ravens','Bills']
Game4 = ['Texans','Chiefs']


#Loop through all scenarios and save them
scenarios = []

#Divisional games
for i in range(0,2):
    NFCdiv2 = Game1[i]

    for j in range(0,2):
        AFCdiv2 = Game4[j]

        for k in range(0,2):
            AFCdiv1 = Game3[k]
            
            for l in range(0,2):
                NFCdiv1 = Game2[l]

                #AFC/NFC Championship Games set
                Game5 = [NFCdiv1,NFCdiv2]
                Game6 = [AFCdiv1,AFCdiv2]

                for m in range(0,2):
                    NFCchamp = Game5[m]

                    for n in range(0,2):
                        AFCchamp = Game6[n]

                        #Superbowl set
                        Game7 = [NFCchamp,AFCchamp]

                        for b in range(0,2):
                            Champ = Game7[b]

                            #Save this scenario
                            scenario1 = [AFCdiv1,AFCdiv2,NFCdiv1,NFCdiv2,AFCchamp,NFCchamp,Champ]
                            scenarios.append(scenario1)

#Now loop through each scenario and add everyone's points 
#list to hold winners, points, names, etc.
winner = [] #winner for scenario
winnermax = [] #ignore
winnerpoints = [] #points scored by winner
points = [] #store everyones points fo reach scenario
pointsnames = [] #corresponding names for points
scenarios=np.array(scenarios)
tot = np.shape(scenarios)[0] #number of senarions 
print(tot)

#loop through scenarios
for i in range(0,tot): 
    scenario1 = scenarios[i][:] # pick a scenario

    #points list for each team for this scenarios
    plist = []
    nlist = [] #corresponding name list

    #loop through a everyones bracket and add up points for that scenario
    for key in brackets.columns[0:5]:

        #Divisional
        dv = brackets[key][6:10] 
        dvs = scenario1[0:4]
        checkdv = [1 for hhh in dv if hhh in dvs]
    
        #Championship
        cv = brackets[key][10:12] 
        cvs = scenario1[4:6]
        checkcv = [1 for hhh in cv if hhh in cvs]
        
        #Superbowl
        sv = brackets[key].values[-1] 
        svs = scenario1[-1]
        checksv = 0
        if  sv == svs: checksv = 1
     
        #Now add all points (50  for wildcard, 75 for divisional, 150 for championships, and 300 for superbowl). Also add score from wildcard weekend
        score1 = 50*dic[key+'Pts'] + 75*len(checkdv) + 150*len(checkcv) + 300*checksv 

        plist.append(score1)
        nlist.append(key)

    #max points scored in scenario
    maxp = max(plist)

    #Find out who scored the max points
    namehold = []
    for pp, n in enumerate(nlist):
        if plist[pp] == maxp: namehold.append(n)

    if len(namehold) == 0: stop() #debug

    #make long string of multiple winners
    thewinners = ""
    for kkk in range(0,len(namehold)):
        thewinners = thewinners + namehold[kkk]
        if kkk < len(namehold)-1: thewinners = thewinners + ","
   
   #Store winners, name lists, scenario, etc.
    winner.append(thewinners)
    winnermax.append([scenario1,thewinners])
    winnerpoints.append(maxp)
    points.append(plist)
    pointsnames.append(nlist)  #all are the in the same order


#Sort winners by name
sortedInd = np.argsort(winner) #indices of sorted array
winnerSort = [winner[i] for i in sortedInd]  
winnermaxSort = [winnermax[i] for i in sortedInd]
scenariosSort = [scenarios[i] for i in sortedInd]
winnerpointsSort = [winnerpoints[i] for i in sortedInd]
pointsSort = [points[i] for i in sortedInd]
pointsnamesSort = [pointsnames[i] for i in sortedInd]


# Write csv
workbook = xlsxwriter.Workbook('scenarios_list_edit.xlsx')
worksheet = workbook.add_worksheet()

# Formatting
bold_format = workbook.add_format(properties={'bold': True})
bold_format.set_border(True)

#Write Header
header = []
header1 = ['AFC Div 1', 'AFC Div 2', 'NFC Div 1', 'NFC Div 2', 'AFC Champ', 'NFC Champ', 'SB Champ']
header2 = pointsnamesSort[0]
for h1 in header1: header.append(h1)
for h1 in header2: header.append(h1)
header.append('Winner(s)')

#Write header to csv
row,col = 0,0
for h1 in header: 
    worksheet.write(row,col,h1,bold_format)
    col = col+1

# Load Team Colors
colordf = pd.read_csv('nfl_teams_info_colors.csv')

#Write each scenario to csv
row,col = 1,0
for s1 in scenariosSort:
    col=0
    for s2 in s1:
        # if colors are Nan
        if colordf[colordf['team'] == s2]['color1'].isnull().values[0]:
            formatpick = workbook.add_format({'bold': True,'bg_color':'white', 'font_color': 'black'})
        else:
            formatpick = workbook.add_format({'bold': True,'bg_color':colordf[colordf['team'] == s2]['color1'].values[0], 'font_color': colordf[colordf['team'] == s2]['color2'].values[0]})

        formatpick.set_border(True)
        worksheet.write(row,col,s2,formatpick)
        col = col+1
    row = row+1

#Write everyone's points for each scenario to CSV
#format1 = workbook.add_format(properties={'border': True, 'bold': True})
row = 1
for s1 in pointsSort:
    col=7
    for s2 in s1:
        worksheet.write(row,col,s2)#,format1)
        col = col+1
    row = row+1

#Write winner for each scenario to CSV
row,col=1,7+N
for s1 in winnerSort:
    worksheet.write(row,col,s1)#,format1)
    row = row+1

workbook.close()

