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
