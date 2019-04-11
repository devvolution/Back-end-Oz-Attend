import urllib.request
import json
import urllib.parse
from http import HTTPStatus
import mysql.connector
from mysql.connector import Error


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

    def __init__(self, event, fn, ln, major, minor, email, yr, dob, gen):
        self.__event = event
        self.__fn = fn
        self.__ln = ln
        self.__major = major
        self.__minor = minor
        self.__email = email.split("@")[0]
        self.__yr = yr
        self.__dob = dob
        self.__gen = gen

    def getEvent(self):
        print(self.__event)
        return self.__event

    def getFirstName(self):
        print(self.__fn)
        return self.__fn

    def getLastName(self):
        print(self.__ln)
        return self.__ln

    def getMajor(self):
        print(self.__major)
        return self.__major

    def getEmail(self):
        print(self.__email)
        return self.__email

    def getYear(self):
        print(self.__yr)
        return self.__yr

    def getDoB(self):
        print(self.__dob)
        return self.__dob

    def getGender(self):
        print(self.__gen)
        return self.__gen

class Organizer:
    def __init__(self):
        self

try:
    connection = mysql.connector.connect(host='pi.cs.oswego.edu',
                                         database = 'attendance',
                                         user='nmolina',
                                         password='csc380')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("connected to database",db_Info)

        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("you're connected to -", record)
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("database closed")


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
            eventList[i].getId()
            eventList[i].getTitle()
            eventList[i].getDescription()
            eventList[i].getStartTime()
            eventList[i].getEndTime()
            eventList[i].getLocation()
            eventList[i].getRoomNumber()
            eventList[i].getPrivate()
            eventList[i].getTypes()
            eventList[i].getTopics()
            eventList[i].getTargets()

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

