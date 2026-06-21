#!/usr/bin/env python3

"""
   This the Library file for the front end modules for AstroNinja, a space launch tracker and space news app for the
   Linux desktop. It scrapes data from spacelaunchnow.com and displays it in an interactive GUI using beautiful soup
   and PyQt5.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.80
   * Date Created:  10/13/17
   * Date Modified: 06/21/26
"""
"""
   * Changelog:
   * Version 0.06: Added a greeting page with data on the next launch. Minor formatting fixes
   * Version 0.10: Added a schedule page with data on the next few launches
   * Version 0.50: Added Space agency logos to the next launch data on welcome tab
   * Version 0.60: Added the new astroGraph module, which tallies the launches remaining in the current month and displays them in
   *               a graph on the new graphs tab. Also added a settings menu with different theme options using the new astroThemes module.
   *               Various other formatting fixes.
   * Version 0.65: Added the new xNews module, which scrapes articles and images from various websites and displays it in the news tab. Added
   *                a new them to astroThemes named broco. Added the function to skip launches on the welcome screen if the date has passed.
   *                Various refactoring of code in the back end modules toward more object orientated solutions. Various formatting fixes.
   *
   * Version 0.70: Refactored various backend functions into reusuable code. Moved launches remaining graph to welcome page. Added ability for
   *                the graph to skip already occured launches. Added the Hubble Views tab, showing the current week's newest image from the
   *                Hubble Space Telescope and previous images. Added multithreading support to the web scraping functions of xNews.py. Added max
   *                launches shown by the launch schedule tab.
   *
   * Version 0.75: Fixed formatting errors when running on Linux Mint. Several icons changed to better fit layout of the gui. Added sources option to the
   *                main menu, giving the user links to view the source websites. An easy to run bash script was added to give the user an easy way to install
   *                the dependancies needed for the program to run. Added multiproccessing support to the scraping functions of xNews.py. Added functionality enabling
   *                graph colors to change with app themes.
   *
   * Version 0.80: Release Version. Font size changes. Added high DPI scaling. Added second graph to welcome
   *                page showing total launches for the current year by org. Changed default theme to the
   *                SpaceX theme, and changed old default theme to 'Marine'. Added ability to skip launches
   *                to the next launch item on welcome page. Added new logos for newly reported companies in launch schedule.
   *                Added the ability to reload window via menu and when choosing a new UI theme. Redesign of Welcome tab.
   *                Added SpaceX lens, a portal to video of the company's last launch or livestream of the current launch. Various bug fixes.
"""

import re
import requests, bs4
import time, os
#from os.path import expanduser
from datetime import date
#import calendar
#from dateutil import parser
import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#from PyQt5 import QtWebEngineCore
#from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl
import astroGraphV80
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import astroThemesV85
import urllib.request
import astroNinja80
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
import astroGraphV80
import urllib.request
import xNews
from configparser import ConfigParser
import http.server
import socketserver
import threading
from PyQt5.QtCore import QUrl

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
# Setting up the GUI window class and methods.

# Getting the relative path of the app, this is added in preparation for packaging.
baseDir = os.path.dirname(__file__)


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        #self.setGeometry(0, 0, 0, 0)
        self.setWindowTitle('AstroNinja')
        self.setWindowIcon(QIcon(os.path.join(baseDir, "Images/Icons/rocket.png")))

        #self.showMaximized()
        self.initUI()

        #self.show()


    # The the method to setup the window.
    def initUI(self):


        # The about button method
        def clickMethod(self):
            aboutBox = QMessageBox()
            aboutBox.setIcon(QMessageBox.Question)
            aboutBox.setWindowTitle("About AstroNinja")
            aboutBox.setText("Version 0.80 TESTING\nCreated By: ShirioNinja Development")
            aboutBox.exec_()

        def sourceMethod(self):
            sourcelinks = ['https://www.spaceflightnow.com', 'https://www.spacenews.com', 'https://www.spacetelescope.org']
            sourceMessage = "Launch Schedule Information From: <br><a href='{}'>     spaceflightnow.com</a><br><br>News Articles From:<br><a href='{}'>spacenews.com</a><br><br>Hubble Images Courtesy Of: <br><a href='{}'>spacetelescope.org</a>".format(sourcelinks[0], sourcelinks[1], sourcelinks[2])
            sourceBox = QMessageBox()
            sourceBox.setIcon(QMessageBox.Information)
            sourceBox.setWindowTitle("Sources")
            sourceBox.setText(sourceMessage)
            sourceBox.exec_()

        """
            Restarts the program
            To be used to reload the window when selecting a new theme
        """
        def restart_program():
            python = sys.executable
            os.execl(python, python, * sys.argv)

        """
            The functions for the Theme menu items
        """
        def Marine():
            themeConfig.set('theme', 'key1', 'marine')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
            restart_program()

        def Spacex():
            themeConfig.set('theme', 'key1', 'spaceX')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
            restart_program()

        def broco():
            themeConfig.set('theme', 'key1', 'broco')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
            restart_program()




        # Selecting newest.
        def newest():
            themeConfig.set('articleSorting', 'key1', 'Newest')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
            restart_program()

        # Selecting oldest.
        def oldest():
            themeConfig.set('articleSorting', 'key1', 'Oldest')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
            restart_program()

        """
            The functions for changing hubble image sortment in the settings menu.
            Added in V0.85
        """

        # Selecting newest.
        def newestHubble():
            themeConfig.set('hubbleSorting', 'key1', 'Newest')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
            restart_program()

        # Selecting oldest.
        def oldestHubble():
            themeConfig.set('hubbleSorting', 'key1', 'Oldest')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
            restart_program()




        # Set the central widget
        central_widget = QWidget(self)          # Create a central widget
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)         # Create a QGridLayout
        central_widget.setLayout(grid_layout)   # Set Layout to central widget

        # Setting fonts
        fontVar = QFont("Noto Sans", 25)        # Create a QFont instance
        fontVar.setBold(True)

        smallerHeader =  QFont("Noto Sans", 17)
        smallerHeader.setBold(True)

        welcomeFont = QFont("Noto Sans", 15)                                # A smaller Font
        welcomeFont.setBold(False)

        basicFont = QFont("Noto Sans", 13)                                # An even smaller Font
        basicFont.setBold(False)
        #=================================================================================================
        # Setting up the theme config file
        #=================================================================================================

        # initialize
        # Checking if the config file is present, and making one if it isnt. This prevents the configuration from being over written.

        global sortingSelected, HubblesortingSelected, versionSelected, themeConfig

        if not os.path.isfile(os.path.join(baseDir, "config.ini")):
            themeConfig = ConfigParser()
            themeConfig.read(os.path.join(baseDir, "config.ini"))
            themeConfig.add_section('theme')
            themeConfig.set('theme', 'key1', 'spaceX')
            themeSelected = themeConfig.get('theme', 'key1')
            # Adding a section in the config.ini for storing options in article sorting.
            themeConfig.add_section('articleSorting')
            themeConfig.set('articleSorting', 'key1', 'Newest')
            sortingSelected = themeConfig.get('articleSorting', 'key1')
            # Adding a section in the config.ini for storing options in hubble sorting.
            themeConfig.add_section('hubbleSorting')
            themeConfig.set('hubbleSorting', 'key1', 'Newest')
            HubblesortingSelected = themeConfig.get('hubbleSorting', 'key1')

            # Adding a section in the config.ini for storing update options.
            themeConfig.add_section('Updates')
            themeConfig.set('Updates', 'key1', 'Stable')
            versionSelected = themeConfig.get('Updates', 'key1')

            with open(os.path.join(baseDir, "config.ini"), 'w') as f:
                themeConfig.write(f)
        elif os.path.isfile(os.path.join(baseDir, "config.ini")):
            themeConfig = ConfigParser()
            themeConfig.read(os.path.join(baseDir, "config.ini"))
            themeSelected = themeConfig.get('theme', 'key1')
            # Getting the sorting setting last set by the user.
            #global sortingSelected
            sortingSelected = themeConfig.get('articleSorting', 'key1')
            # Getting the sorting setting for hubble images last set by the user.
            HubblesortingSelected = themeConfig.get('hubbleSorting', 'key1')
            # Getting the Update option selected by the user.
            versionSelected = themeConfig.get('Updates', 'key1')


        #=================================================================================================
        # Creating tabs in the UI
        #=================================================================================================

       # Initilizing tabs
        self.tabs = QTabWidget()
        self.welcomeTab = QWidget()
        self.scheduleTab = QWidget()
        #self.graphTab = QWidget()
        self.spacexTab = QWidget()
        self.stellarTab = QWidget()
        self.issTab = QWidget()


        if themeSelected == 'marine':
            astroThemesV85.defaultTabs(self.welcomeTab, self.scheduleTab, self.stellarTab, self.tabs, self.spacexTab, self.issTab)
        if themeSelected == 'spaceX':
            astroThemesV85.spacexTabs(self.welcomeTab, self.scheduleTab, self.stellarTab, self.tabs, self.spacexTab, self.issTab)
            self.setStyleSheet("QMainWindow { background-color: White; color: White; }")
        if themeSelected == 'broco':
            astroThemesV85.brocoTabs(self.welcomeTab, self.scheduleTab, self.stellarTab, self.tabs, self.spacexTab, self.issTab)
            self.setStyleSheet("QMainWindow { background-color: Black; color: Black; }")


        self.tabs.addTab(self.welcomeTab, "Welcome")
        self.tabs.addTab(self.scheduleTab, "Launch Schedule")
        self.tabs.addTab(self.spacexTab, "News")
        self.tabs.addTab(self.stellarTab, "Stellar Views")
        self.tabs.addTab(self.issTab, "ISS Portal")



        #=========================================================================================================
        # All the functions needed to build a UI for a PyQt5 App
        #=========================================================================================================

        # a function for creating and configuring frame items
        # (a) is the layout that the frame is to be added to
        # (b) is the first position value
        # (c) is the second position value
        # (e) is a toggle for if it is an inner frame

        def frameBuilder(a, b, c,  d, e ):
            self.frame = QFrame()

            self.frame.setFrameShape(QFrame.Box)
            #self.nextframe.setFixedSize(150, 150)
            self.frame.adjustSize()
            a.addWidget(self.frame, b, c)
            if e == False:
                global frameLayout
            frameLayout = QGridLayout()
            self.frame.setLayout(frameLayout)
            frameLayout.setHorizontalSpacing(25)
            a.setColumnMinimumWidth(1, d)



        # A function that adds verticle margins to layouts
        # Takes the layout it is to be added to as "a"
        # "b" and "c" are the x and y dimensions
        def vert_Spacer(a, b, c):
            verticalSpacer = QSpacerItem(b, c, QSizePolicy.Maximum, QSizePolicy.Expanding)
            a.addItem(verticalSpacer, 3, 0)
            a.addItem(verticalSpacer, 3, 3)


        # A function for creating scroll objects
        # gets the tab/location the scroll is to be inserted as location
        # gets the x and y coordinates as x and y
        global scroll
        def scrollBuilder(location, x, y):
            global scroll
            scroll = QScrollArea(self)

            # Creating the style sheet for the scroll bar colors.


            location.addWidget(scroll, x, y)
            scroll.setWidgetResizable(True)
            #scroll.setMinimumHeight(50)
            scrollContent = QWidget(scroll)
            scroll.layout = QGridLayout(scrollContent)
            scrollContent.setLayout(scroll.layout)

            scroll.setWidget(scrollContent)

        # A function that builds headers
        # (a) is the message string
        # (b) is the first position variable
        # (c) is the second position variable
        # (d) is the layout that the label is to be added to
        # (e) is the amount of height given to the header
        def headerBuild(a, b, c, d, e):

            self.header = QLabel(a, self)
            self.header.setAlignment(QtCore.Qt.AlignCenter)
            self.header.setFixedHeight(e)
            self.header.setWordWrap(True)
            self.header.setFont(fontVar)
            self.header.setStyleSheet('QLabel {background: transparent}')
            d.addWidget(self.header, b, c)



        # A quick Qlabel generator
        # (stringVar) is the string to be displayed
        # (xCord and yCord) are the coordinates the label is to be placed at
        # (layout) is the object the label is to be placed in.
        def genLabel(stringVar,xCord, yCord, layout):

            self.label = QLabel(stringVar, self)
            self.label.adjustSize()
            self.label.setWordWrap(True)
            self.label.setMaximumWidth(450)
            self.label.setFont(basicFont)
            layout.addWidget(self.label, xCord, yCord)

        # Adding the most recent Label
        def get_recent():
            astroNinja80.armStrong()
            astroNinja80.nextFlight.append('Ah')
            global recentMessage
            recentMessage = "{}\n\n{}\n\n{}\n\n{}".format(astroNinja80.nextFlight[0], astroNinja80.nextFlight[1], astroNinja80.nextFlight[2], astroNinja80.nextFlight[3])
            self.nextLaunch = QLabel(recentMessage, self)
            self.nextLaunch.setWordWrap(True)
            self.nextLaunch.setMaximumWidth(800)
            self.nextLaunch.setFont(welcomeFont)
            #self.nextLaunch.setAlignment(QtCore.Qt.AlignCenter)
            #self.nextLaunch.resize(30, 30)
            frameLayout.addWidget(self.nextLaunch, 1, 1)
            return recentMessage

        # A function that searches the string in nextFlight[2] for space agency names and displays the agency's logo with the launch data in the next launch.
        # V0.70, added the need for arguement x, which is the item that is to be searched
        def choose_Icon(x):
            global nextLogo
            nextLogo = ''
            if 'SpaceX' in x:
                nextLogo = os.path.join(baseDir, "Images/Logos/spacex.png")
            elif 'Chinese' in x:
                nextLogo = os.path.join( baseDir, "Images/Logos/china.png")
            elif 'United Launch Alliance' in x:
                nextLogo = os.path.join(baseDir, "Images/Logos/ula.png")
            elif 'Arianespace' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/ariane.png")
            elif 'India' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/india.png")
            elif 'Rocket Lab' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/rocketlab.png")
            elif 'Japan' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/Japan.png")
            elif 'Russian' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/russia.png")
            elif 'Pegasus' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/nasa2.png")
            elif 'Eurockot' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/eurockot.png")
            elif 'International Launch Services' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/ILS.png")
            elif 'Northrop Grumman' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/northop.png")
            elif 'Virgin Orbit' in  x:
                nextLogo = os.path.join(baseDir, "Images/Logos/virginorbit.png")
            elif 'Astra' in x:
                nextLogo = os.path.join(baseDir, "Images/Logos/astra.png")
            else:
                nextLogo = ''
            return nextLogo

        # a function to ad an agency logo to the launch schedule item
        # gets the tab layout it is to be added to as tab
        # a and b are positions for the icon
        # search item is the item choose_Icon() is to search

        def recent_logo(tab, a, b, searchItem):
            choose_Icon(searchItem)
            self.nextLogo = QLabel(self)
            self.nextLogo.setStyleSheet('QLabel {background: transparent}')
            iconPix = QPixmap(nextLogo)
            self.nextLogo.setPixmap(iconPix)
            self.nextLogo.setAlignment(QtCore.Qt.AlignCenter)
            self.nextLogo.setMaximumWidth(400)

            #self.nextLaunch.resize(30, 30)
            tab.addWidget(self.nextLogo, a, b)


        # A function that create graphs from data passed from backend modules.
        # takes the tally data as tallies
        # takes the unique label for the yLabel as ylabelString
        # takes a string as title
        # takes org list as launchers
        # takes the container it is to be placed in as container
        # and takes x, y placement in the container as x,y

        def graph_maker(tallies, ylabelString, title, launchers, container, x, y):

            self.figure = plt.figure(figsize=(11,5))
            ax = self.figure.add_subplot(111)

            self.canvas = FigureCanvas(self.figure)

            container.addWidget(self.canvas, x, y)

            # Changing the graph colors based on which theme is selected:
            global bg_color, fg_color, bar_color

            if themeSelected == 'marine':
                bg_color = 'White'
                fg_color = 'black'
                bar_color = 'Darkslategray'

            if themeSelected == 'spaceX':
                bg_color = 'White'
                fg_color = 'black'
                bar_color = 'Steelblue'

            if themeSelected == 'broco':
                bg_color = 'black'
                fg_color = 'white'
                bar_color = 'DarkTurquoise'

            # x-coordinates
            xItems = 10
            ind = np.arange(xItems)


            p1 = plt.bar(ind, tallies) #setting the plot

            for item in p1:
                item.set_color(bar_color)

            plt.ylabel(ylabelString, color=fg_color)
            plt.xlabel('Organizations/Nations', color=fg_color)
            plt.title(title, fontsize=17, color=fg_color)
            plt.xticks(ind, launchers, color=fg_color)
            if max(tallies) == 0:
                    plt.yticks(np.arange(0, 2), color=fg_color)
            else:
                plt.yticks(np.arange(0, max(tallies) + 5, 5.0), color=fg_color)

            #plt.style.use(u'dark_background')
            ax.patch.set_facecolor(bg_color)
            #ax.autoscale(enable=True)
            ax.tick_params(axis='x', labelsize=8)
            self.figure.patch.set_facecolor(bg_color)

            # Adding the totals to the bars
            for index,data in enumerate(tallies):
                plt.text(x=index , y =data-data , s=f"{data}" , fontdict=dict(fontsize=8, ha='center', va='bottom', color=bg_color))
            self.canvas.draw()


        # A function that creates web objects, kind of a way to build a webpage into a widget.

        def web_wrapper(urlItem, maxHeight, container, xPos, yPos, vidOb):

            if vidOb == True:
                self.webView = QtWebEngineWidgets.QWebEngineView()     # creating the webengine object
                self.webView.setHtml(urlItem)         # setting the URL
                self.webView.adjustSize()
                self.webView.setMinimumHeight(maxHeight)

                container.addWidget(self.webView, xPos, yPos)

            elif vidOb == False:
                self.webView = QtWebEngineWidgets.QWebEngineView()     # creating the webengine object
                self.webView.setUrl(QUrl(urlItem))         # setting the URL
                self.webView.adjustSize()
                self.webView.setMinimumHeight(maxHeight)

                container.addWidget(self.webView, xPos, yPos)

        # A better function to create label widgets in PyQt5.
        # Takes the string to be shown as message.
        # Justification is set with alignment,
        # font size is set with font
        # width sets maximum width of the label.
        # container is where the label is to be placed.
        def label_maker(message, alignment, font, width, container, xpos, ypos):

            self.label = QLabel(message, self)
            self.label.adjustSize()
            self.label.setWordWrap(True)
            self.label.setAlignment(alignment)
            self.label.setMaximumWidth(width)
            self.label.setFont(font)

            container.addWidget(self.label, xpos, ypos)







        #==========================================================================================
        # Creating the first tab. The welcome tab that contains a welcome message, the next launch,
        # and the graph showing launches remaining.
        #==========================================================================================

        # Configuring the tab's layout
        self.welcomeTab.layout =  QGridLayout()
        #self.welcomeTab.layout.setRowStretch(1, 5)

        # Building the scrollbars
        firstScroll = scrollBuilder(self.welcomeTab.layout, 1, 1)

        # Adding a verticle spacer
        vert_Spacer(scroll.layout, 250, 250)

        # Adding Horizontal spacers inbetween frame items
        horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum)          # Top H spacer
        scroll.layout.addItem(horizSpacer, 0, 1)
        horizSpacer = QSpacerItem(20, 20, QSizePolicy.Maximum)          # Resizing for middle spacers
        scroll.layout.addItem(horizSpacer, 2, 1)
        scroll.layout.addItem(horizSpacer, 4, 1)
        scroll.layout.addItem(horizSpacer, 6, 1)
        # Building the frame to put the next launch icon and description
        frameBuilder(scroll.layout, 0, 1, 750, False)
        # Running the function that uses the backend module that scrapes the data needed
        # to display the next launch. Also builds the label object
        headerBuild("Next Launch", 0, 1, frameLayout, 60)
        self.header.setAlignment(QtCore.Qt.AlignLeft)

        get_recent()
        # Choosing the right agency logo and placing it in the frame
        recent_logo(frameLayout, 1, 0, recentMessage)

        #================================================================================================
        # Attempting to add a YouTube stream as an object in the first tab
        #================================================================================================

        # Running the backend function that get's the url of the embed version of the newest
        # video by the SpaceX youtube channel.
        # Also will enable the livestreaming of launches.
        """
        youtubeTest.testFlight()
        self.spacexView = QtWebEngineWidgets.QWebEngineView()     # creating the webengine object
        self.spacexView.setUrl(QUrl(youtubeTest.fullURL))         # setting the URL to the one scraped by testFlight()

        # Building the SpaceX Lens object
        frameBuilder(scroll.layout, 3, 1, 750, False)
        frameLayout.addItem(horizSpacer, 1, 1)
        vert_Spacer(frameLayout, 20, 20)
        frameLayout.addWidget(self.spacexView, 2, 1)
        frameLayout.addItem(horizSpacer, 3, 1)

        # building the header frame
        frameBuilder(frameLayout, 0, 1, 650, False)
        self.frame.setLineWidth(5)
        windowMessage = "SpaceX Lens"
        headerBuild(windowMessage, 0, 0, frameLayout, 50)
        # The mission name header
        missionTitle = "%s" % youtubeTest.newestName
        headerBuild(missionTitle, 0, 2, frameLayout, 50)
        
            Use a smaller font for the mission title if it's
            longer than 25 char. This prevents cutting off of
            parts of the header.
        
        if len(missionTitle) >= 25:
            self.header.setFont(smallerHeader)

        # Building a Verticle divider Item with QFrame()
        vDivider  = QFrame()
        vDivider.setFrameShape(QFrame.VLine)
        vDivider.setLineWidth(3)
        frameLayout.addWidget(vDivider, 0, 1)
        """

        #============================================================================================================================
        # Adding the Mars Weather service to AstroNinja.
        # A simple embed using QtWebEngineWidgets as a container.
        # Added in Version 0.85
        #============================================================================================================================

        # Building the Mars Meteorologist  Object
        frameBuilder(scroll.layout, 2, 1, 750, False)
        frameLayout.addItem(horizSpacer, 1, 1)
        vert_Spacer(frameLayout, 20, 20)
        web_wrapper("https://mars.nasa.gov/layout/embed/image/mslweather/", 720, frameLayout, 2, 1, False)
        frameLayout.addItem(horizSpacer, 3, 1)

        # building the header frame
        frameBuilder(frameLayout, 0, 1, 650, False)
        self.frame.setLineWidth(5)

        marsTitle = "Mars Weather Service"
        headerBuild(marsTitle, 0, 0, frameLayout, 50)
        
        # This was for iterating the postions of the items in the tab, in case one item didn't load. not used yet in this version.
        #itemPosition += 1

        #=============================================================================================================================
        # Creating the graph that shows launches remaining.
        # Moved from own tab in Version 0.70
        #=============================================================================================================================
        # counters for the tallying funtion
        global monthCount
        global missionCount
        monthCount = 0                                   # For iterating over the launchHead2 Items
        missionCount = 3                                 # For iterating over the descriptionMissfin items
        astroGraphV80.tally_ho(monthCount, missionCount)    # the meat and bones of the graph feature

        # the tallies
        remainingTallies = [astroGraphV80.spaceXCount, astroGraphV80.chinaCount, astroGraphV80.japaneseCount, astroGraphV80.ulaCount, astroGraphV80.rocketCount, astroGraphV80.indiaCount, astroGraphV80.arianeCount, astroGraphV80.russiaCount, astroGraphV80.northCount, astroGraphV80.euroCount]

        # The Organizations
        orgs = ('SpaceX', 'China', 'JAXA', 'ULA', 'Rocket\nLabs', 'India', 'ArianeSpace', 'Russia', 'Northrop', 'Eurockot')

        graph_maker(remainingTallies, 'Launches Remaining', 'Launches Remaining for This Month by Organization\n', orgs, scroll.layout, 3, 1)

        #=============================================================================================================================
        # Creating the second graph that shows total launches so far for the year
        # added in Version 0.80
        #=============================================================================================================================


        """  
            After so many years, I finally created a sane way of changing years to tally
            without doing it manually. 
        """
        my_date = date.today()

        currentYear  = str(my_date.year)
        previousYear = str(my_date.year-1)    # The current year minus one.

        # Running function that scrapes launch history in the backend module
        totals = astroGraphV80.historian(currentYear)

        # The tallies (use values returned by historian)
        historyTallies = [
            totals.get('spaceX', 0),
            totals.get('china', 0),
            totals.get('ula', 0),
            totals.get('india', 0),
            totals.get('rocket', 0),
            totals.get('japanese', 0),
            totals.get('ariane', 0),
            totals.get('russia', 0),
            totals.get('north', 0),
            totals.get('blueOrigin', 0),
        ]

        # The Organizations
        orgs = ('SpaceX', 'China', 'ULA', 'India', 'Rocket\nLabs', 'Japan', 'Ariane\nSpace', 'Russia', 'Northrop', 'Blue\nOrigin')

        # Making year progression automatic.
        titleStr = 'Total Launches For %s by Organization\n' % currentYear

        graph_maker(historyTallies, 'Launch Totals', titleStr, orgs, scroll.layout, 4, 1)
        #itemPosition += 1

        #=================================================================================================
        # Creating the third graph, which shows  the total launches for the previous year
        # Added V0.85
        #=================================================================================================

        # Running function that scrapes launch history in the backend module
        astroGraphV80.historian(previousYear)

        # The tallies
        historyTallies = [astroGraphV80.spaceXCount, astroGraphV80.chinaCount, astroGraphV80.ulaCount, astroGraphV80.indiaCount, astroGraphV80.rocketCount, astroGraphV80.japaneseCount, astroGraphV80.arianeCount, astroGraphV80.russiaCount, astroGraphV80.northCount, astroGraphV80.blueOrigin]

        titleStr = 'Total Launches For %s by Organization\n' % previousYear

        graph_maker(historyTallies, 'Launch Totals', titleStr, orgs, scroll.layout, 5, 1)

        self.welcomeTab.setLayout(self.welcomeTab.layout)

        #=================================================================================================
        # The second tab, which contains the complete launch schedule.
        #=================================================================================================


        # Configuring the tab
        self.scheduleTab.layout = QGridLayout()
        # Building the header
        scheduleHeader = "Launch Schedule"
        headerBuild(scheduleHeader, 0, 0, self.scheduleTab.layout, 50)



        # Running the schedule scraping function from the astroNinja module
        astroNinja80.getSchedule()
        astroNinja80.scheduleList.append('Ah')

        # A function that adds verticle margins to layouts
        # Takes the layout it is to be added to as "a"
        # "b" and "c" are the x and y dimensions
        def vert_Spacer(a, b, c):
            verticalSpacer = QSpacerItem(b, c, QSizePolicy.Maximum, QSizePolicy.Expanding)
            a.addItem(verticalSpacer, 2, 0)
            a.addItem(verticalSpacer, 2, 4)

        # Building the scroll bar for the schedule. scrollBuilder() added V.75
        scrollBuilder(self.scheduleTab.layout, 1, 0)
        # A function to automate the adding of schedule items and their icons to the launch schedule.
        def launch_scheduleBuild(a, b, c, d, e):

            # Building the frame for the item created by launch_scheduleBuild()
            frameBuilder(scroll.layout, e, 1, 300, False)
            # Building the label
            scheduleItem = "{}\n\n{}\n\n{}\n\n{}\n\n".format(astroNinja80.scheduleList[a],astroNinja80.scheduleList[b],astroNinja80.scheduleList[c],astroNinja80.scheduleList[d])
            label_maker(scheduleItem, QtCore.Qt.AlignLeft, basicFont, 800, frameLayout, 0, 0)

            #frameLayout.addWidget(self.itemLabel)
            scroll.layout.addWidget(self.frame, e, 2)

            # getting the agency logo for each item
            recent_logo(scroll.layout, e, 1, scheduleItem)



        # calling launch_scheduleBuild() for the schedule entries. the first three arguments correspond with
        # items from the scheduleList in the back end module.
        #
        # The last arguement correspond with the item number in the schedule, and set what position the item
        # appears in.


        # The variables that are to be used to advance launch_scheduleBuild through each schedule item
        # Must be declared as global outside of iterator function and within it
        global firstCount, secondCount, thirdCount, fourthCount, position

        skipCount = 0
        firstCount = 0
        secondCount = 1
        thirdCount = 2
        fourthCount = 3
        position = 1
        # Running the function that updates the date variable of the first shedule item
        astroNinja80.update_launch(skipCount)

        """
            Iterate through each schedule item while each date is older than
            todays.
        """
        while astroNinja80.comparedList[0] > astroNinja80.comparedList[1]:
            skipCount += 1
            firstCount += 4
            secondCount += 4                        # advance by 4 to skip to the next launch in scheduleList
            thirdCount += 4
            fourthCount += 4
            astroNinja80.update_launch(skipCount)     # update to the next schedule item
                                                    # after iterating the counter

        # building a function that iterates through schedule items and builds each
        # one into it's own UI item
        def schedule_iterator(a, b, c, d, e):
            launch_scheduleBuild(a, b, c, d, e)
            global firstCount, secondCount, thirdCount, fourthCount, position
            firstCount += 4
            secondCount += 4                        # advance by 4 to skip to the next launch in scheduleList
            thirdCount += 4
            fourthCount += 4
            position += 1
            return

        # run the iterator until it reaches the end of the schedule list provided by the backend
        while fourthCount < len(astroNinja80.scheduleList):
            schedule_iterator(firstCount, secondCount, thirdCount, fourthCount, position)

        vert_Spacer(scroll.layout, 250, 250)
        self.scheduleTab.setLayout(self.scheduleTab.layout)

        #============================================================================================================================
        # The News tab, showing news articles scraped by xNews.py
        #============================================================================================================================

        self.spacexTab.layout =  QGridLayout()

        # xNews scraping moved to before QApplication to avoid Qt thread conflicts

        # A simple fix to remove duplicate articles from showing up in News page
        #fixed_titleList = list(dict.fromkeys(xNews.titleList))
        #fixed_bodyList = list(dict.fromkeys(xNews.bodyList))
        #fixed_imageList = list(dict.fromkeys(xNews.imageList))


        # Building the scroll bar for the schedule. scrollBuilder() added V.75
        scrollBuilder(self.spacexTab.layout, 0, 0)

        # An function based on launch_scheduleBuild that builds out the list of articles in the GUI
        # a is the position of the item in titleList
        # b is the position of the item in bodyList
        # c is the position of the item in the gui.
        # d is the position of the item in imageList
        def newsListBuilder(a, b, c, d):

            # Building the frame for the item created by launch_scheduleBuild()
            frameBuilder(scroll.layout, c, 1, 1000, False)


            # Building the label
            titleVar = "{}".format(xNews.titleList[a])
            bodyVar = "{}\n\n".format(xNews.bodyList[b])
            # setting the label for the title of the article
            headerBuild(titleVar, 0, 2, frameLayout, 150)

            self.image= QLabel(self)

            """
                Using modern urllib with Mozilla user agent to mask the scraper.
                Gets around Admins blocking urllib scrapers on their websites.
            """
            image_data = None
            try:
                req = urllib.request.Request(xNews.imageList[d])
                req.add_header('User-Agent', 'Mozilla/5.0')
                response = urllib.request.urlopen(req, timeout=15)
                if '\u2014' not in xNews.imageList[d]:
                    image_data = response.read()
            except Exception as e:
                print('News image load failed:', xNews.imageList[d], e)

            if image_data:
                artmap = QPixmap()
                artmap.loadFromData(image_data)
                self.image.setPixmap(artmap)
            else:
                self.image.setText('Image unavailable')
                self.image.setAlignment(QtCore.Qt.AlignCenter)

            self.image.adjustSize()
            frameLayout.addWidget(self.image, 2, 2)
            # Adding a space to further seperate the article image and body
            horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum, QSizePolicy.Expanding)
            frameLayout.addItem(horizSpacer, 1, 2)
            frameLayout.addItem(horizSpacer, 3, 2)

            # setting the label for the body of the article
            self.bodyLabel = QLabel(bodyVar, self)
            self.bodyLabel.adjustSize()
            self.bodyLabel.setWordWrap(True)
            self.bodyLabel.setAlignment(QtCore.Qt.AlignLeft)
            self.bodyLabel.setMaximumWidth(900)
            self.bodyLabel.setFont(basicFont)
            frameLayout.addWidget(self.bodyLabel, 4, 2)

            # Adding verticle spacing
            vert_Spacer(scroll.layout, 250, 250)

        # Building an iterator for working through items passed by the backend module
        global countKeeper
        countKeeper = 0
        def iterator(a):
            global countKeeper
            newsListBuilder(a, a, a, a)
            countKeeper += 1

            return

        # Build the news list until we reach the end of the data
        while countKeeper < len(xNews.titleList):
            iterator(countKeeper)

        self.spacexTab.setLayout(self.spacexTab.layout)

        #======================================================================================
        # The Hubble Views tab, which shows the shot of the weeks from the Hubble
        # Space Telescope
        #======================================================================================

        self.stellarTab.layout = QGridLayout()

        # Building the scroll bar. scrollBuilder() added V.75
        scrollBuilder(self.stellarTab.layout, 0, 0)

        # xNews.hubbleViewz() moved to run before QApplication
        # placeholders if needed
        xNews.fullImage.append('Ah')
        xNews.fullDescription.append('Ah')

        def hubbleViewBuilder(b, c, d):

            # Building the frame for the item created by launch_scheduleBuild()
            frameBuilder(scroll.layout, c, 1, 1000, False)


            # Building the label
            bodyVar = "{}\n\n".format(xNews.fullDescription[b])
            # setting the label for the title of the article

            self.image= QLabel(self)
            hubble_data = None
            try:
                hubble_data = urllib.request.urlopen(xNews.fullImage[d], timeout=15).read()
            except Exception as e:
                print('Hubble image load failed:', xNews.fullImage[d], e)

            if hubble_data:
                artmap = QPixmap()
                artmap.loadFromData(hubble_data)
                self.image.setPixmap(artmap)
            else:
                self.image.setText('Image unavailable')
                self.image.setAlignment(QtCore.Qt.AlignCenter)

            self.image.adjustSize()
            frameLayout.addWidget(self.image, 1, 1)
            # Adding a space to further seperate the article image and body
            horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum, QSizePolicy.Expanding)
            frameLayout.addItem(horizSpacer, 0, 2)
            frameLayout.addItem(horizSpacer, 3, 2)

            #vert_Spacer(frameLayout, 100, 100)
            # setting the label for the body of the article
            frameBuilder(frameLayout, 1, 3, 600, True)
            self.bodyLabel = QLabel(bodyVar, self)
            self.bodyLabel.adjustSize()
            self.bodyLabel.setWordWrap(True)
            self.bodyLabel.setAlignment(QtCore.Qt.AlignLeft)
            self.bodyLabel.setMaximumWidth(600)
            self.bodyLabel.setFont(basicFont)
            frameLayout.addWidget(self.bodyLabel, 0, 0)




        vert_Spacer(scroll.layout, 250, 250)



        global hubKeeper
        hubKeeper = 0
        def hubIterator(x):
            hubbleViewBuilder(x, x, x)
            global hubKeeper
            hubKeeper += 1
            return

        while hubKeeper < 16:
            hubIterator(hubKeeper)

        self.stellarTab.setLayout(self.stellarTab.layout)

        # Add tabs to widget
        grid_layout.addWidget(self.tabs)


        #==========================================================================================
        # Creating the ISS Tab.
        # Experiment info, and crew information. added V0.85
        #==========================================================================================

        # Configuring the tab's layout
        self.issTab.layout =  QGridLayout()

        # Building the scrollbars
        scrollBuilder(self.issTab.layout, 0, 0)

        """
            Creating the ISS livestream embed, which threw several errors, so I had Claude help me troubleshoot. 
            The main issue was that YouTube was blocking the stream from loading in the QWebEngineView, which was giving error 153. 
            To get around this, I had to set a desktop user-agent and allow local HTML to access remote URLs. 
            I also had to create a local server to serve the YouTube embed code with sandbox disabled, which finally allowed the stream to load properly.
        
            I'm not 100% behind this clunky fix, but it is the only thing that got it to work after arguing with the bot for few hours.
        """
        # Enable plugins globally
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.PluginsEnabled, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True
        )

        # Allow local HTML to access remote URLs and set a desktop user-agent to avoid YouTube blocking (fix error 153)
        # TODO: find out iff all tese settings are necessary, or if some can be removed.
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.WebGLEnabled, True
        )
        
        QWebEngineProfile.defaultProfile().setHttpUserAgent(
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
         )

        # Load YouTube embed with sandbox disabled
        class YouTubeHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    html = b"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body { margin: 0; padding: 0; overflow: hidden; }
                            iframe { border: none; }
                        </style>
                    </head>
                    <body>
                        <iframe width="900" height="700" 
                            src="https://www.youtube.com/embed/FuuC4dpSQ1M?si=jTdxMlCOACYwXkhw&fs=1" 
                            frameborder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen" 
                            allowfullscreen>
                        </iframe>
                    </body>
                    </html>
                    """
                    self.wfile.write(html)

        # Start local server in background thread
        PORT = 8888
        handler = YouTubeHandler
        httpd = socketserver.TCPServer(("", PORT), handler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Replace your YouTube embed code with this:
        self.issView = QtWebEngineWidgets.QWebEngineView()
        self.issView.setUrl(QUrl(f"http://localhost:{PORT}/"))
        self.issView.setMinimumWidth(900)
        self.issView.setMaximumHeight(700)
        # Building the SpaceX Lens object
        frameBuilder(scroll.layout, 0, 1, 750, False)
        vert_Spacer(scroll.layout, 150, 50)
        frameLayout.addWidget(self.issView, 2, 0)




        # building the header frame
        windowMessage = "                           ISS Window                        "
        headerBuild(windowMessage, 0, 0, frameLayout, 50)

        frameBuilder(frameLayout, 2, 1, 450, True)              # Creating the inner frame
        self.frame.setLineWidth(5)

        headerMessage = "HDEV Camera"
        technicalDescrip = "\tActivated on April 30, 2014, the primary purpose of the High Definition Earth-Viewing System (HDEV) is to monitor the rate at which HD video image quality degrades when exposed to the harsh environment of space, mainly cosmic ray damage. Unfortunatly, the HDEV experiment reached End of Life in 2019, but rejoice space fans! Live views of our beautiful home can be enjoyed through another camera mounted elsewhere on the ISS.\n\tThis new camera presents a new view in which one may occasionally spot a solar panel.\n"
        blackHead = "Why is the window black?\n"
        descrip = "\tDon't fear! The ISS is currently passing over the night side of the Earth. The view usually brightens again a few minutes, and sometimes we're treated with a sunrise!"
        powerHead = "What is this screen?\n"
        screenDesc = "\tIf a screen that looks more like a PowerPoint slide is greeting you, don't fret! The system is only switching cameras or the feed has lost contact with home. The stream is still working, and the view will return."
        headerBuild(headerMessage, 0, 0, frameLayout, 100)


        welcomeFont.setBold(True)
        # Creating the label for the technical description of HDEV
        label_maker(technicalDescrip, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 1, 0 )


        hDivider  = QFrame()
        hDivider.setFrameShape(QFrame.HLine)
        hDivider.setLineWidth(3)
        frameLayout.addWidget(hDivider, 2, 0)

        # Creating the label with the black header
        label_maker(blackHead, QtCore.Qt.AlignCenter, welcomeFont, 450, frameLayout, 3, 0)


        # Creating the black screen explanation label
        label_maker(descrip, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 4, 0)


        hDivider  = QFrame()
        hDivider.setFrameShape(QFrame.HLine)
        hDivider.setLineWidth(3)
        frameLayout.addWidget(hDivider, 5, 0)

        # Creating the label with the power point head
        label_maker(powerHead, QtCore.Qt.AlignCenter, welcomeFont, 450, frameLayout, 6, 0)


        # Creating the black screen explanation label

        label_maker(screenDesc, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 7, 0)
        #horizSpacer = QSpacerItem(20, 20, QSizePolicy.Maximum, QSizePolicy.Expanding)
        #frameLayout.addItem(horizSpacer, 3, 2)


        """
            Creating the ISS tracker section
        """
        frameBuilder(scroll.layout, 1, 1, 750, False)

        verticalSpacer = QSpacerItem(125, 125, QSizePolicy.Maximum, QSizePolicy.Expanding)
        frameLayout.addItem(verticalSpacer, 0, 0)
        frameLayout.addItem(verticalSpacer, 0, 2)

        # Adding an ISS Tracker as a Web object.
        mapUrl = "https://isstracker.spaceflight.esa.int/"
        trackerHTML = "<body padding='0px' style='background-color: #778899; max-height: 350; max-width: 625;'> <iframe width='100%' height='100%' allowtransparency='true' style='background: Darkslategray; position: fixed; top:0; left:0; bottom:0; right:0;' src='{}' frameborder='0' scrolling='no' allowfullscreen></iframe>".format(mapUrl)
        web_wrapper(trackerHTML, 100, frameLayout, 0, 1, True)
        self.webView.setMaximumWidth(630)
        self.webView.setMaximumHeight(350)


        # Building the "Fun facts" section
        frameBuilder(frameLayout, 0, 4, 450, True)
        self.frame.setLineWidth(5)

        # The strings for the facts labels.
        speed = "The International Space Station orbits the Earth every 90 minutes, travelling at 5 miles per second."
        orbit = "The station orbits our planet 16 times a day."
        altitude = "The ISS resides about 250 miles from Earth. On average, it takes about six hours to reach the station from Earth."
        headerStr = "ISS Fun Facts"

        #Building and placing the labels.
        headerBuild(headerStr, 0, 0, frameLayout, 100)
        label_maker(speed, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 1, 0)
        # Throwing in a divider
        hDivider  = QFrame()
        hDivider.setFrameShape(QFrame.HLine)
        hDivider.setLineWidth(3)
        frameLayout.addWidget(hDivider, 5, 0)

        frameLayout.addWidget(hDivider, 2, 0)
        label_maker(orbit, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 3, 0)
        # Throwing in a divider
        hDivider  = QFrame()
        hDivider.setFrameShape(QFrame.HLine)
        hDivider.setLineWidth(3)
        frameLayout.addWidget(hDivider, 5, 0)

        frameLayout.addWidget(hDivider, 4, 0)
        label_maker(altitude, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 5, 0)


        # Keep at bottom of tab section. needed for the tab to showup.
        self.issTab.setLayout(self.issTab.layout)



        #=======================================================================
        # Creating the menu bar and its entries.
        #=======================================================================

        #class MenuBar():

            #def __init__(self):

        iconList = [os.path.join(baseDir, "Images/Icons/exit.png"), os.path.join(baseDir, "Images/Icons/about.png"), os.path.join(baseDir, "Images/Icons/information.png"), os.path.join(baseDir, "Images/Icons/refresh.png"), os.path.join(baseDir, "Images/Icons/update.png")]


        # The menu item builder
        # takes an image from iconLst as image
        # toggles icons off with iconToggle
        # takes the tool tip as statusTip
        # gets the item's name as menuName
        # method is the function to be run when clicked
        def buildMenuItemAction(image, iconToggle, statusTip, menuName, method):

            if iconToggle is True:
                item = QAction(QIcon(image), menuName, self)
                item.setStatusTip(statusTip)
                item.triggered.connect(method)
                return item
            else:
                item = QAction(menuName, self)
                item.setStatusTip(statusTip)
                item.triggered.connect(method)
                return item


        toggler = True
        exitAct = buildMenuItemAction(iconList[0], toggler, "Exit Application", "&Exit", qApp.quit)                               # Exit option
        aboutAct = buildMenuItemAction(iconList[1], toggler, "Build Information", "&About", clickMethod)                          # About Option
        sourceAct = buildMenuItemAction(iconList[2], toggler, "List of Sources Used By AstroNinja", "&Sources", sourceMethod)     # Sources option
        refreshAct = buildMenuItemAction(iconList[3], toggler, "Refreshes The Window", "&Reload", restart_program)                # Refresh option
        toggler = False                                                                                                           # The rest of the options have no icons
        marineAct = buildMenuItemAction(iconList[0], toggler, "A More Subtle Theme", "&Marine", Marine)                           # Default Theme
        spacexAct = buildMenuItemAction(iconList[0], toggler, "A Theme based On SpaceX and The Default Theme", "&SpaceX", Spacex) # SpaceX Theme
        brocoAct = buildMenuItemAction(iconList[0], toggler, "A Vaporwave Theme For Dark Mode", "&Broco", broco)                  # Broco Theme

        # Adding a menubar.
        menubar = self.menuBar()


        if themeSelected == 'marine':
            astroThemesV85.defaultMenu(menubar)    # TESTING the function for the default menubar theme
        if themeSelected == 'spaceX':
            astroThemesV85.spacexMenu(menubar)
        if themeSelected == 'broco':
            astroThemesV85.brocoMenu(menubar)
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(refreshAct)
        fileMenu.addAction(sourceAct)
        fileMenu.addAction(aboutAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        # Adding a Settings menu to the menu bar.
        settingsMenu = menubar.addMenu('&Settings')
        themeMenu = settingsMenu.addMenu('&Themes')
        themeMenu.addAction(marineAct)
        themeMenu.addAction(spacexAct)
        themeMenu.addAction(brocoAct)

        self.statusBar()
        self.showMaximized()
        #self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Prefetch news and hubble data after QApplication exists so QThread can initialize safely.
    try:
        xNews.phoneHome()
    except Exception as e:
        print('xNews.phoneHome() failed:', e)
    try:
        xNews.hubbleViewz()
    except Exception as e:
        print('xNews.hubbleViewz() failed:', e)

    ex = App()
    #self.show()
    sys.exit(app.exec_())
