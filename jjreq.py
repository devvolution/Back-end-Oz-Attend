import urllib.request
import json
#!usr/bin/python
import MySQLdb
class Event:
	#title = t
	#event_instance->start= fD
	#event_instance->end = lD
	#location_name = loc
	#room_number = rN
	#private = p
	#description_text = d
	#event_types = eTy
	#event_topics =  eTo
	#event_target_audience = eTa
	
	def __init__(self, t, d, loc, fD, lD, rN, p, eTy, eTo, eTa, idt):
		self.__t = t
		self.__fD = fD
		self.__lD = lD
		self.__loc = loc
		self.__rN = rN
		self.__p = p
		self.__d = d
		self.__eTy = eTy
		self.__eTo =  eTo
		self.__eTa = eTa
		self.__pin = self.__configurePin(idt)
		self.__attendance = []

	def __configurePin(self, iden):
		alpha = iden ^ 4716857
		beta = iden ^ 1938427
		
		
		iden = int((alpha * beta) / 641)
		while iden < 60466177:
			iden = iden * 13
		
		r = []
		while iden > 36:
			r.append(int(iden % 36))
			iden = (iden - iden % 36) / 36
		r.append(int(iden % 36))
		
		for t in range(0,len(r)):
			if r[t] < 26:
				r[t] = chr(r[t] + 65)
			else:
				r[t] = chr(r[t] + 22)
		
		v = ''.join(r)
		#print (v)
		return v

	def getTitle(self):
		#print (self.__t)
		return self.__t

	def getDescription(self):
		#print (self.__d)
		return self.__d

	def getStartTime(self):
		#print (self.__fD)
		return self.__fD

	def getEndTime(self):
		#print (self.__lD)
		return self.__lD

	def getLocation(self):
		#print (self.__loc)
		return self.__loc

	def getRoomNumber(self):
		#print (self.__rN)
		return self.__rN

	def getPrivate(self):
		print (self.__p)
		return self.__p

	def getTypes(self):
		#print (self.__eTy)
		return self.__eTy

	def getTopics(self):
		#print (self.__eTo)
		return self.__eTo

	def getTargets(self):
		#print (self.__eTa)
		return self.__eTa

	#Needs to ask for credentials
	def sendPin(self):
		#print (self.__pin)
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

class Participant:
	
	def __init__(self, fN, lN, SID, E, M, Y, DB, G):
		self.__first = fN
		self.__last = lN
		self.__ID = SID
		self.__email = E
		self.__username = E.split('@')[0]
		self.__major = M
		self.__year = Y
		self.__DoB = DB
		self.__gender = G

	def getName(self):
		print (self.__first + " " + self.__last)
		return self.__first + " " + self.__last

	def getFirst(self):
		print (self.__first)
		return self.__first

	def getLast(self):
		print (self.__last)
		return self.__last

	def getID(self):
		print (self.__ID)
		return self.__ID

	def getEmail(self):
		print (self.__email)
		return self.__email

	def getUser(self):
		print (self.__username)
		return self.__username

	def getMajor(self):
		print (self.__major)
		return self.__major

	def getYear(self):
		print (self.__year)
		return self.__year

	def getDoB(self):
		print (self.__DoB)
		return self.__DoB

	def getGender(self):
		print (self.__gender)
		return self.__gender

	def joinEvent(self):
		if eventList[0].confirmAttendance("I1U9GXB", self):
			print('You have joined the following event:\n' + eventList[0].getTitle())
		else:
			print('You have failed to join event.')

def main():
	# define a variable to hgfdfgold the source URL
	# In this case we'llfdghgf use the free data feed from the USGS
	# This feed lists all earthquakes fdgfhdfor the last day larger than Mag 2.5
	urlData = "https://calendar.oswego.edu/api/2/events?days=10&pp=15"

	# Open the URL and read the data
	webUrl = urllib.request.urlopen(urlData)
	#print ("result code: " + str(webUrl.getcode()))
	if (webUrl.getcode() == 200):
		data = webUrl.read()
		# print out our customized results
		jsonstr = str(data).replace("\\\\","\\")
		encoding = webUrl.info().get_content_charset('utf-8')
		ghj = json.loads(data.decode(encoding))

		global eventList
		eventList = []
		for i in ghj['events']:
			typeList = []
			topicList = []
			targetList = []

			for j in i['event']['filters']['event_types']:
				#print(j['name'])
				typeList.append(j['name'])
			try:
				for j in i['event']['filters']['event_topic']:
					#print(j['name'])
					topicList.append(j['name'])
			except:
				#print("the error is: ")
				topicList.append("None")
			for j in i['event']['filters']['event_target_audience']:
				#print(j['name'])
				targetList.append(j['name'])

			eventList.append(Event(i['event']['title'], i['event']['description_text'], i['event']['location_name'], i['event']['event_instances'][0]['event_instance']['start'], i['event']['event_instances'][0]['event_instance']['end'], i['event']['room_number'], i['event']['private'], typeList, topicList, targetList, i['event']['id']))

##		listTester = 5
##		eventList[listTester].getTitle()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getDescription()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getStartTime()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getEndTime()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getLocation()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getRoomNumber()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getPrivate()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getTypes()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getTopics()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].getTargets()
##		print("----------------------------------------------------------------------------")
##		eventList[listTester].sendPin()
##		print("----------------------------------------------------------------------------")
		
		pp = []
	else:
		print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))

	db = MySQLdb.connect("pi.cs.oswego.edu","nmolina","csc380","attendance")
	cursor = db.cursor()
	sql = "SELECT * FROM Account"
	
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		#print (results)
		
		for row in results:
			student = row[0]
			fname = row[1]
			lname = row[2]
			email = row[4]
			year = row[5]
			major = row[6]
			birth = row[7]
			gender = row[8]
			
			print ("id = " + str(student))
			print ("fname = " + fname)
			print ("lname = " + lname)
			print ("email = " + email)
			print ("year = " + year)
			print ("major = " + major)
			print ("birthday = " + birth)
			print ("gender = " + gender)
			pp.append(Participant(fname, lname, student, email, major, year, birth, gender))
	
	except:
		print("Error: unable to fetch data")
	
	db.close()
	
	pp[0].getName()

if __name__ == "__main__":
	main()
