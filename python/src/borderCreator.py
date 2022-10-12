from wand.image import Image
from wand.color import Color
from wand.version import formats
from threading import Thread
import getopt, sys, os

from config import Config
import usage

# Do the image processing
def process(path):
    print(f"Processing {path}")
    # Separate filename from extension
    fNameSplit = path.rsplit('.', 1)
    filename = fNameSplit[0]
    ext = fNameSplit[1]

    # Open the image and do the processing
    with Image(filename = path) as toProcess:
        width = toProcess.width
        height = toProcess.height

        # Use the long edge for the border size calculation if useLong is true,
        # otherwise use the short edge
        if conf.useLong:
            borderSize = int(width * (conf.borderAmount)*0.01) if width >= height else int(height * (conf.borderAmount)*0.01)
        else:
            borderSize = int(height * (conf.borderAmount)*0.01) if width >= height else int(width * (conf.borderAmount)*0.01)
        
        # Add the border, save the image with _border in the filename
        toProcess.border(color = Color(conf.colour), width = borderSize, height = borderSize)
        toProcess.save(filename = filename + "_border." + ext)


if __name__ == '__main__':    
    # Get all but the first arg from the command line
    argv = sys.argv[1:]

    # Imagemagick supported formats
    supportedFormats = formats('*')

    cParams: dict = {}

    try:
        opts, args = getopt.getopt(argv, shortopts="f:F:p:b:c:lh")

        for opt, arg in opts:
            if opt in ['-f']:
                cParams["file"] = arg
            elif opt in ['-F']:
                cParams["dir"] = arg
            elif opt in ['-b']:
                cParams["border"] = int(arg)
            elif opt in ['-c']:
                cParams["colour"] = arg
            elif opt in ['-l']:
                cParams["useLong"] = True
            elif opt in ['-h']:
                usage.getUsage()
                sys.exit(0)
    except:
        usage.getUsage()
        sys.exit(0)

    conf: Config = Config(cParams)

    # If no border amount given, provide default amount
    if conf.borderAmount is None:
        borderAmount = 5

    # If no colour given, set colour to white
    if conf.colour is None:
        colour="white"

    if conf.filePath is not None:
        process(conf.filePath)
    
    elif conf.dirPath is not None:
        threads = []

        # For each file in the folder, if it's in imagemagick's supported
        # formats, process it
        for f in os.listdir(conf.dirPath):
            nameSplit = f.rsplit('.', 1)
            ext = ""
            # Check the file is not a directory (with no extension)
            if(len(nameSplit) > 1):
                ext = nameSplit[1]
            
            if ext.upper() in supportedFormats:
                # Make sure path is in an OS friendly format
                path = os.path.join(conf.folderPath,f)

                # Create & run a new thread to process the image
                t = Thread(target = process, args = (path,))
                threads.append(t)
                t.start()

        # Wait until all the threads are finished
        for t in threads:
            t.join()
    
    else:
        print("No file/folder specified!")
        usage.getUsage()
        sys.exit(0)
