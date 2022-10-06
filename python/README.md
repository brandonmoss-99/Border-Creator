## Prerequisites
Make sure both Python 3 and Pip are installed

## Usage
Run the script as `python borderCreator.py` or `python3 borderCreator.py`, with the following options:

`-f <filepath>`: Use the image at the given filepath

`-F <folderpath>`: Use the images in the given folderpath

`-b <amount>`: How large a border to add, in % of the image size. Defaults to 5% of the short edge

`-c <colour>`: Colour to use on the border, either as a word "cyan", or a hex code "#00ffff"

`-l`: Use the long edge instead for the % calculation

`-h`: Display the help message

## Examples

Add a white border to a single image, that's 10% of the short edge, to every edge:
```bash
python borderCreator.py -f image.jpg -b 10 -c white
```

Add a black border to every image in the `test` directory, that's 15% of that image's long edge, to every edge:
```bash
python borderCreator.py -F ../test -b 15 -c black -l
```

Add a border of colour `#00ff55` to a single image, that's 5% of the long edge, to every edge:
```bash
./addBorder.sh -f image.jpg -b 5 -c "#00ff55" -l
```