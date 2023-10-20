import getopt, sys, usage

def createConfig(argv):
    cParams: dict = {}

    try:
        opts, args = getopt.getopt(argv, shortopts="f:F:p:b:c:r:o:a:lh")

        for opt, arg in opts:
            if opt in ['-f']:
                cParams["file"] = arg
            elif opt in ['-F']:
                cParams["dir"] = arg
            elif opt in ['-b']:
                cParams["border"] = float(arg)
            elif opt in ['-c']:
                cParams["colour"] = arg
            elif opt in ['-r']:
                cParams["ratio"] = arg
            elif opt in ['-o']:
                cParams["resize"] = arg
            elif opt in ['-a']:
                cParams["rounded"] = float(arg)
            elif opt in ['-l']:
                cParams["useLong"] = True
            elif opt in ['-h']:
                usage.getUsage()
                sys.exit(0)
    except:
        usage.getUsage()
        sys.exit(0)
    
    return cParams
