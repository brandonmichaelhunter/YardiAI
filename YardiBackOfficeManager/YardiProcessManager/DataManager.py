#
# DataManager is a class that will provide clients with methods to connect to any data source.
#
import urllib3
import socket
import pyrebase
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
        
        db = self.firebase.database()
        recs = db.child("Commands").get()
        return recs
        


