import unittest
from mock import patch
import Execution




class MyTest(unittest.TestCase):
    
    SOURCE_FILE_OK = r'd:\temp\006_005_001'
    DESTINATION_FILE_OK = r'c:\Data'
    SOURCE_FILE_NOK = r'd:\notexist'
    DESTINATION_FILE_NOK = r'c:\Data'
    
    def __init__(self, *args, **kwargs):
        super(MyTest, self).__init__(*args, **kwargs)
        self.positive = Execution.Execute(MyTest.SOURCE_FILE_OK, MyTest.DESTINATION_FILE_OK)
        self.negative = Execution.Execute(MyTest.SOURCE_FILE_NOK, MyTest.DESTINATION_FILE_NOK)
    
    @patch('Execution.Execute.steps')
    def test_fileverif1(self,mock):
        '''Positive test If files are available'''
        self.positive.init_files()
        self.assertTrue(mock.called)
        
    @patch('Execution.Execute.steps')
    def test_fileverif2(self,mock):
        '''Negative test If files are available'''
        self.negative.init_files()
        self.assertFalse(mock.called)
        
    @patch('Execution.Execute.tal_creator')
    def test_foldercreate(self,mock):
        '''Positive test for folder creation'''
        self.positive.init_files()
        self.assertTrue(mock.called)
   


if __name__ == "__main__":
    unittest.main()