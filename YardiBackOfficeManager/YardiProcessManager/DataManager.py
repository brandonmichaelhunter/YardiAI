#
# DataManager is a class that will provide clients with methods to connect to any data source.
#TODO:
# Add a timer to run every 3 seconds to call Firebase for new entries. Maybe use the stream object. See documentation
# Use the IsConnected method to determine if we're still connected to the internet.If we're not,then write the record key and image name to text file. Once we're back online, then process the data
# within the text file first and then process new items from Firebase.
# Add error handling

import urllib3
import socket
import pyrebase
from datetime import datetime
class DataManager(object):

    config = ""
    firebase = ""
    def __init__(self):
        self.config = {
          "apiKey": "AIzaSyDdd2opaT2VZUkSuhwWuM0Kcz6gRJUR_e0",
          "authDomain": "yardiai-4ca2b.firebaseapp.com",
          "databaseURL": "https://yardiai-4ca2b.firebaseio.com",
          "storageBucket": "yardiai-4ca2b.appspot.com",
          "serviceAccount": "C:\\Users\Brandon\Documents\GitHub\YardiAI\YardiAI\YardiBackOfficeManager\YardiProcessManager\Resources\YardiAI-303194ef51f7.json"
        }
        self.firebase = pyrebase.initialize_app(self.config)
        pass


    # Determines if we're connected to firebase.
    def IsConnected(self):
        # This method will see if we're connected online.
       try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("firebase.google.com", 80))
        return True
       except OSError:
        return False

    def GetRecentPosts(self):
        queue = {}
        db = self.firebase.database()
        # Retrieve records that has been processed yet
        recs = db.child("YardTasks").order_by_child("ImageProcessed").equal_to(0).get()
        #store results into local queue for processing.
        for item in recs.each():
            queue[item.key()] = item.val()["ImageName"]
        
        #return queue to caller
        return queue
    def GenerateDateTimeStamp(self):
        year    = datetime.today().year
        day     = 0
        month   = 0
        hour    = 0
        minute  = 0
        seconds = 0
        
        if(datetime.today().minute < 10):
            minute = '0%a' %(datetime.today().minute)
        else:
            minute = datetime.today().minute
        
        if(datetime.today().second < 10):
            seconds = '0%a' %(datetime.today().second)
        else:
            seconds = datetime.today().second
        
        if(datetime.today().hour < 10):
            hour = '0%a' %(datetime.today().hour)
        else:
            hour = datetime.today().hour
        
        if(datetime.today().month < 10):
            month = '0%a' %(datetime.today().month)
        else:
            month = datetime.today().month

        if(datetime.today().day < 10):
           day = '0%a' %(datetime.today().day)
        else:
            day = datetime.today().day

        #return  "%a-%a-%a %a:%a:%a" %(year,month,day,hour,minute,seconds)
        #my_datetime.strftime("%B %d, %Y")
        return datetime.isoformat(datetime.now())

    def ProccessQueueTask(self, RecordKey, ImageName):
        #store the primary key and image url into a local variable.
        recID = RecordKey
        imageName = ImageName

        #Download the image to a local folder
        storage = self.firebase.storage()
        storageQuery = "images/{}".format(imageName)
        storage.child(storageQuery).download(imageName)

        #Call Tensorflow to determine what is the image
        results = self.IdentifyImage()

        #Save the results back to record in the YardsTasks table.
        result  = self.PublishResults(recID,results)

    def PublishResults(self, RecordKey, AIResults):
        db = self.firebase.database()
        #d = d.getFullYear() + "-" + ('0' + (d.getMonth() + 1)).slice(-2) + "-" + ('0' + d.getDate()).slice(-2) + " " + ('0' + d.getHours()).slice(-2) + ":" + ('0' + d.getMinutes()).slice(-2) + ":" + ('0' + d.getSeconds()).slice(-2);
        # publish changes to YardTasks table.
        modifiedDate = self.GenerateDateTimeStamp()
        saveResults = db.child("YardTasks").child(RecordKey).update({"ImageProcessed":1, "ImageClassified":AIResults,"ModifiedDate":modifiedDate})
        # return results back to consumer.
        return saveResults

    def IdentifyImage(self):
        return "95% this is an image"
    def CallerGetRecentUnprocessTasks(self):
        #Need to add a timer that will call this every 3 seconds
        queueTasks = self.GetRecentPosts()
        for k,v in queueTasks.items():
            self.ProccessQueueTask(k,v)

        


