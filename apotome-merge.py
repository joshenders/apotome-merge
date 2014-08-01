#!/usr/bin/env python

import argparse
import re
import sys

from wand.image import Image
from wand.color import Color
from wand.display import display

parser = argparse.ArgumentParser(description="Tool for merging RGB TIFF images taken with a ZEISS fluorescence microscope")

parser.add_argument("-p", "--preview", action="store_true", help="Display the resulting image but do not save it")
parser.add_argument("-v", "--verbose", action="store_true", help="Produce more output")
parser.add_argument("green_channel_image")
parser.add_argument("red_channel_image")

# Print verbose help instead of terse help in case of no arguments passed
# (similar to GNU convention)
if len(sys.argv) != 2:
    parser.print_help()
    exit(1)

args = parser.parse_args()

suffix = '_composite.tiff'
pattern = re.compile(r'\.tiff?$')

# Sanity check
if pattern.search(args.green_channel_image):
    outfile = re.sub(pattern, suffix, args.green_channel_image)
else:
    sys.stderr.write("Output filename would overwrite input filename. Not a TIFF file? No action taken.\n")
    exit(1)

# We have to use a multi-staged approach with wand.display.composite_channel
# because wand 0.3.4. doesn't have ImageMagick's SetImageAlphaChannel or any
# real way to directly modify channels. The more efficient approach may
# actually be shelling out to ImageMagick proper.

# Open green_channel_image
with Image(filename=args.green_channel_image) as green:
    if args.verbose:
        for key, value in green.metadata.items():
            print(key, value)

    # Open red_channel_image
    with Image(filename=args.red_channel_image) as red:
        if args.verbose:
            for key, value in green.metadata.items():
                print(key, value)

        # Clone green_channel_image to "result" to ensure we're non-destructive
        with green.clone() as result:
            # Receive only the red channel from red_channel_image onto result
            result.composite_channel(
                channel='all_channels',
                image=red,
                operator='copy_red')

            # Remove blue channel from result by compositing it with a minus
            # operation onto final
            with result.clone() as final:
                final.composite_channel(
                    channel='blue',
                    image=result,
                    operator='minus')

                if args.preview:
                    display(final)
                else:
                    final.save(filename=outfile)
                    if args.verbose:
                        print "Composite image saved to", outfile
