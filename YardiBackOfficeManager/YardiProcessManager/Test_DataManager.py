import unittest
import os
import FirebaseTestDataLoader
import DataManager
import pyrebase
class Test_DataManagerTDD(unittest.TestCase):
    config = ""
    firebase = ""
    def setUp(self):
        self.config = {
          "apiKey": "AIzaSyDdd2opaT2VZUkSuhwWuM0Kcz6gRJUR_e0",
          "authDomain": "yardiai-4ca2b.firebaseapp.com",
          "databaseURL": "https://yardiai-4ca2b.firebaseio.com",
          "storageBucket": "yardiai-4ca2b.appspot.com",
          "serviceAccount": "YardiBackOfficeManager/YardiProcessManager/Resources/YardiAI-303194ef51f7.json"
        }
        self.firebase = pyrebase.initialize_app(self.config)

    def test_PublishResults(self):
        RecordKey   = "-KtbzMxrLqBycADLferl"
        ImageName = "FirebaseIcon.png"
        ExpectedImageProcessedValue = 1
        ActualImageProcessValue = 0
        dm = DataManager.DataManager(False)
        dm.PublishResults(RecordKey,ImageName)

        # Query YardsTasks table to confirm that thee ImagedProcessed is equal to 1
        db = self.firebase.database()
        results = db.child("YardTasks").child(RecordKey).get()
        ActualImageProcessValue = results.val()["ImageProcessed"]
        self.assertEqual(ExpectedImageProcessedValue,ActualImageProcessValue)

if __name__ == '__main__':
    unittest.main()
