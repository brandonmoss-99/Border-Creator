# Border Creator

Use imagemagick to add a border around images, using a % of image size

## Pre-requisites
Make sure imagemagick is either installed, or you have the executable downloaded and accessible

## Usage
Make sure the script is executable, `chmod +x addBorder.sh`

Can then run it as `addBorder.sh`, with the following options:

`-f <filepath>`: Use the image at the given filepath

`-F <folderpath>`: Use the images in the given folderpath

`-b <amount>`: How large a border to add, in % of the image size. Defaults to 5% of the short edge

`-p <path>`: The path to the imagemagick executable, if using a portable executable of it

`-l`: Use the long edge instead for the % calculation

`-h`: Display the help message
