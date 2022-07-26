# Border Creator

Use imagemagick to add a border around images, using a % of image size

## Prerequisites
Make sure imagemagick is either installed, or you have the executable downloaded and accessible

## Usage
Make sure the script is executable, `chmod +x addBorder.sh`

Can then run it as `addBorder.sh`, with the following options:

`-f <filepath>`: Use the image at the given filepath

`-F <folderpath>`: Use the images in the given folderpath

`-b <amount>`: How large a border to add, in % of the image size. Defaults to 5% of the short edge

`-c <colour>`: Colour to use on the border, either as a word "cyan", or a hex code "#00ffff"

`-p <path>`: The path to the imagemagick executable, if using a portable executable of it

`-l`: Use the long edge instead for the % calculation

`-h`: Display the help message

## Examples

Add a white border to a single image, that's 10% of the short edge, to every edge:
```bash
./addBorder.sh -f image.jpg -b 10 -c white
```

Add a black border to every image in the `test` directory, that's 15% of that image's long edge, to every edge:
```bash
./addBorder.sh -F ../test -b 15 -c black -l
```

Add a border of colour `#00ff55` to a single image, that's 5% of the long edge, to every edge, using a downloaded imagemagick executable:
```bash
./addBorder.sh -f image.jpg -b 5 -c "#00ff55" -p ../magick -l
```