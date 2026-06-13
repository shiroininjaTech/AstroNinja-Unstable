
"""
   This the Library file for the backend graph module for AstroNinja, a space launch tracker and space news app for the
   Linux desktop. It scrapes data from spacelaunchnow.com and displays it in an interactive GUI using beautiful soup
   and PyQt5.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.80
   * Date Created: 01/11/18
   * Date Modified: 06/12/26
"""

import AstroNinjaMainV80
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import astroNinja80
import time, os
import calendar
from dateutil import parser
from datetime import date
import re
import requests, bs4

#missionCount = 3
my_date = date.today()


# A function to tally how many launches each agency has in a given month.
# Takes monthCount as x and missionCount as y
def tally_ho(x, y):

    # tally_ho uses functions from astroNinja to tally the launch counts.
    astroNinja80.getSchedule()
    astroNinja80.scheduleList.append('Ah')
    astroNinja80.launchHead2.append('Ah')
    #print(astroNinja80.launchHead2)
    # The variables that keep count of the agency Tallies
    global spaceXCount
    global chinaCount
    global ulaCount
    global indiaCount
    global rocketCount
    global japaneseCount
    global arianeCount
    global russiaCount
    global northCount
    global euroCount
    global virginCount

    spaceXCount = 0
    chinaCount = 0
    ulaCount = 0
    indiaCount = 0
    rocketCount = 0
    japaneseCount = 0
    arianeCount = 0
    russiaCount = 0
    northCount = 0
    euroCount = 0
    virginCount = 0

    # A function to that tallies launches based on orginization
    # Takes changedSlice2 as an arguement
    def countDracula(a):

        global spaceXCount
        global chinaCount
        global ulaCount
        global indiaCount
        global rocketCount
        global japaneseCount
        global arianeCount
        global russiaCount
        global northCount
        global euroCount
        global virginCount

        # If launch is in the current month and matches with keywords, then add to the tally variable for that agency.
        # Then increment both month count and mission count by 4.
        if todaySlice == a and changedSlice >= todaydateStr :
             if 'SpaceX' in astroNinja80.scheduleList[y]:
                 spaceXCount += 1
             elif 'Chinese' in astroNinja80.scheduleList[y]:
                 chinaCount += 1
             elif 'Arianespace' in astroNinja80.scheduleList[y]:
                 arianeCount += 1
             elif 'India' in astroNinja80.scheduleList[y]:
                 indiaCount += 1
             elif 'United Launch Alliance' in astroNinja80.scheduleList[y]:
                 ulaCount += 1
             elif 'Rocket Lab' in astroNinja80.scheduleList[y]:
                 rocketCount += 1
             elif 'Japan' in astroNinja80.scheduleList[y]:
                 japaneseCount += 1
             elif 'Russian' in astroNinja80.scheduleList[y]:
                 russiaCount += 1
             elif 'Eurockot' in astroNinja80.scheduleList[y]:
                 euroCount += 1
             elif 'Northrop Grumman' in astroNinja80.scheduleList[y]:
                 northCount += 1
             elif 'Virgin Orbit' in astroNinja80.scheduleList[y]:
                 virginCount += 1


    # Haven't found fixes for these, so they're skipped for now.
    brokenDates = ['Early', 'Quarter', 'First Half', 'TBD', 'Spring', 'Mid-2019', 'summer', 'Q1', 'Q2', 'Q3', 'Q4']


    # Iterate over scheduleList until finished
    while x != len(astroNinja80.scheduleList)-1 and y != len(astroNinja80.scheduleList)-1:


        # checking for any of the vague launch dates that cause breakage.
        if any(word in astroNinja80.scheduleList[x] for word in brokenDates) :
            x += 4
            y += 4

        # First we start with some conditionals that check for breaking characters in the launch month and correct them before continuing
        elif 'Approx.' in astroNinja80.scheduleList[x] :
            later = astroNinja80.scheduleList[x].replace('Approx. ', '') # removing breaking characters
            slicy = later[0:3]
            #print(slicy)
            # converting scheduleList[x] so that it can be compared to the current month.
            test = parser.parse(slicy)
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4


        elif 'Mid-' in astroNinja80.scheduleList[x] and 'Mid-2019' not in astroNinja80.scheduleList[x]:
            later = astroNinja80.scheduleList[x].replace('Mid-', '') # removing breaking characters
            slicy = later[0:3]
            #print(slicy)
            # converting scheduleList[x] so that it can be compared to the current month.
            test = parser.parse(slicy)
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]


            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4


        elif 'Late' in str(astroNinja80.scheduleList[x]):
            later = astroNinja80.scheduleList[x].replace('Late ', '') # removing breaking characters
            #print(later)
            slicy = later[0:4]
            #print(slicy)
            # converting scheduleList[x] so that it can be compared to the current month.
            test = parser.parse(slicy)
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4

        elif 'Mid/Late' in astroNinja80.scheduleList[x] :
            later = astroNinja80.scheduleList[x].replace('Mid/Late ', '') # removing breaking characters
            #slicy = later[0:3]
            #print(later)
            # converting scheduleList[x] so that it can be compared to the current month.
            test = parser.parse(later)
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4



        elif '/' in astroNinja80.scheduleList[x]:
            monthString = astroNinja80.scheduleList[x]
            noSlash = re.sub('/.*', '', monthString)
            #print(noSlash)             # Removing breaking characters
            # converting scheduleList[x] so that it can be compared to the current month.
            test = parser.parse(noSlash)
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            #print(changedSlice)
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4


        elif 'NET' in astroNinja80.scheduleList[x]:
            netMonth = astroNinja80.scheduleList[x]
            noNet = netMonth[4:]      # cutting out characters that cause a crash and miscount.
            # converting scheduleList[x] so that it can be compared to the current month.
            test = parser.parse(noNet)
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4


        elif '/' and 'NET' in astroNinja80.scheduleList[x]:
            monthString = astroNinja80.scheduleList[x]
            #print(monthString)
            noNet = monthString[4:]
            #noSlash = noNet[0:3]               # Removing breaking characters
            # converting scheduleList[x] so that it can be compared to the current month.
            test = parser.parse(noSlash)
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4



        else:
            # converting scheduleList[x] so that it can be compared to the current month.
            #print(astroNinja80.scheduleList[x])
            test = parser.parse(astroNinja80.scheduleList[x])
            changedateStr = str(test)
            changedSlice = changedateStr[0:10]
            todaydateStr = str(my_date)
            todaySlice = todaydateStr[5:7]
            changedSlice2 = changedSlice[5:7]

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4
    #print(spaceXCount)
    #print(chinaCount)   # testing
    #print(japaneseCount)
    #print(ulaCount)
    #print(rocketCount)
    #print(arianeCount)
    #print(indiaCount)
    #print(commieCount)

    return

"""
    A Function that scrapes launch history from rocketlaunch.live and tallies it.
    It then passes the counts to AstroNinjaMain to build a graph of previous launch
    Counts in the GUI.

    Takes a year in string form as year
"""
def historian(year):

    # getting the site
    historyURLs = ('https://www.rocketlaunch.live/?pastOnly=1&page=1', 'https://www.rocketlaunch.live/?pastOnly=1&page=2','https://www.rocketlaunch.live/?pastOnly=1&page=3', 'https://www.rocketlaunch.live/?pastOnly=1&page=4', 'https://www.rocketlaunch.live/?pastOnly=1&page=5', 'https://www.rocketlaunch.live/?pastOnly=1&page=6', 'https://www.rocketlaunch.live/?pastOnly=1&page=7', 'https://www.rocketlaunch.live/?pastOnly=1&page=8', 'https://www.rocketlaunch.live/?pastOnly=1&page=9', 'https://www.rocketlaunch.live/?pastOnly=1&page=10',  'https://www.rocketlaunch.live/?pastOnly=1&page=11', 'https://www.rocketlaunch.live/?pastOnly=1&page=12', 'https://www.rocketlaunch.live/?pastOnly=1&page=13', 'https://www.rocketlaunch.live/?pastOnly=1&page=14', 'https://www.rocketlaunch.live/?pastOnly=1&page=15','https://www.rocketlaunch.live/?pastOnly=1&page=16', 'https://www.rocketlaunch.live/?pastOnly=1&page=17', 'https://www.rocketlaunch.live/?pastOnly=1&page=18', 'https://www.rocketlaunch.live/?pastOnly=1&page=19', 'https://www.rocketlaunch.live/?pastOnly=1&page=20', 'https://www.rocketlaunch.live/?pastOnly=1&page=21', 'https://www.rocketlaunch.live/?pastOnly=1&page=22', 'https://www.rocketlaunch.live/?pastOnly=1&page=23')

    def getPage(url):
        print('Indexing {0}......'.format(url))
        result = requests.get(url)


        return result

    dateText = []
    orgText = []

    results = map(getPage, historyURLs)
    for result in results:
        historySite = result
        historySite.raise_for_status()

        # Parsing
        historyHtml = bs4.BeautifulSoup(historySite.text, "lxml")
        #good_html = historyHtml.prettify()
        launchDates = historyHtml.find_all('div', class_="large-2 medium-2 small-3 columns") # Getting the launch date from the site

        # Select date elements directly (more robust than relying on container classes)
        date_items = historyHtml.select('.launch_datetime.rlt_datetime')
        for item in date_items:
            text = item.get_text(separator=' ', strip=True)
            text = re.sub(r'\n', '', text)
            try:
                parsed = str(parser.parse(text))
            except Exception:
                continue
            dateText.append(parsed)

        # Getting the Organisations behind the launch
        launchOrgs = historyHtml.find_all("div", attrs={'class': 'rlt-provider'})
        for i in launchOrgs:
            orgText.append(i.text)

    # A loop iterating through all the dateText and orgText objects, checking
    # for Organization names and matching years. Upon finding a match in date
    # and org, the corresponding variable is increased by one.

    tallyCounty = 0      # variable to be used for iterator

    global spaceXCount
    global chinaCount
    global ulaCount
    global indiaCount
    global rocketCount
    global japaneseCount
    global arianeCount
    global russiaCount
    global northCount
    global euroCount
    global landSpace
    global exPace
    global blueOrigin, orbitalATK

    spaceXCount = 0
    chinaCount = 0
    ulaCount = 0
    indiaCount = 0
    rocketCount = 0
    japaneseCount = 0
    arianeCount = 0
    russiaCount = 0
    northCount = 0
    euroCount = 0
    landSpace = 0
    exPace = 0
    blueOrigin = 0
    orbitalATK = 0

    def pastTally(tallyVar):
        global spaceXCount
        global chinaCount
        global ulaCount
        global indiaCount
        global rocketCount
        global japaneseCount
        global arianeCount
        global russiaCount
        global northCount
        global euroCount
        global landSpace
        global exPace
        global blueOrigin, orbitalATK
        global tallyCounty

        if 'China' in orgText[tallyVar]:
            chinaCount += 1
        elif 'SpaceX' in orgText[tallyVar]:
            spaceXCount += 1
        elif 'Roscosmos' in orgText[tallyVar] or 'Russian Military' in orgText[tallyVar]:
            russiaCount += 1

        elif 'Arianespace' in orgText[tallyVar]:
            arianeCount += 1
        elif "ISRO" in orgText[tallyVar]:
            indiaCount += 1
        elif 'Rocket Lab' in orgText[tallyVar]:
            rocketCount += 1
        elif 'Northrop Grumman' in orgText[tallyVar]:
            northCount += 1
        elif 'JAXA' in orgText[tallyVar]:
            japaneseCount += 1
        elif 'LandSpace' in orgText[tallyVar]:
            landSpace += 1
        elif 'United Launch Alliance' in orgText[tallyVar]:
            ulaCount += 1
        elif 'ExPace' in orgText[tallyVar]:
            exPace += 1
        elif 'Blue Origin' in orgText[tallyVar]:
            blueOrigin += 1
        elif 'Orbital ATK' in orgText[tallyVar]:
            orbitalATK += 1

    #print(len(dateText))
    while tallyCounty < min(len(dateText), len(orgText)):
        #print(tallyCounty)
        if year in dateText[tallyCounty]:
            #print(dateText[tallyCounty])
            #print(orgText[tallyCounty])
            pastTally(tallyCounty)

        tallyCounty += 1
    """
    print("SpaceX %s" % spaceXCount)
    print("China %s" % chinaCount)
    print("Russia %s " % russiaCount)
    print("Ariane %s" % arianeCount)
    print("India %s" % indiaCount)
    print("Rocket labs %s" % rocketCount)
    print("Northrop %s" % northCount)
    print("Japan %s" % japaneseCount)
    print("United %s" % ulaCount)
    print("Blue Origin %s" % blueOrigin)
    """

    # TO-DO : make the loop end early if
    # it reaches the last launch of that year.
    #print('historian: year={}, counts=SpaceX:{}, China:{}, ULA:{}, India:{}, Rocket:{}, JAXA:{}, Ariane:{}, Russia:{}, Northrop:{}, Euro:{}, LandSpace:{}, ExPace:{}, BlueOrigin:{}, OrbitalATK:{}'.format(year, spaceXCount, chinaCount, ulaCount, indiaCount, rocketCount, japaneseCount, arianeCount, russiaCount, northCount, euroCount, landSpace, exPace, blueOrigin, orbitalATK))
    return

#tally_ho(monthCount, missionCount)
#build_Graph()
#historian('2019')
