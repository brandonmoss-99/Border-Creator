# Border Creator
Use imagemagick to add a border around images, using a % of image size

## Prerequisites
Make sure both Python 3 and Pip are installed

Install the required dependencies, `pip install -r requirements.txt` or `pip3 install -r requirements.txt`

## Usage
Run the script as `python src/borderCreator.py` or `python3 src/borderCreator.py`, with the following options:

`-f <filepath>`: Use the image at the given filepath

`-F <folderpath>`: Use the images in the given folderpath

`-b <amount>`: How large a border to add, in % of the image size. Defaults to 5% of the short edge

`-r <amount>`: The ratio to extend the borders to fit (ensuring the borders don't shrink below the specified border amount), as \<width>x\<height>, 5x4, 1x1, etc

`-c <colour>`: Colour to use on the border, either as a word "cyan", or a hex code "#00ffff"

`-o <size>`: The output size of the longest edge, in pixels, 1024, 2048, etc

`-a <amount>`: How much Arc (rounding) to apply to the original image corners, in % of the image size

`-l`: Use the long edge instead for the % calculation

`-h`: Display the help message

## Examples

Add a white border to a single image, that's 10% of the short edge, to every edge:
```bash
python src/borderCreator.py -f image.jpg -b 10 -c white
```

Add a black border to every image in the `test` directory, that's 15% of that image's long edge, to every edge:
```bash
python src/borderCreator.py -F ../test -b 15 -c black -l
```

Add a border of colour `#00ff55` to a single image, that's 5% of the long edge, to every edge:
```bash
python src/borderCreator.py -f image.jpg -b 5 -c "#00ff55" -l
```

Add a border of colour `#00ff55` to a single image, that's 5% of the long edge, to every edge. Within the original image, apply a 1% of the long edge rounding amount to each corner:
```bash
python src/borderCreator.py -f image.jpg -b 5 -c "#00ff55" -a 1 -l
```

Add a border of colour `#00ff55` to a single image, that's 5% of the long edge, to every edge. Extend the borders to fit a 1x1 (square) aspect ratio:
```bash
python src/borderCreator.py -f image.jpg -b 5 -c "#00ff55" -l -r 1x1
```

Add a border of colour `#00ff55` to a single image, that's 5% of the long edge, to every edge. Extend the borders to fit a 5x4 aspect ratio, and then resize so the output is 2048px on the longest side (preserving the existing 5x4 aspect ratio)
```bash
python src/borderCreator.py -f image.jpg -b 5 -c "#00ff55" -l -r 5x4 -o 2048
```