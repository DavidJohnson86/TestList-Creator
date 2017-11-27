'''
Created on 2017. nov. 24.

@author: SzuroveczD
'''
import unittest
import Execution


class MyTest(unittest.TestCase):

    SOURCE_FILE_OK = r'd:\temp\006_005_001'
    DESTINATION_FILE_OK = r'c:\Data'
    SOURCE_FILE_NOK = r'd:\temp'
    DESTINATION_FILE_NOK = r'c:\Data'

    def test_filever(self):
        '''Negative test If files are not available'''
        self.obj = Execution.Execute(MyTest.SOURCE_FILE_NOK, MyTest.DESTINATION_FILE_NOK)
        self.assertEqual(self.obj.init_files(), False)

    def test_filever1(self):
        '''Check if files are exist on the directory'''
        self.obj = Execution.Execute(MyTest.SOURCE_FILE_OK, MyTest.DESTINATION_FILE_OK)
        self.obj.init_files()
        self.assertEqual(self.obj.verification(), True)


if __name__ == '__main__':
    unittest.main()
