## About

Tool for merging RGB TIFF images taken with a ZEISS fluorescence microscope

## Dependencies

  * [Wand >= 0.3.7](http://docs.wand-py.org)
  * [ImageMagick >= 6.8.9](http://www.imagemagick.org)

## Installation

```
port install imagemagick
pip install wand
```

## Usage
The ouput filename will be green_channel_image's name with `_composite.tiff` appended.

```
usage: apotome-merge.py [-h] [-p] [-v] green_channel_image red_channel_image

Tool for merging RGB TIFF images taken with the ZEISS ApoTome

positional arguments:
  green_channel_image
  red_channel_image

optional arguments:
  -h, --help           show this help message and exit
  -p, --preview        Display the resulting image but do not save it
  -v, --verbose        Produce more output
```
