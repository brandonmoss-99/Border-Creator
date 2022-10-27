import unittest
import processor
from config import Config

class Test_borderCalculator(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_BorderSizeCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": False})
        self.assertEqual(processor.calculateBorderSize(c_1, 4000, 3000), 300)

        c_2 = Config({"file": "test.jpg", "border": 10, "useLong": False})
        self.assertEqual(processor.calculateBorderSize(c_2, 3000, 4000), 300)

    def test_longBorderSizeCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": True})
        self.assertEqual(processor.calculateBorderSize(c_1, 4000, 3000), 400)

        c_2 = Config({"file": "test.jpg", "border": 10, "useLong": True})
        self.assertEqual(processor.calculateBorderSize(c_2, 3000, 4000), 400)


class Test_extensionParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_jpg(self):
        f = "test.jpg"
        self.assertEqual(processor.getExtension(f), "jpg")
    
    def test_multidotFile(self):
        f = "test.file.jpg"
        self.assertEqual(processor.getExtension(f), "jpg")

    def test_manyMultidotFile(self):
        f = "test.file.with.many.dots.png.jpg.tiff.jpg.png"
        self.assertEqual(processor.getExtension(f), "png")
    
    def test_noExtension(self):
        f = "directory"
        self.assertEqual(processor.getExtension(f), "")
    

if __name__ == '__main__':
    unittest.main()