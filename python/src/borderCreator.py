from wand.image import Image
from wand.color import Color
from wand.version import formats
from threading import Thread
import getopt, sys, os

def getUsage():
    print('''
Usage: borderCreator<extension> [<options>]

-f <filepath>       Use the image at the given filepath
-F <folderpath>     Use the images in the given folderpath
-b <amount>         How large a border to add, in % of the image size.
                    Defaults to 5% of the short edge
-c <colour>         Colour to use on the border, either as a word
                    "cyan", or a hex code "#00ffff"
-l                  Use the long edge instead for the % calculation
-h                  Display this help message
''')
    sys.exit(0)

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
        if useLong:
            borderSize = int(width * (borderAmount)*0.01) if width >= height else int(height * (borderAmount)*0.01)
        else:
            borderSize = int(height * (borderAmount)*0.01) if width >= height else int(width * (borderAmount)*0.01)
        
        # Add the border, save the image with _border in the filename
        toProcess.border(color = Color(colour), width = borderSize, height = borderSize)
        toProcess.save(filename = filename + "_border." + ext)


if __name__ == '__main__':
    # Get all but the first arg from the command line
    argv = sys.argv[1:]

    file = None
    folder = None
    borderAmount = None
    colour = None
    useLong = False

    # Imagemagick supported formats
    supportedFormats = formats('*')

    try:
        opts, args = getopt.getopt(argv, shortopts="f:F:p:b:c:lh")

        for opt, arg in opts:
            if opt in ['-f']:
                file = arg
            elif opt in ['-F']:
                folder = arg
            elif opt in ['-b']:
                borderAmount = int(arg)
            elif opt in ['-c']:
                colour = arg
            elif opt in ['-l']:
                useLong = True
            elif opt in ['-h']:
                getUsage()
    except:
        getUsage()

    # If no border amount given, provide default amount
    if borderAmount is None:
        borderAmount = 5

    # If no colour given, set colour to white
    if colour is None:
        colour="white"

    if file is not None:
        process(file)
    
    elif folder is not None:
        threads = []

        # For each file in the folder, if it's in imagemagick's supported
        # formats, process it
        for f in os.listdir(folder):
            nameSplit = f.rsplit('.', 1)
            ext = ""
            # Check the file is not a directory (with no extension)
            if(len(nameSplit) > 1):
                ext = nameSplit[1]
            
            if ext.upper() in supportedFormats:
                # Make sure path is in an OS friendly format
                path = os.path.join(folder,f)

                # Create & run a new thread to process the image
                t = Thread(target = process, args = (path,))
                threads.append(t)
                t.start()

        # Wait until all the threads are finished
        for t in threads:
            t.join()
    
    else:
        print("No file/folder specified!")
        getUsage()
