from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.version import formats

from threading import Thread
import os

# Do the image processing
def process(path, conf):
    osPath = os.path.abspath(path)
    print(f"Processing {osPath}")

    # Open the image and do the processing
    try:
        with Image(filename = osPath) as toProcess:

            # Round the image corners first, if specified
            if conf.rounded != None:
                roundCorners(conf, toProcess)

            # Add the border, save the new image
            borderSize = calculateBorderSize(conf, toProcess.width, toProcess.height)
            toProcess.border(color = Color(conf.colour), width = borderSize[0], height = borderSize[1])

            # Resize the output image, if specified
            if conf.resize != None:
                toProcess.transform(resize=f'{conf.resize}x{conf.resize}')

            toProcess.save(filename = generateNewFilePath(conf, osPath))
    except Exception as e:
        print(f"Couldn't process {osPath} - {e}")


def generateNewFilePath(conf, originalPath) -> str:
    # Separate filename from extension
    fNameSplit = originalPath.rsplit('.', 1)

    borderText = f"_{conf.borderAmount}pct{'l' if conf.useLong else 's'}-border" if conf.borderAmount != None else ""
    arcText = f"_{conf.rounded}pct-arc" if conf.rounded != None else ""
    ratioText = f"_{int(conf.ratio.split('x')[0])}x{int(conf.ratio.split('x')[1])}" if conf.ratio != None else ""
    resizeText = f"_{conf.resize}px" if conf.resize != None else ""

    return f"{fNameSplit[0]}{borderText}{arcText}{ratioText}{resizeText}.{fNameSplit[1]}"


def calculateBorderSize(conf, width, height):
    # Use the long edge for the border size calculation if useLong is true,
    # otherwise use the short edge
    if conf.useLong:
        borderSize = int(width * (conf.borderAmount) * 0.01) if width >= height else int(height * (conf.borderAmount) * 0.01)
        if conf.ratio == None:
            return borderSize, borderSize
        else:
            return calculatePadding(conf, borderSize, width, height)
        
    else:
        borderSize = int(height * (conf.borderAmount) * 0.01) if width >= height else int(width * (conf.borderAmount) * 0.01)
        if conf.ratio == None:
            return borderSize, borderSize
        else:
            return calculatePadding(conf, borderSize, width, height)
        

def calculatePadding(conf, borderSize, width, height):
    '''
    Calculate the padding needed on an image to match a specified ratio, and
    return a tuple with the width and height of the border to be applied with
    padding added on
    '''
    
    ratio = conf.ratio.split("x")
    ratio_w = int(ratio[0])
    ratio_h = int(ratio[1])

    # Set the minimum pixel size of each dimension
    # We multiply the borderSize by 2, because imagemagick applies the borderSize
    # amount on both sides of a dimension
    img_border_min_w = width + (borderSize * 2)
    img_border_min_h = height + (borderSize * 2)

    # Check if width is larger than height. Do the calculation on longest side
    if img_border_min_w >= img_border_min_h:
        # Check if multiplying the longest dimension by the ratio will make the
        # shorter dimension less than the min dimension size. If it does, pad
        # the longer dimension, otherwise pad the shorter one
        img_shorter_dim_padded = img_border_min_w / (ratio_w/ratio_h)
        
        if img_shorter_dim_padded >= img_border_min_h:
            # Padded is larger than min. Pad the shorter side
            toPad = (img_shorter_dim_padded - img_border_min_h) / 2
            return int(borderSize),int(toPad + borderSize)
        else:
            img_longer_dim_padded = img_border_min_h * (ratio_w/ratio_h)
            toPad = (img_longer_dim_padded - img_border_min_w) / 2
            return int(toPad + borderSize), int(borderSize)
    else:
        # Image is taller than it is wide. Use height for calculating
        img_shorter_dim_padded = img_border_min_h / (ratio_h/ratio_w)

        if img_shorter_dim_padded >= img_border_min_w:
            # Padded is larger than min. Pad the shorter side
            toPad = (img_shorter_dim_padded - img_border_min_w) / 2
            return int(toPad + borderSize), int(borderSize)
        else:
            # Padded is smaller than min. Pad the longer side
            img_longer_dim_padded = img_border_min_w * (ratio_h/ratio_w)
            toPad = (img_longer_dim_padded - img_border_min_h) / 2
            return int(borderSize), int(toPad + borderSize)
    

def roundCorners(conf, image):
    radiusAmount = 0

    # Set the radius amount depending on if useLong is true
    if conf.useLong:
        radiusAmount = image.width * (conf.rounded/100) if image.width >= image.height else image.height * (conf.rounded/100)
    else:
        radiusAmount = image.height * (conf.rounded/100) if image.width >= image.height else image.width * (conf.rounded/100)

    # Perform 2 passes, first masking out the corners with white, then 
    # replacing that white with the user specified background colour
    for roundPass in [("white", "black", "screen"), (conf.colour, "white", "multiply")]:
        # Create a new blank image of the same size as the photo to process
        # to manipulate as a mask
        with Image(width=image.width, height=image.height, background=Color(roundPass[0])) as mask:

            # Create a new mask, using a rectangle with a rounded radius
            with Drawing() as ctx:
                ctx.fill_color = Color(roundPass[1])
                ctx.rectangle(left=0, top=0, width=mask.width, height=mask.height, radius=radiusAmount)
                ctx.draw(mask)
        
            # Perform a screen composite on all image channels, of the
            # original image and the new mask we just made
            image.composite_channel('all_channels', mask, roundPass[2])


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
