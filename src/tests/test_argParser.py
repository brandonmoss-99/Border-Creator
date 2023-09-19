import unittest, sys
import argParser
from io import StringIO

class Test_createConfig(unittest.TestCase):
    def setUp(self):
        pass


    def test_file_1(self):
        args = ["-f", "test.jpg"]
        confDict = argParser.createConfig(args)

        self.assertEqual(confDict, {"file": "test.jpg"})
    

    def test_file_2(self):
        args = ["-f", "test.jpg", "-b", "10", "-c", "black", "-l"]
        confDict = argParser.createConfig(args)

        self.assertEqual(confDict, {"file": "test.jpg", "border": 10, "colour": "black", "useLong": True})


    def test_dict_1(self):
        args = ["-F", "test"]
        confDict = argParser.createConfig(args)

        self.assertEqual(confDict, {"dir": "test"})
    

    def test_dict_2(self):
        args = ["-F", "test", "-b", "10", "-c", "black", "-l"]
        confDict = argParser.createConfig(args)
        
        self.assertEqual(confDict, {"dir": "test", "border": 10, "colour": "black", "useLong": True})


if __name__ == '__main__':
    unittest.main()