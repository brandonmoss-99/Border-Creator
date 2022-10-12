import sys

from config import Config
import usage, processor, argParser

if __name__ == '__main__':    
    # Get all but the first arg from the command line, and create config
    conf: Config = Config(argParser.createConfig(sys.argv[1:]))

    if conf.filePath is not None:
        processor.processFile(conf)
    elif conf.dirPath is not None:
        processor.processDir(conf)
    else:
        print("No file/folder specified!")
        usage.getUsage()
        sys.exit(0)
