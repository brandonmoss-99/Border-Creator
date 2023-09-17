import unittest
import processor
from config import Config

class Test_borderCalculator(unittest.TestCase):
    def setUp(self):
        pass
    

    def test_BorderSizeCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": False})
        c_2 = Config({"file": "test.jpg", "border": 10, "useLong": False})

        self.assertEqual(processor.calculateBorderSize(c_1, 4000, 3000), (300,300))
        self.assertEqual(processor.calculateBorderSize(c_2, 3000, 4000), (300,300))


    def test_longBorderSizeCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": True})
        c_2 = Config({"file": "test.jpg", "border": 10, "useLong": True})

        self.assertEqual(processor.calculateBorderSize(c_1, 4000, 3000), (400,400))
        self.assertEqual(processor.calculateBorderSize(c_2, 3000, 4000), (400,400))

class Test_paddingCalculator(unittest.TestCase):
    def setUp(self):
        pass

    def test_squareRatioCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": False, "ratio": "1x1"})
        c_2 = Config({"file": "test.jpg", "border": 10, "useLong": False, "ratio": "1x1"})

        self.assertEqual(processor.calculateBorderSize(c_1, 1000, 2000), (600,100)) # 2200x2200
        self.assertEqual(processor.calculateBorderSize(c_2, 2000, 1000), (100,600)) # 2200x2200
    
    def test_longSquareRatioCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": True, "ratio": "1x1"})
        c_2 = Config({"file": "test.jpg", "border": 10, "useLong": True, "ratio": "1x1"})

        self.assertEqual(processor.calculateBorderSize(c_1, 1000, 2000), (700,200)) # 2400x2400
        self.assertEqual(processor.calculateBorderSize(c_2, 2000, 1000), (200,700)) # 2400x2400
    
    # Check wider image pads horizontally when ratio is wider than itself
    def test_wideImgWideRatioCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": True, "ratio": "3x1"})
        self.assertEqual(processor.calculateBorderSize(c_1, 2000, 1000), (1100,200)) # 4200x1400
    
    # Check wider image pads vertically when ratio is shorter than itself
    def test_wideImgShortRatioCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": True, "ratio": "5x4"})
        self.assertEqual(processor.calculateBorderSize(c_1, 2000, 1000), (200,460)) # 2400x1920

    # Check tall image pads vertically when ratio is taller than itself
    def test_tallImgWideRatioCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": True, "ratio": "1x3"})
        self.assertEqual(processor.calculateBorderSize(c_1, 1000, 2000), (200,1100)) # 1400x4200

    # Check tall image pads horizontally when ratio is shorter than itself
    def test_tallImgShortRatioCalculation(self):
        c_1 = Config({"file": "test.jpg", "border": 10, "useLong": True, "ratio": "4x5"})
        self.assertEqual(processor.calculateBorderSize(c_1, 1000, 2000), (460,200)) # 2400x1920


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