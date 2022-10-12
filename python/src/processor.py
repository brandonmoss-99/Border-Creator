from wand.image import Image
from wand.color import Color
from wand.version import formats

from threading import Thread
import os

# Do the image processing
def process(path, conf):
    osPath = os.path.abspath(path)
    print(f"Processing {osPath}")
    # Separate filename from extension
    fNameSplit = osPath.rsplit('.', 1)
    filename = fNameSplit[0]
    ext = fNameSplit[1]

    # Open the image and do the processing
    with Image(filename = osPath) as toProcess:
        width = toProcess.width
        height = toProcess.height

        # Add the border, save the image with _border in the filename
        borderSize = calculateBorderSize(conf, width, height)
        toProcess.border(color = Color(conf.colour), width = borderSize, height = borderSize)
        toProcess.save(filename = filename + "_border." + ext)


def calculateBorderSize(conf, width, height) -> int:
    # Use the long edge for the border size calculation if useLong is true,
    # otherwise use the short edge
    if conf.useLong:
        return int(width * (conf.borderAmount) * 0.01) if width >= height else int(height * (conf.borderAmount) * 0.01)
    else:
        return int(height * (conf.borderAmount) * 0.01) if width >= height else int(width * (conf.borderAmount) * 0.01)


def getExtension(f: str) -> str:
    '''
    Return the extension name of a file

        Parameters:
            f (str): The file to extract the extension from
        
        Returns:
            extension (str): The extension name of the file
    '''
    nameSplit = f.rsplit('.', 1)
    # Check the file is not a directory (with no extension)
    return nameSplit[1] if len(nameSplit) > 1 else ""


def processFile(conf):
    process(conf.filePath, conf)


def processDir(conf):
    # Imagemagick supported formats
    supportedFormats = formats('*')

    threads = []

    # For each file in the folder, if it's in imagemagick's supported
    # formats, process it
    osDirPath = os.path.abspath(conf.dirPath)
    for f in os.listdir(osDirPath):
        ext = getExtension(f)
        
        if ext.upper() in supportedFormats:
            # Make sure path is in an OS friendly format
            path = os.path.join(conf.dirPath,f)

            # Create & run a new thread to process the image
            t = Thread(target = process, args = (path,conf,))
            threads.append(t)
            t.start()

    # Wait until all the threads are finished
    for t in threads:
        t.join()
