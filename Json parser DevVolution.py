import urllib.request
import json
import urllib.parse
from http import HTTPStatus
import itertools
import base64


# def eventInfo(source)
# Event class incomplete
class Event:
    # id = id
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

    def __init__(self, iD, t, d, loc, fD, lD, rN, p, eTy, eTo, eTa, idt):
        self.__iD = iD
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

    def getId(self):
        print(self.__iD)
        return self.__iD

    def getTitle(self):
        print(self.__t)
        return self.__t

    def getDescription(self):
        print(self.__d)
        return self.__d

    def getStartTime(self):
        print(self.__fD)
        return self.__fD

    def getEndTime(self):
        print(self.__lD)
        return self.__lD

    def getLocation(self):
        print(self.__loc)
        return self.__loc

    def getRoomNumber(self):
        print(self.__rN)
        return self.__rN

    def getPrivate(self):
        print(self.__p)
        return self.__p

    def getTypes(self):
        print(self.__eTy)
        return self.__eTy

    def getTopics(self):
        print(self.__eTo)
        return self.__eTo

    def getTargets(self):
        print(self.__eTa)
        return self.__eTa

    # Needs to ask for credentials
    def sendPin(self):
        print (self.__pin)
        return self.__pin


class Participant:

    def __init__(self, event, info):
        self.__event = event
        self.__info = info



    def viewEvent(self):
        print(self.e.getId())
        print(self.e.getTitle())
        print(self.e.getDescription())
        print(self.e.getStartTime())
        print(self.e.getEndTime())
        print(self.e.getLocation())
        print(self.e.getRoomNumber())
        print(self.e.getPrivate())
        print(self.e.getTypes())
        print(self.e.getTopics())
        print()
        return self.e.getId(), self.e.getTitle(), self.e.getDescription(), self.e.getStartTime(), self.e.getEndTime(), \
               self.e.getLocation(), self.e.getRoomNumber(), self.e.getPrivate(), self.e.getTypes(), self.e.getTopics(), \
               self.e.getTargets()


def main():
    # define a variable to hgfdfgold the source URL
    urlData = "https://calendar.oswego.edu/api/2/events?pp=25"

    # Open the URL and read the data
    webUrl = urllib.request.urlopen(urlData)
    print("result code: " + str(webUrl.getcode()))
    if (webUrl.getcode() == HTTPStatus.OK):
        data = webUrl.read()
        # print out our customized results
        jsonstr = str(data).replace("\\\\", "\\")
        size = jsonstr.rfind("\"size\"")
        encoding = webUrl.info().get_content_charset('utf-8')
        atributes = json.loads(data.decode(encoding))
        # print (ghj['events'][0]['event']['title'])
        # print (ghj['events'][1]['event']['title'])
        print("size:\t{}\n".format(atributes['page']['size']))

        # def xor_crypt_string(data, key='awesomepassword', encode=False, decode=False):
        #   from itertools import izip, cycle
        #  import base64
        #   if decode:
        #      data = base64.decodestring(data)
        #  xored = eventList.getId().join(chr(ord(x) ^ ord(y)) for (x, y) in izip(data, cycle(key)))
        #  if encode:
        #      return base64.encodestring(xored).strip()
        # return xored

        eventList = []
        for i in atributes['events']:
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

            eventList.append(Event(i['event']['id'], i['event']['title'], i['event']['description_text'],
                                   i['event']['location_name'],
                                   i['event']['event_instances'][0]['event_instance']['start'],
                                   i['event']['event_instances'][0]['event_instance']['end'], i['event']['room_number'],
                                   i['event']['private'], typeList, topicList, targetList, i['event']['id']))
        s = eventList.__sizeof__()
    try:
        # listTester = i
        for i in range(0, s):
            print("----------------------------------------------------------------------------")
            eventList[i].viewEvent()
			# eventList[i].getId()
			# eventList[i].getTitle()
			# eventList[i].getDescription()
			# eventList[i].getStartTime()
			# eventList[i].getEndTime()
			# eventList[i].getLocation()
			# eventList[i].getRoomNumber()
			# eventList[i].getPrivate()
			# eventList[i].getTypes()
			# eventList[i].getTopics()
			# eventList[i].getTargets()

            print("----------------------------------------------------------------------------\n")
    except IndexError as error:
        print("end of the list")
    # eventList = jsonstr.split('},{\"event\":')
    # for i in range(len(eventList)):
    # print (eventList[i])
    # print ("\n\n")

    else:
        print("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))


if __name__ == "__main__":
    main()

# def main():
# define a variable to hold the source URL
#	urlData = "https://calendar.oswego.edu/api/2/events?pp=100"

# Open the URL and read the data
#	webUrl = urllib.request.urlopen(urlData)
#	print ("result code: " + str(webUrl.getcode()))
# checks the connection to web
#	if (webUrl.getcode() == HTTPStatus.OK):
# data is the object holding the read json file
#		data = webUrl.read()
# print out our customized results
# jsonstr fixes discrepancies in the json string
#		jsonstr = str(data).replace("\\\\","\\")
# size = jsonstr.rfind("\"size\"")
#		encoding = webUrl.info().get_content_charset('utf-8')
# atributes is the obj that holds the json file which was read
#		atributes = json.loads(data.decode(encoding))
# this loop pulls out the needed attributes
#		k=0
#		for i in atributes['events']:
#			print(i['event']['title'])
#			print(i['event']['last_date'])
#			print(i['event']['first_date'])
#			print(i['event']['room_number'])
#			print(i['event']['location_name'])
#			print("privacy status:")
#			print(i['event']['private'])
#			print("event description:")
#			print(i['event']['event_instances'][0]['event_instance']['start'])
#			print(i['event']['description_text'])


# this loop is supposed to get the type of event
#			try:
#				for j in atributes['events'][k]['event']['filters']['event_types']:
#					print(j['name'])
#			except Exception as e:
#				print("the error is: "+ str(e))
#			print("----------\n")
#			k = k+1

# eventList = jsonstr.split('},{\"event\":')
# for i in range(len(eventList)):
# print (eventList[i])
# print ("\n\n")

#	else:
#		print("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))


# if __name__ == "__main__":
#	main()
