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
        self.__attendance = []

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
        print(v)
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
        print(self.__pin)
        return self.__pin

        #Needs to ask for credentials
    def sendAttendance(self):
        #print (self.__attendance)
        return self.__attendance

        # add location verirification likely via IP
    def confirmAttendance(self, psuedo, potential):
        test = self.__pin == psuedo
        #print(test)
        if test:
            self.__attendance.append(potential)
        return test

# the participant class used to generate participant objects
class Participant:

    def __init__(self, userId, id, fn, ln, userName, major, email, yr, dob, gen):
        self.__userId = userId
        self.__id = id
        self.__fn = fn
        self.__ln = ln
        self.__userName = userName
        self.__major = major
        self.__email = email
        self.__yr = yr
        self.__dob = dob
        self.__gen = gen

    #def getEvent(self):
     #   print(event)
      #  return event

    def getUserId(self):
        return (self.__userId)

    def getID(self):
        #print(self.__id)
        return self.__id

    def setID(self, ident):
        self.__id = ident

    def getFirstName(self):
        #print(self.__fn)
        return self.__fn

    def setFirstName(self, firstN):
        self.__fn = firstN

    def getLastName(self):
        #print(self.__ln)
        return self.__ln

    def setLastName(self, lastN):
        self.__ln = lastN

    def getUserName(self):
        #print(self.__userName)
        return self.__userName

    def setUserName(self, use):
        self.__userName = use

    def getMajor(self):
        #print(self.__major)
        return self.__major

    def setMajor(self, maj):
        self.__major = maj


    def getEmail(self):
        #print(self.__email)
        return self.__email

    def setEmail(self, mail):
        self.__email = mail

    def getYear(self):
        #print(self.__yr)
        return self.__yr

    def setYear(self, year):
        self.__yr = year

    def getDoB(self):
        #print(self.__dob)
        return self.__dob

    def setDoB(self, birth):
        self.__dob = birth

    def getGender(self):
        #print(self.__gen)
        return self.__gen

    def setGender(self, onlyTwo):
        self.__gen = onlyTwo

    def joinEvent(self):
        if eventList[0].confirmAttendance("I1U9GXB", self):
            print('You have joined the following event:\n' + eventList[0].getTitle())
        else:
            print('You have failed to join event.')


class Organizer:
    def __init__(self):
        self


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


        global eventList
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
        connection = mysql.connector.connect(host='pi.cs.oswego.edu',
                                             database='attendance',
                                             user='nmolina',
                                             password='csc380')
        sql_select_Query = "select * from Account"
        cursor = connection.cursor()

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        participants = []
        print("things in the DB - ", cursor.rowcount)
        i = list
        for row in records:
            userId = row[0]

            iden = row[1]

            firstName = row[2]

            lastName = row[3]

            userName = row[4]

            year = row[5]

            major = row[6]

            email = row[7]

            dob = row[8]

            thing = row[9]


            participants.append(Participant(userId, iden, firstName, lastName, userName, email, year, major, dob, thing))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("connected to database", db_Info)

            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("you're connected to -", record)
    except Error as e:
            print("Error while connecting to MySQL", e)
    finally:
         if(connection.is_connected()):
                cursor.close()
                connection.close()
                print("database closed")
    try:
        for i in range(0, s):
            print("-------------------------------------")
            print("user ID: " + str(participants[i].getUserId()))
            print("ID: " + str(participants[i].getID()))
            print("First Name: " + participants[i].getFirstName())
            print("Last Name: " + participants[i].getLastName())
            print("User Name: " + participants[i].getUserName())
            print("Year: " + participants[i].getYear())
            print("Major: " + participants[i].getMajor())
            print("Email: " + participants[i].getEmail())
            print("Date of Birth:" + participants[i].getDoB())
            print("Sex: " + participants[i].getGender())
            participants[0].joinEvent()
    except IndexError as e:
        print("end of participant list")
        print("---------------------------------------\n")
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
