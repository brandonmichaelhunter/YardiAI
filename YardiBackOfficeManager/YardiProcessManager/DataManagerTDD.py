import unittest
import os
import FirebaseTestDataLoader
class Test_DataManagerTDD(unittest.TestCase):
    
    def test_LoadTestData(self):
        # Delete any existing files in the test images folder
        TestImageLocation = "C:\\FirebaseTestImages\\Images"
        OldImagesList = os.listdir(TestImageLocation)
        for ImageItem in OldImagesList:
            os.unlink("{}\\{}".format(TestImageLocation,ImageItem))
         
        fbTestLoader = FirebaseTestDataLoader.FirebaseTestDataLoader();
        # Test the LoadTestData method and have it create 10 images.
        ExpectedCreatedImages = 10
        fbTestLoader.LoadTestData(ExpectedCreatedImages,False)

        #Setup test configuration for testing against the LoadTestData method.
        
        ActualImagesCreated = 0
        ImagesList = os.listdir(TestImageLocation)
        for ImageItem in ImagesList:
            ActualImagesCreated += 1

        self.assertEqual(ExpectedCreatedImages,ActualImagesCreated)

if __name__ == '__main__':
    unittest.main()
