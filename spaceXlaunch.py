"""
   * A practice script for scraping data from article pages using scrapy instead
   * of bs4
"""

"""
   * Written By : Tom Mullins
   * Created:  07/24/20
   * Modified: 05/22/21
"""

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
        link.append(spacexDict['link'])
        missionTitle.append(spacexDict['mission'])

    # Catching if there is no launch video available.
    if len(link) == 0:
        onlyLink = ""

    else:
        # Getting the first link and mission title in the schedule.
        onlyLink = link[0]
        onlyTitle = missionTitle[0]


    return
