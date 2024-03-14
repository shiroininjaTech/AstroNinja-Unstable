"""
   * A practice script for scraping data from article pages using scrapy instead
   * of bs4
"""

"""
   * Written By : Tom Mullins
   * Created:  07/24/20
   * Modified: 10/17/23
"""

from youtubesearchpython import VideosSearch

global spacexDump
spacexDump = []



# pipeline to fill the items list
class MoreCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        spacexDump.append(item)


def liftOff():
    # lists to be filled with items from spacexDump
    global onlyLink, onlyTitle
    link = []
    missionTitle = []

    for i in spacexDump:
        spacexDict = dict(i)
        link.append(spacexDict['youtubeUrl'])
        missionTitle.append(spacexDict['mission'])

    # Catching if there is no launch video available.
    if len(link) == 0:
        onlyLink = ""

    else:

        
        # Getting the first link and mission title in the schedule.
        onlyLink = link[0]
        onlyTitle = missionTitle[0]


    # getting the launch url using a youtube searching library, and then parsing the results to the first video result's link.
    
    launchSearch = VideosSearch(missionTitle[0], limit = 1)

    if len(launchSearch.result()['result']) == 0 :
        return     
    
    else:

        resultDict = launchSearch.result()['result'][0]  # Getting the first dictionary from the main dictionary.
        print(resultDict)
        result2  = (resultDict['link']).replace("watch?v=", 'embed/')+ '?si=XPF4U5XII6S2xNTz' # Turning the video link into an embed link.

        onlyLink = result2



        return

