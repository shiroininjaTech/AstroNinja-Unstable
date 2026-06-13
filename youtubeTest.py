"""
   * A test script for scraping the url for the newest video from a youtube
   * video.
"""

"""
   * Written By : Tom Mullins
   * Created:  04/05/18
   * Modified: 06/30/20
"""

import re
import requests, bs4


# a simple function to get the url of the newest spaceX video

def testFlight():
    # Getting the website and making sure we've made contact :P

    links = []

    # If connection to YouTube fails, keep trying.
    while len(links) == 0:
        spacexChannel = requests.get('https://www.youtube.com/c/SpaceX/videos?view=0&sort=dd&flow=grid')
        spacexChannel.raise_for_status()

        # Now that we have the website loaded, let's parse it with Beautiful Soup (why not Ugly soup??)
        xSoup = bs4.BeautifulSoup(spacexChannel.text, "lxml")
        print(xSoup)

        # Getting the Date and Mission name
        findVids = xSoup.find_all("div", class_ = "style-scope ytd-grid-video-renderer")
        global fullURL, newestName
        print(findVids)
        names = []
        for x in findVids:
            links.append(x.get("href"))
            #print(links)
            names.append(x.get("title"))
            #print(names)
    youtubeURL = 'https://www.youtube.com/embed'
    newestLink = links[0]
    newestLink2 = newestLink[9:]
    newestName = names[0]
    fullURL = youtubeURL + newestLink2
    #print(fullURL)
    #print(newestName)
    return



#testFlight()
