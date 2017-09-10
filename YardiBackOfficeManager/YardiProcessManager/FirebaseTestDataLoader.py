import os, shutil 
import time
from datetime import datetime
import pyrebase
import glob
import DataManager
import geocoder
class FirebaseTestDataLoader(object):
       config = ""
       firebase = ""
       testUserID = "07b5W12BUWYmJ23ZDiT0z9VH1cG3"
       def __init__(self):
          self.config = {
          "apiKey": "AIzaSyDdd2opaT2VZUkSuhwWuM0Kcz6gRJUR_e0",
          "authDomain": "yardiai-4ca2b.firebaseapp.com",
          "databaseURL": "https://yardiai-4ca2b.firebaseio.com",
          "storageBucket": "yardiai-4ca2b.appspot.com",
          "serviceAccount": "C:\\Users\Brandon\Documents\GitHub\YardiAI\YardiAI\YardiBackOfficeManager\YardiProcessManager\Resources\YardiAI-303194ef51f7.json"
          }
          self.firebase = pyrebase.initialize_app(self.config)

       def LoadTestData(self, NumberOfImagesToLoad, TestWriteToFileFeature):
           dm = DataManager.DataManager(True)
           
           # Locate the test folder where we store the test images.
           ParnetTestFolderPath = "C:\\FirebaseTestImages"
           ChildTestFolderPath = "C:\\FirebaseTestImages\\Images"
           

           # Retrieve all the contents from the test directory
           parentFolderFilesList = os.listdir(ParnetTestFolderPath)
           filename = parentFolderFilesList[0]
           for a in range(NumberOfImagesToLoad):
               # Rename the test image file and move it to the Images folder.
               oldFileName     = "{}\\{}".format(ParnetTestFolderPath,filename)
               newFileName     = "{}.png".format(self.GetCurrentDateTimeStamp())
               newFileLocation = "{}\\{}".format(ChildTestFolderPath,newFileName)
               fbNewFileLocation = "images/{}".format(newFileName)
               #Copy the file to child folder, TestImages
               shutil.copy(oldFileName, "{}\\{}".format(ChildTestFolderPath,newFileName))
               print("New File Copied: {}\\{}".format(ChildTestFolderPath,newFileName))

               # Add the new image to images folder in Firebase
               storage = self.firebase.storage()
               result = storage.child(fbNewFileLocation).put(newFileLocation)
               
               # Get the url of the newly image added to Firebase
               userToken = storage.credentials.access_token
               firebaseImageURL = storage.child(fbNewFileLocation).get_url(userToken)
               
               # Retrieve latitude and longitude to add to our test data.
               g = geocoder.google('Bluffton, SC')
               latitude  = g.latlng[0]
               longitude = g.latlng[1]
               
               # Add test data to the YardsTasks table
               testData = {
                   "Latitude": latitude,
                   "Longitude": longitude,
                   "CreatedDate": dm.GenerateDateTimeStamp(),
                   "ModifiedDate": dm.GenerateDateTimeStamp(),
                   "UserID": self.testUserID,
                   "ImageURL": firebaseImageURL,
                   "ImageName": newFileName,
                   "Tags": "SOD",
                   "ImageProcessed": 0,
                   "TaskComplete": 0,
                   "ImageClassified":''
               }
               
               
               db = self.firebase.database()
               result = db.child("YardTasks").push(testData)
               
               if (TestWriteToFileFeature):
                   dm = DataManager.DataManager(True);
                   dm.WriteTasksToFile(result['name'],newFileName)

               time.sleep(3)


           

           
       def GetCurrentDateTimeStamp(self):

            year    = datetime.today().year
            day     = datetime.today().day
            month   = datetime.today().month
            hour    = datetime.today().hour
            minute  = datetime.today().minute
            seconds = datetime.today().second
        
            return "{}_{}_{}_{}_{}_{}".format(year,month,day,hour,minute,seconds)