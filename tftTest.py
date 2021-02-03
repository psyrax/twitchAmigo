# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will draw a few rectangles onto the screen along with some text
on top of that.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import re

# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 12

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.CE1)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = ili9341.ILI9341(
    spi,
    rotation=0,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a green filled box as the background
draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
disp.image(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

# Draw Some Text
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi pulvinar nulla dolor, a vehicula turpis lobortis vitae. Nam sapien ante, ultricies ac lacinia non, elementum nec tellus. Sed sit amet augue nec risus dignissim lacinia et ac augue. Aenean tincidunt enim in lobortis vestibulum."
linedText = re.sub("(.{37})", "\\1\n", text, 0, re.DOTALL)
(font_width, font_height) = font.getsize(linedText)
nextLine = linedText.count(
    '\n') * font.getsize(linedText)[1] + (font.getsize(linedText)[1] * 2)
print(nextLine)
draw.text(
    (0,0),
    linedText,
    font=font,
    fill=(255, 255, 255),
)


draw.text(
    (0, nextLine),
    linedText,
    font=font,
    fill=(255, 255, 255),
)

# Display image.
disp.image(image)

