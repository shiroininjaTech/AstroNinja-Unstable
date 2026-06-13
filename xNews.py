"""
   * A Module for AstroNinja that pulls news articles from multiple sources
   * and wraps them in a global list for iterating over and passing over to the
   * front end for displaying to the user via the SpaceX news tab.
"""

"""
   * Written By : Tom Mullins
   * Created:  04/30/18
   * Modified: 06/12/26
"""

import re
import requests, bs4
import threading
from queue import Queue
from multiprocessing import Process

# A funtion that gets articles from SpaceX's website
def phoneHome():

    # A function that gets the links to the articles and splices it together so
    # BeautifulSoup can use it to scrape the article's text.
    def articleLinks():
        # Getting the website and making sure we've made contact :P
        spacexSite = requests.get('http://www.spacex.com/news')
        spacexSite.raise_for_status()
        xSoup = bs4.BeautifulSoup(spacexSite.text, "lxml")

        findURL = xSoup.find_all("div", class_= "readmore")
        links = []
        for x in findURL:
            links.append(x.find('a'))
        linkHref =[]
        for x in links:
            linkHref.append(x.get('href'))

        spaceXURL = 'http://www.spacex.com'
        global fullAddresses
        fullAddresses = []
        for x in linkHref:
            fullAddresses.append(spaceXURL + x)
        #print(fullAddresses)   # TESTING
        return

    # some variables needed for articleSpyder to iterate over the article links
    # provided by articleLinks() and populate lists with the article bodiesself.
    global xCounter
    xCounter = 0
    global titleList, bodyList, imageList
    titleList = []
    bodyList = []
    imageList = []



    # The function to get the text of the article located at URLs provided by phoneHome
    # Gets xCounter as an arguement.
    def articleSpyder(x):

        articleSite = requests.get(fullAddresses[x])
        articleSite.raise_for_status()
        articleSoup = bs4.BeautifulSoup(articleSite.text, "lxml")

        # Getting the Article's title
        articleTitle = articleSoup.find_all("h1", class_="title")
        titleStr = articleTitle[0].getText()

        # Getting the article bodies
        articleBody = articleSoup.find_all("div", class_="group-right")
        fixEDT = []

        articleParagraph = [i.getText() for i in articleBody]       # Getting rid of tags in items
        stripParagraph = [str(i) for i in articleParagraph]         # Turning items into mutable strings
        for i in stripParagraph:
            if 'EDT' in i:
                fixEDT.append(i.replace('. EDT', ' EDT'))           # Fixing formatting so there's
            elif 'PDT' in i:                                        # no uneeded newlines
                fixEDT.append(i.replace('. PDT', ' PDT'))
        #finalEDT = [i.replace('T, ', 'T, \n') for i in fixEDT]      # Adding newlines after the time
        tabVar = "\t"
        finalPara = []
        for i in fixEDT:
            finalPara.append(re.sub('You can.*', '', i))

        for i in finalPara:
            bodyList.append(tabVar + i)             # removing link information

        titleList.append(titleStr)
        global xCounter
        xCounter += 1     # Increment counter by 1 to move to the next URL
        return


    # A function to get lists of article links from spacenews.com
    # Takes either missions or news as arguements
    commercial = 'https://spacenews.com/section/commercial-archive/'
    news = 'https://spacenews.com/section/launch-archive/'
    civil = 'https://spacenews.com/section/civil1/'
    global hyperSpace
    hyperSpace = []
    global missionList, newsList, civilList
    commercialList = []
    newsList = []
    civilList = []

    def marsHeadlines(link, urlList):

        newspaper = requests.get(link)
        newspaper.raise_for_status()
        martianSoup = bs4.BeautifulSoup(newspaper.text, "lxml")
        headlines = martianSoup.find_all("h2", class_="entry-title")

        links = []
        for x in headlines:
            links.append(x.find('a'))
        print(links)
        spaceHref = []
        for x in links:
            spaceHref.append(x.get('href'))

        # the final list, that gets passed to intestellarNews
        #global urlList
        for x in spaceHref:
            urlList.append(str(x))
        return

    global yCounter
    yCounter = 0
    global counter
    counter = 0



    #print(articleSoups)
    # A function to get article text from links provided by marsHeadlines()
    # gets yCounter as an arguement for iterating through the links
    def intestellar_News(x):


        articleHtml = articleSoups[x]
        #print(articleHtml)
        # Getting the article's title
        articleTitle = articleHtml.find_all("h1", class_="entry-title")
        titleStr = articleTitle[0].getText()

        # Getting the article body
        articleBody = articleHtml.find_all("p")
        articleText = []
        for x in articleBody:
            articleText.append(x.getText())
            articleFixed = []
        for x in articleText:
            articleFixed.append('\t' + str(x))


        # A simple function to merge together the paragraph items into a single
        # String
        def concatenate_list(list):
            result = ''
            for element in list:
                result += str(element)
                result += '\n\n'
            return result

        fullArticle = concatenate_list(articleFixed)
        # getting the image for the article
        articleImg = articleHtml.find_all("figure", class_="post-thumbnail")
        imgLink = []
        global yCounter
        for x in articleImg:
            imgLink.append(x.find('img'))          # narrowing down the html parsing
        if not imgLink or imgLink[0] is None:
            titleList.append(titleStr)                     # Appending to the global
            bodyList.append(fullArticle)                   # Lists to be displayed
            imageList.append('https://cdn-icons-png.flaticon.com/512/117/117992.png')
            #send_end.send(titleStr, fullArticle, imgLink2[0])
            # increment counter by 1
            yCounter += 1

            return
        else:

            imgLink2 = []
            for x in imgLink:
                imgLink2.append(x.get('src'))
                #print(imgLink2)                          # TESTING

            #fullArticle2 = fullArticle.replace('. ', '. \n')
            titleList.append(titleStr)                     # Appending to the global
            bodyList.append(fullArticle)                   # Lists to be displayed
            imageList.append(imgLink2[0])                  # in the GUI.
            #print(titleStr, fullArticle)
            #pipe_list.append(titleStr)
            #pipe_list.append(fullArticle)
            #pipe_list.append(imgLink2[0])
            # increment counter by 1
            yCounter += 1

            return


    marsHeadlines(news, newsList)             # Getting the urls needed to scrape the articles
    marsHeadlines(commercial, commercialList)
    marsHeadlines(civil, civilList)

    # To thoroughly mix the articles from the two categories, we need a function
    # to sort them. Added V.075
    switchVar = 0

    def sewing_Machine(counter):
        hyperSpace.append(newsList[counter])
        hyperSpace.append(civilList[counter])
        hyperSpace.append(commercialList[counter])


    # Running sewing_Machine() until the end of the Lists
    while switchVar < len(commercialList):
        sewing_Machine(switchVar)
        switchVar += 1

    # Removing duplicate URLs/Articles
    hyperSpace = list(dict.fromkeys(hyperSpace))
    global articleSoups
    articleSoups = []               # The list variable for getting the multithreaded html

    # The function that is to be run by each thread.
    def get_page_info(current_page):
        #print(current_page)
        article = requests.get(current_page)
        article.raise_for_status()
        global articleSoups
        articleSoups.append(bs4.BeautifulSoup(article.text, "lxml"))

    # The function that processes Items in the threaded queue
    def process_queue():
        while True:
            current_page = page_queue.get()
            get_page_info(current_page)
            page_queue.task_done()
            #page_queue.join()

    page_queue = Queue()
    # Creating the threads and setting them to run the function
    for i in range(6):
        t = threading.Thread(target=process_queue)
        t.daemon = True
        t.start()


    for current_page in hyperSpace:
        page_queue.put(current_page)

    page_queue.join()
    #===========================================================================
    # Using multiprocessing to speed up processing of the data pulled from the
    # 31 urls pulled by marsHeadlines()
    #===========================================================================


    # Process the fetched article HTML sequentially to avoid out-of-range indexing.
    for index in range(len(articleSoups)):
        intestellar_News(index)

    #while yCounter != 32:
        #intestellar_News(yCounter)



    #print(len(titleList))
    #print(len(bodyList))
    #print(len(imageList))


    return
"""
    * A function that scapes Images from the Hubble space telescope from spacetelescope.org
    * using a function that scrapes links from the site and passes it to another Function
    * that retreives the image and description.
"""

def hubbleViewz():

    # The first function that get's the urls that are needed to get the images
    global hubbleLinks
    hubbleLinks = []

    def hubbleUrl():

        hubbleSite = requests.get('https://www.spacetelescope.org/images/potw/')
        hubbleSite.raise_for_status()
        hubbleSoup = bs4.BeautifulSoup(hubbleSite.text, "lxml")
        findHubble = hubbleSoup.find_all("div", class_="col-md-3 col-sm-6 col-xs-12")

        links = []
        for x in findHubble:
            links.append(x.find('a'))

        hubbleHref = []

        for x in links:
            hubbleHref.append(x.get('href'))

        hubSite = 'https://www.spacetelescope.org'
        global hubbleLinks
        # combining the items in hubbleHref with hubSite to make the full URL
        for x in hubbleHref:
            hubbleLinks.append(hubSite + x)

        #print(hubbleLinks)
        return hubbleLinks

    # the global lists to be populated with the images abd their descriptions
    global fullImage, fullDescription
    fullImage = []
    fullDescription = []
    global hubbleCounter
    hubbleCounter = 0

    # The function that retrieves the images from links provided by hubbleUrl()
    # gets a counter as "a"
    def hubbleScraper(a):

        hubbleHtml = hubbleSoups[a]

        hubImage = hubbleHtml.find_all('img', class_='img-responsive')
        # Getting the link
        imgLink = []
        for x in hubImage:
            imgLink.append(x.get('src'))

        hubSite = 'https://cdn.spacetelescope.org'
        if imgLink:
            if not imgLink[0].startswith(('http://', 'https://')):
                imgLink[0] = hubSite + imgLink[0]
        else:
            imgLink.append('https://cdn-icons-png.flaticon.com/512/117/117992.png')

        fullImage.append(imgLink[0])
        #print(fullImage)
        # Getting the image description
        imageDescrip = hubbleHtml.find_all("p")
        #descriptP = []
        #for x in imageDescrip:
            #descriptP.append(x.get('p'))
        descripText = []
        for x in imageDescrip:
            descripText.append(x.getText())
        descriptFixed = []
        for x in descripText:
            descriptFixed.append('\t' + str(x))

        # A simple function to merge together the paragraph items into a single
        # String
        def concatenate_list(list):
            result = ''
            for element in list:
                result += str(element)
                result += '\n'
            return result

        fullDescriptionList = concatenate_list(descriptFixed)
        fullDescription.append(fullDescriptionList)

        global hubbleCounter
        hubbleCounter += 1
        return




    hubbleUrl()


    global hubbleSoups
    hubbleSoups = []
    def get_page_info(current_page):
        #print(current_page)
        article = requests.get(current_page)
        article.raise_for_status()
        global hubbleSoups
        hubbleSoups.append(bs4.BeautifulSoup(article.text, "lxml"))

    def process_queue():
        while True:
            current_page = page_queue.get()
            get_page_info(current_page)
            page_queue.task_done()

    page_queue = Queue()

    for i in range(2):
        t = threading.Thread(target=process_queue)
        t.daemon = True
        t.start()

        #start = time.time()

    for current_page in hubbleLinks:
        page_queue.put(current_page)

    page_queue.join()

    #===========================================================================
    # Process the fetched Hubble pages and extract image URLs.
    #===========================================================================

    for idx in range(len(hubbleSoups)):
        hubbleScraper(idx)

    #print(fullImage)
    #print(fullDescription)
#phoneHome()
#hubbleViewz()
