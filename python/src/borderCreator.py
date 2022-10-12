from wand.version import formats
from threading import Thread
import sys, os

from config import Config
import usage, processor, argParser

if __name__ == '__main__':    
    # Get all but the first arg from the command line, and create config
    conf: Config = Config(argParser.createConfig(sys.argv[1:]))

    # Imagemagick supported formats
    supportedFormats = formats('*')

    if conf.filePath is not None:
        processor.process(conf.filePath, conf)
    
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
                t = Thread(target = processor.process, args = (path,))
                threads.append(t)
                t.start()

        # Wait until all the threads are finished
        for t in threads:
            t.join()
    
    else:
        print("No file/folder specified!")
        usage.getUsage()
        sys.exit(0)
