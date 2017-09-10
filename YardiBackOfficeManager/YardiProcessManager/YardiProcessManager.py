#TODO:
# Add unit test -check out these articles - http://www.blog.pythonlibrary.org/2011/03/09/python-102-an-intro-to-tdd-and-unittest/ and http://www.blog.pythonlibrary.org/2016/07/07/python-3-testing-an-intro-to-unittest/
# 

import DataManager
import FirebaseTestDataLoader as dl

dataLoader = dl.FirebaseTestDataLoader();
dataLoader.LoadTestData(5,True)
dm = DataManager.DataManager(True)
#IsConnected = dm.IsConnected()
dm.CallerGetRecentUnprocessTasks()

#UnprocessedYardTasks = dm.GetRecentPosts()
#print("Is connected {}.".format(IsConnected))
#print(UnprocessedYardTasks)