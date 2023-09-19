import unittest
import config

class Test_createConfig(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_filePath(self):
        conf = {"file": "test.jpg", "border": 10, "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.dirPath, None)
        self.assertEqual(parsedConf.filePath, "test.jpg")
    

    def test_dirPath(self):
        conf = {"dir": "test", "border": 10, "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)
        
        self.assertEqual(parsedConf.dirPath, "test")
        self.assertEqual(parsedConf.filePath, None)


    def test_borderAmount(self):
        conf = {"file": "test.jpg", "border": 10, "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.borderAmount, 10)
    

    def test_default_borderAmount(self):
        conf = {"file": "test.jpg", "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.borderAmount, 5)

    def test_borderAmount_float(self):
        conf = {"file": "test.jpg", "border": 10.5, "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.borderAmount, 10.5)
    
    def test_borderAmount_floatUnderOne(self):
        conf = {"file": "test.jpg", "border": 0.5, "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.borderAmount, 0.5)

    def test_colour(self):
        conf = {"file": "test.jpg", "border": 10, "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.colour, "black")


    def test_default_colour(self):
        conf = {"file": "test.jpg", "border": 10, "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.colour, "white")


    def test_useLong(self):
        conf = {"file": "test.jpg", "border": 10, "colour": "black", "useLong": True}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.useLong, True)


    def test_default_useLong(self):
        conf = {"file": "test.jpg", "border": 10, "colour": "black"}
        parsedConf = config.Config(conf)

        self.assertEqual(parsedConf.useLong, False)


if __name__ == '__main__':
    unittest.main()