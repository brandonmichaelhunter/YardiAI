import tensorflow as tf, sys
import urllib3
import socket
import pyrebase
import time
import logging
import os
from datetime import datetime
from PIL import Image
import shutil
#import DataManager
class DataManager(object):

    config = ""
    firebase = ""
    loggerFile = "DataManager_{}_{}_{}.log".format(datetime.now().year, datetime.now().month,datetime.now().day)
    loggerLevel = "DataManager"
    enableDebug = False
    auth = ""
    user = ""
    def __init__(self, EnableDebug):
        self.config = {
          "apiKey": "AIzaSyDdd2opaT2VZUkSuhwWuM0Kcz6gRJUR_e0",
          "authDomain": "yardiai-4ca2b.firebaseapp.com",
          "databaseURL": "https://yardiai-4ca2b.firebaseio.com",
          "storageBucket": "yardiai-4ca2b.appspot.com",
          "serviceAccount": "/tf_files/grapes/YardiAI-303194ef51f7.json"
        }
        #self.config = {
        #  "apiKey": "AIzaSyDdd2opaT2VZUkSuhwWuM0Kcz6gRJUR_e0",
        #  "authDomain": "yardiai-4ca2b.firebaseapp.com",
        #  "databaseURL": "https://yardiai-4ca2b.firebaseio.com",
        #  "storageBucket": "yardiai-4ca2b.appspot.com"
        #}
        #print(self.config)
        self.firebase = pyrebase.initialize_app(self.config)
        # Get a reference to the auth service
        #self.auth = self.firebase.auth()
        # Log the user in
        #self.user = self.auth.sign_in_with_email_and_password("brandonmichaelhunter@live.com", "$harep01nt2010")
        # initalizing logging
        logging.basicConfig(filename=self.loggerFile,format="%(asctime)s:%(levelname)s:%(message)s")
        self.enableDebug = EnableDebug


    # Determines if we're connected to firebase.
    def IsConnected(self):
        # This method will see if we're connected online.
       try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("firebase.google.com", 80))
        return True
       except OSError:
        self.LogDebugMessage("We close internet !!!")
        return False

    def GetRecentPosts(self):
        queue = {}
        
        try:
            logging.info("Creating an connection object to firebase",True)
            db = self.firebase.database()
            logging.info("Creating an connection object to firebase - Completed")
            # Retrieve records that has been processed yet
            logging.info("Getting records from Firebase where ImageProcessed equals to 0")
            recs = db.child("YardTasks").order_by_child("ImageProcessed").equal_to(0).get()
            logging.info("Getting records from Firebase where ImageProcessed equals to 0 - Completed")
            #store results into local queue for processing.
            for item in recs.each():
                queue[item.key()] = item.val()["ImageName"]
        except:
            logging.error("We got an error processing GetRecentPosts")
        finally:
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
            minute = '0{}'.format(datetime.today().minute)
        else:
            minute = datetime.today().minute
        
        if(datetime.today().second < 10):
            seconds = '0{}'.format(datetime.today().second)
        else:
            seconds = datetime.today().second
        
        if(datetime.today().hour < 10):
            hour = '0{}'.format(datetime.today().hour)
        else:
            hour = datetime.today().hour
        
        if(datetime.today().month < 10):
            month = '0{}'.format(datetime.today().month)
        else:
            month = datetime.today().month

        if(datetime.today().day < 10):
           day = '0{}'.format(datetime.today().day)
        else:
            day = datetime.today().day

        #return  "%a-%a-%a %a:%a:%a" %(year,month,day,hour,minute,seconds)
        #my_datetime.strftime("%B %d, %Y")
        return datetime.isoformat(datetime.now())

    def ProccessQueueTask(self, RecordKey, ImageName):
        logging.info("Calling ProccessQueueTask")
        #store the primary key and image url into a local variable.
        recID = RecordKey
        imageName = ImageName
        try:
            # Check to see if we're connected to the internet
            if(self.IsConnected() == True):
                #Download the image to a local folder
                logging.info("Processing image {}".format(ImageName))
                storage = self.firebase.storage()
                storageQuery = "images/{}".format(ImageName)
                self.LogDebugMessage("Download File: {} ".format(storageQuery))
                # Download the file to the /tf_files/grapes folder.
                downlaodFileLoc = "/tf_files/grapes/{}".format(ImageName)
                result = storage.child(storageQuery).download(downlaodFileLoc)
                self.LogDebugMessage("File Downloaded: {} ".format(storageQuery))

                # Get the current directory where the file was executed.
                dir_path = os.path.dirname(os.path.realpath(__file__))
                self.LogDebugMessage("Converting File - {} from .png to .jpg".format(downlaodFileLoc))

                # Open the current file that was downloaded
                oldFileLocation = "{}/{}".format(dir_path,ImageName)

                # Get the filename with extension
                filename_w_ext = os.path.basename(downlaodFileLoc)

                # Extract the filename and file extension name
                filename, file_extension = os.path.splitext(filename_w_ext)

                # Add the .jpg the filename variable and add the current directory location.
                newFileLocation = "/tf_files/grapes/{}.{}".format(filename, "jpg")
                self.LogDebugMessage("Converting to {}".format(newFileLocation))
                # Convert the file to a .jpg
                currentImage = Image.open(oldFileLocation)
                rgb_im       = currentImage.convert('RGB')
                rgb_im.save(newFileLocation)
                self.LogDebugMessage("File {} has been converted".format(newFileLocation))
                #Call Tensorflow to determine what is the image
                results = self.IdentifyImage(newFileLocation)

                #Save the results back to record in the YardsTasks table.
                result  = self.PublishResults(recID,results)
                logging.info("Image {} has been processed.".format(imageName))

            else:
                logging.error("We are not connected to the internet. We will begin cashing queuing tasks")
                self.WriteTasksToFile(recID,imageName);
        except:
            logging.error("We have an error")
            self.WriteTasksToFile(recID,imageName)

    def PublishResults(self, RecordKey, AIResults):
        db = self.firebase.database()
        # publish changes to YardTasks table.
        modifiedDate = self.GenerateDateTimeStamp()
        saveResults = db.child("YardTasks").child(RecordKey).update({"ImageProcessed":1, "ImageClassified":AIResults,"ModifiedDate":modifiedDate})
        # return results back to consumer.
        return saveResults

    def WriteTasksToFile(self,RecordKey, ImageName):
        new_path = 'CachedTasks.txt'
        log = open(new_path,'a')
        log.write("{}:{}\n".format(RecordKey,ImageName))
        log.close()
    
    def ReadTasksFromFile(self):
        FilePath = 'CachedTasks.txt'
        
        # Check to see if the file exists. If it doesn, then it means we have records that needs to be processed.
        if(os.path.exists(FilePath)):
            self.LogDebugMessage("Reading from CachedTasks.txt file")
            log = open(FilePath)
            logContents = log.readlines()
            for logContent in logContents:
                result = logContent
                RecordKey = logContent.split(":")[0].strip()
                ImageName = logContent.split(":")[1].strip()
                self.LogDebugMessage("Processing {} - {}".format(RecordKey, ImageName))
                self.ProccessQueueTask(RecordKey,ImageName)
                self.LogDebugMessage("Processed {} - {}".format(RecordKey, ImageName))
            log.close()

            # Once completed, then delete the file.
            os.unlink(FilePath)

    def LogDebugMessage(self, Message):
        if(self.enableDebug):
           CurrentDateTime = self.GenerateDateTimeStamp()
           print("{}: {}".format(CurrentDateTime,Message))

    def IdentifyImage(self, FileLocation):
        image_path = FileLocation #sys.argv[1]
        self.LogDebugMessage("FILE TO BE PROCESSED: {}".format(image_path))
        # Read in the image_data
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        self.LogDebugMessage("Read in image data")
        # Loads label file, strips off carriage return
        label_lines = [line.rstrip() for line 
                           in tf.gfile.GFile("/tf_files/retrained_labels.txt")]
        self.LogDebugMessage("Loads label file, strips off carriage return ")
        returnMsg = ""
        self.LogDebugMessage("upersists graph from file")
        # Unpersists graph from file
        with tf.gfile.FastGFile("/tf_files/retrained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='') 
        
        self.LogDebugMessage("Feed the image_data as input to the graph and get first prediction")
        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})
    
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id] * 100
                # If the image is greater then 92, then move the file to its label directory.
                if(score > 92):
                   self.LogDebugMessage("Label: {} - Score: {}".format(human_string,score))
                   self.CopyFileToLabelFolder(FileLocation, human_string)

                self.LogDebugMessage("Get Prediction")
                returnMsg = '%s (score = %.2f)' % (human_string, score) 
                self.LogDebugMessage("Prediction: {}".format(returnMsg))
                break

        return returnMsg
    def CopyFileToLabelFolder(self, FileLocation, FolderName):
        try:
            # Build the folder location to where we will copy the image to
            labelFolderPath = "/tf_files/grapes/{}/".format(FolderName)
            self.LogDebugMessage("Copying {} to {}".format(FileLocation, labelFolderPath))
            shutil.copy(FileLocation,labelFolderPath)
            self.LogDebugMessage("File {} has been copied to {}".format(FileLocation, labelFolderPath))
        except:
            logging.error("There was a problem copying a file to a Label directory")
            self.LogDebugMessage("There was a proble copying a file to a label directory")


    def CallerGetRecentUnprocessTasks(self):
        #Need to add a timer that will call this every 3 seconds
        #
        while True:
            # First process any tasks that were saved to file before querying the database again.
            #self.ReadTasksFromFile()
            # Second process tasks from the database.
            queueTasks = self.GetRecentPosts()

            #Check to see if we're still connected to the internet
            if (self.IsConnected()):
                for k,v in queueTasks.items():
                    self.LogDebugMessage("Processing {} - {}".format(k,v))
                    self.ProccessQueueTask(k,v)
                    self.LogDebugMessage("Processed {} - {}".format(k,v))
            else:
                #Write the queueTasks to a to a cache file.
                self.LogDebugMessage("Client is disconnected from the internet. Currently writing queue tasks to a cache file.")
                for k,v in queueTasks.items():
                    self.WriteTasksToFile(k,v)

            self.LogDebugMessage("App is sleeping")
            time.sleep(3)
            self.LogDebugMessage("I'm awake")



dm = DataManager(True)
#IsConnected = dm.IsConnected()
dm.CallerGetRecentUnprocessTasks()




