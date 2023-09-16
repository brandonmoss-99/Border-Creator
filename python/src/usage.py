def getUsage():
    print('''
Usage: borderCreator<extension> [<options>]

-f <filepath>       Use the image at the given filepath
-F <folderpath>     Use the images in the given folderpath
-b <amount>         How large a border to add, in % of the image size.
                    Defaults to 5% of the short edge
-r <ratio>          The ratio to extend the borders to fit (ensuring the
                    borders don't shrink below the specified amount). Specified
                    as <width>x<height> - 4x5, 3x1, etc
-c <colour>         Colour to use on the border, either as a word
                    "cyan", or a hex code "#00ffff"
-l                  Use the long edge instead for the % calculation
-h                  Display this help message
''')
