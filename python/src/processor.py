from wand.image import Image
from wand.color import Color

# Do the image processing
def process(path, conf):
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
