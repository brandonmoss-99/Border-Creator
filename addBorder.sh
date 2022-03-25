#!/bin/bash

# Location of the imagemagick portable executable
magicPath="/home/brandy/Desktop"

# How much border to give. 0.1 = 10%
borderAmount="0.05"

for f in ./*.jpg; do
    echo "Processing: ${f}"
    # Separate filename from extension
    # Terrible design, only works with 3 char extensions
    filename=$(echo "$f" | awk '{ print substr( $0, 1, length($0)-4 ) }')
    ext=$(echo "$f" | awk '{ print substr( $0, length($0)-3, length($0) ) }')

    # Use imagemagick to retrieve image width & height
    width=$($magicPath/magick identify -format "%[w]" "$f")
    height=$($magicPath/magick identify -format "%[h]" "$f")

    # Use the short edge for the border size calculation
    if [ $width -ge $height ]; then
        borderSize=$(printf %2.0f $(echo "$height*$borderAmount" | bc -l))
    else
        borderSize=$(printf %2.0f $(echo "$width*$borderAmount" | bc -l))
    fi

    # Add a white border, save the image with _border in the filename
    $($magicPath/magick convert "$f" -bordercolor white -border $borderSize "${filename}_border${ext}")

done
