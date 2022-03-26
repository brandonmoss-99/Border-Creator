#!/bin/bash

# Get passed in args
while getopts f:F:p:b: arg; do
    case "${arg}" in
        f)file=${OPTARG};;
        F)folder=${OPTARG};;
        b)borderAmount=${OPTARG};;
        p)magicPath=${OPTARG};;
    esac
done

# Check imagemagick is installed/a path for it is supplied, otherwise exit
if [ ! -n "$magicPath" ] && ! command -v imagemagick >/dev/null 2>&1; then
    echo "Couldn't find imagemagick installed"
    echo "No path for imagemagick supplied. Exiting..."
    exit 1
fi

# If no border amount given, provide default amount
if [ ! -n "$borderAmount" ]; then
    # How much border to give. 0.05 = 5%
    borderAmount="0.05"
fi

do_processing () {
    echo "Processing: ${1}"
    # Separate filename from extension
    filename=$(echo "${1%.*}")
    ext=$(echo "${1##*.}")

    # Use imagemagick to retrieve image width & height
    width=$($magicPath/magick identify -format "%[w]" "$1")
    height=$($magicPath/magick identify -format "%[h]" "$1")

    # Use the short edge for the border size calculation
    if [ $width -ge $height ]; then
        borderSize=$(printf %2.0f $(echo "$height*$borderAmount" | bc -l))
    else
        borderSize=$(printf %2.0f $(echo "$width*$borderAmount" | bc -l))
    fi

    # Add a white border, save the image with _border in the filename
    $($magicPath/magick convert "$1" -bordercolor white -border $borderSize "${filename}_border.${ext}")
}

# If we're dealing with folder, process over every file within
if [ -n "$folder" ]; then
    for f in ${folder}/*.*; do
        do_processing $f
    done
# If just 1 file, process it
elif [ -n "$file" ]; then
    do_processing $file
fi
