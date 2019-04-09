import urllib.request
import json
import urllib.parse
from http import HTTPStatus
def printResults(data):
    # Use the json module to load the string data into a dictionary
    theJSON = json.loads(data)
    # now we can access the contents of the JSON like any other Python object
    print (data)

def par(eventLog):


 def main():
    # define a variable to hold the source URL
    urlData = "https://calendar.oswego.edu/api/2/events?days=90&pp=100"

    # Open the URL and read the data
    webUrl = urllib.request.urlopen(urlData)
    print ("result code: " + str(webUrl.getcode()))
    if (webUrl.getcode() == HTTPStatus.OK):
        data = webUrl.read()
        # print out our customized results
        printResults(data)
    else:
        print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))

 if __name__ == "__main__":
    main()
