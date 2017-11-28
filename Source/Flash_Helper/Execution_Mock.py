import unittest
from mock import patch
import Execution
import shutil
import os
from time import sleep
import stat


class MyTest(unittest.TestCase):

    SOURCE_FILE_OK = r'd:\temp\006_005_001'
    DESTINATION_FILE_OK = r'c:\Data'
    SOURCE_FILE_NOK = r'd:\notexist'
    DESTINATION_FILE_NOK = r'c:\Data'

    def __init__(self, *args, **kwargs):
        super(MyTest, self).__init__(*args, **kwargs)
        self.positive = Execution.Execute(
            MyTest.SOURCE_FILE_OK,
            MyTest.DESTINATION_FILE_OK,
            console=False)
        self.negative = Execution.Execute(
            MyTest.SOURCE_FILE_NOK,
            MyTest.DESTINATION_FILE_NOK,
            console=False)

    def test_copyfiles(self):
        '''Positive test if copy files are ok'''
        self.positive.init_files()
        self.positive.create_folders()
        self.assertEqual(self.positive.steps(), True)

    #===========================================================================
    # def test_folderexist2(self):
    #     '''Negative test if Folder are not available'''
    #     self.positive.init_files()
    #     Helper.delete_folders(
    #         self.positive.directories,
    #         self.positive.destination_folder,
    #         self.positive.sw_ver)
    #     sleep(1)
    #     self.assertEqual(self.positive.create_folders(), True)
    #===========================================================================

    def test_folderexist1(self):
        '''Positive test if Folder is available'''
        self.positive.init_files()
        self.assertEqual(self.positive.create_folders(), False)

    def test_filever1(self):
        '''Negative test if Files are not available'''
        self.assertEqual(self.negative.init_files(), False)

    def test_filever2(self):
        '''Positive test if Files are available'''
        self.assertEqual(self.positive.init_files(), True)


class Helper():

    @staticmethod
    def delete_folders(directories, destination_folder, sw_ver):
        """Create folders with same name as SW version in the specified folders."""
        for folder in directories:
            os.chdir(destination_folder + folder)
            try:
                shutil.rmtree(destination_folder + folder + '\\' + sw_ver)
            except WindowsError as error:
                print(error)


if __name__ == "__main__":
    unittest.main()
