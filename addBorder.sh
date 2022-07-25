#!/bin/bash

# Get passed in args
while getopts f:F:p:b:l arg; do
    case "${arg}" in
        f)file=${OPTARG};;
        F)folder=${OPTARG};;
        b)borderAmount=${OPTARG};;
        p)magicPath=${OPTARG};;
        # Should we use the short or long edge for percent calculation?
        l)useLong=true;;
    esac
done

# Check imagemagick is installed/a path for it is supplied, otherwise exit
# Here we just assume that if the terminal has access to 'convert' and 'identify',
# imagemagick is probably installed on the machine
if [ ! -n "$magicPath" ] && ! command -v convert >/dev/null 2>&1 && ! command -v identify >/dev/null 2>&1; then
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
    if [ -n "$magicPath" ]; then
        width=$($magicPath/magick identify -format "%[w]" "$1")
        height=$($magicPath/magick identify -format "%[h]" "$1")
    else
        width=$(identify -format "%[w]" "$1")
        height=$(identify -format "%[h]" "$1")
    fi

    # Use the long edge for the border size calculation if useLong is true,
    # otherwise use the short edge
    if [ "$useLong" = true ]; then
        if [ $width -ge $height ]; then
            borderSize=$(printf %2.0f $(echo "$width*$borderAmount" | bc -l))
        else
            borderSize=$(printf %2.0f $(echo "$height*$borderAmount" | bc -l))
        fi
    else
        if [ $width -ge $height ]; then
            borderSize=$(printf %2.0f $(echo "$height*$borderAmount" | bc -l))
        else
            borderSize=$(printf %2.0f $(echo "$width*$borderAmount" | bc -l))
        fi
    fi

    # Add a white border, save the image with _border in the filename
    if [ -n "$magicPath" ]; then
        $($magicPath/magick convert "$1" -bordercolor white -border $borderSize "${filename}_border.${ext}")
    else
        $(convert "$1" -bordercolor white -border $borderSize "${filename}_border.${ext}")
    fi
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
