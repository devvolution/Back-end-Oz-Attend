import urllib.request
import json


# Event class incomplete
class Event:
    # title = t
    # event_instance->start= fD
    # event_instance->end = lD
    # location_name = loc
    # room_number = rN
    # private = p
    # description_text = d
    # event_types = eTy
    # event_topics =  eTo
    # event_target_audience = eTa

    def __init__(self, t, d, loc, fD, lD, rN, p, eTy, eTo, eTa, idt):
        self.__t = t
        self.__fD = fD
        self.__lD = lD
        self.__loc = loc
        self.__rN = rN
        self.__p = p
        self.__d = d
        self.__eTy = eTy
        self.__eTo = eTo
        self.__eTa = eTa
        self.__pin = self.__configurePin(idt)

    def __configurePin(self, iden):
        alpha = iden ^ 4716857
        beta = iden ^ 1938427

        while iden < 1000000000:
            iden = iden * 13

        iden = int((alpha * beta) / 641)
        r = []
        while iden > 36:
            r.append(int(iden % 36))
            iden = (iden - iden % 36) / 36
        r.append(int(iden % 36))

        for t in range(0, len(r)):
            if r[t] < 26:
                r[t] = chr(r[t] + 65)
            else:
                r[t] = chr(r[t] + 22)

        v = ''.join(r)
        print (v)
        return v

    def getTitle(self):
        print (self.__t)
        return self.__t

    def getDescription(self):
        print (self.__d)
        return self.__d

    def getStartTime(self):
        print (self.__fD)
        return self.__fD

    def getEndTime(self):
        print (self.__lD)
        return self.__lD

    def getLocation(self):
        print (self.__loc)
        return self.__loc

    def getRoomNumber(self):
        print (self.__rN)
        return self.__rN

    def getPrivate(self):
        print (self.__p)
        return self.__p

    def getTypes(self):
        print (self.__eTy)
        return self.__eTy

    def getTopics(self):
        print (self.__eTo)
        return self.__eTo

    def getTargets(self):
        print (self.__eTa)
        return self.__eTa

    # Needs to ask for credentials
    def sendPin(self):
        print (self.__pin)
        return self.__pin


def main():
    # define a variable to hgfdfgold the source URL
    # In this case we'llfdghgf use the free data feed from the USGS
    # This feed lists all earthquakes fdgfhdfor the last day larger than Mag 2.5
    urlData = "https://calendar.oswego.edu/api/2/events?days=10&pp=50"

    # Open the URL and read the data
    webUrl = urllib.request.urlopen(urlData)
    print ("result code: " + str(webUrl.getcode()))
    if (webUrl.getcode() == 200):
        data = webUrl.read()
        # print out our customized results
        jsonstr = str(data).replace("\\\\", "\\")
        size = jsonstr.rfind("\"size\"")
        encoding = webUrl.info().get_content_charset('utf-8')
        ghj = json.loads(data.decode(encoding))
        # print (ghj['events'][0]['event']['title'])
        # print (ghj['events'][1]['event']['title'])
        print ("size:\t{}\n".format(ghj['page']['size']))

        eventList = []
        for i in ghj['events']:
            typeList = []
            topicList = []
            targetList = []

            for j in i['event']['filters']['event_types']:
                # print(j['name'])
                typeList.append(j['name'])
            try:
                for j in i['event']['filters']['event_topic']:
                    # print(j['name'])
                    topicList.append(j['name'])
            except:
                # print("the error is: ")
                topicList.append("None")
            for j in i['event']['filters']['event_target_audience']:
                # print(j['name'])
                targetList.append(j['name'])

            eventList.append(Event(i['event']['title'], i['event']['description_text'], i['event']['location_name'],
                                   i['event']['event_instances'][0]['event_instance']['start'],
                                   i['event']['event_instances'][0]['event_instance']['end'], i['event']['room_number'],
                                   i['event']['private'], typeList, topicList, targetList, i['event']['id']))

        listTester = 1
        eventList[listTester].getTitle()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getDescription()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getStartTime()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getEndTime()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getLocation()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getRoomNumber()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getPrivate()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getTypes()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getTopics()
        print("----------------------------------------------------------------------------")
        eventList[listTester].getTargets()
        print("----------------------------------------------------------------------------")
        eventList[listTester].sendPin()
        print("----------------------------------------------------------------------------")

    # eventList = jsonstr.split('},{\"event\":')
    # for i in range(len(eventList)):
    # print (eventList[i])
    # print ("\n\n")

    else:
        print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))


if __name__ == "__main__":
    main()
