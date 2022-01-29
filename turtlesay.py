#!/usr/bin/env python3

import subprocess
from datetime import datetime
from io import BytesIO, FileIO
import svgwrite
import logging
import svgtextbox
from wand.color import Color
from wand.image import Image
import os


logging.basicConfig(level=logging.DEBUG)

#def turtle_say(text, size=75, interline_ratio=0.5, side_pad=10) -> BytesIO:
def turtle_say(text: str, size: float = 300, padl: float = .05, padm: float = .4, padr:float = .05) -> BytesIO:
    SIZE = 512
    IMG_SCALE = 0.8
    IMG_INSERT = SIZE * (1 - IMG_SCALE)

    txt_box_insert = (180, 6)
    txt_box_size = (SIZE - txt_box_insert[0] - 6, 250)

    dwg = svgwrite.Drawing(profile='full', size=(SIZE, SIZE), debug=True)

    # loading turtle
    base_img = svgwrite.image.Image(
        "file://" + os.getcwd() + "/base/turtle.svg", insert=(0, 0), size=(SIZE, SIZE))
    base_img.translate(0, IMG_INSERT)
    base_img.scale(IMG_SCALE)
    dwg.add(base_img)

    #f = dwg.add(svgwrite.filters.Filter())
    f = svgwrite.filters.Filter()
    dwg.defs.add(f)
    f.feTurbulence(type="turbulence", baseFrequency="0.05", numOctaves=1, result="turbulence")
    f.feDisplacementMap(in_="SourceGraphic", in2="turbulence", scale="3",
                        xChannelSelector="R", yChannelSelector="G")

    rect = svgwrite.shapes.Rect(txt_box_insert, txt_box_size)
    #dwg.add(rect)
    
    #txt = svgtextbox.textBuilder(text, txt_box_size[0] - side_pad, size, interline_ratio, font="James Tan Dinawanao")
    txt = svgtextbox.textBuilder2(text, txt_box_size[0], size, pad=(padl, padm, padr), f=f)#font="James Tan Dinawanao")
    txt.center(txt_box_size[1])
    txt.translate(txt_box_insert[0], txt_box_insert[1])

    txtgroup = svgwrite.container.Group()
    txtgroup.add(rect)

    txtgroup.add(txt)
    txtgroup.skewX(-2)
    txtgroup.skewY(2)
    txtgroup.translate(-10, 0)

    dwg.add(txtgroup)


    # export as image
    svg_code = dwg.tostring()
    #logging.debug(svg_code)

    # convert -background transparent output.svg output.png


    with open("output.svg", "w") as f:
        f.write(svg_code)

    subprocess.run(["convert", "-background", "transparent", "output.svg", "output.png"])

    with open("output.png", "rb") as f:
        out = f.read()
    
    """
    with Image(blob=svg_code.encode("utf-8"), format="svg", background=Color('transparent')) as image:
        out = image.make_blob("png")

    out = svg2png(bytestring=svg_code, write_to=None)
    
    with open("output.svg", "w") as f:
        f.write(svg_code)
    with open("output.png", "wb") as f:
        f.write(outio.read())
    """
    return BytesIO(out)


if __name__ == "__main__":
    turtle_say("NICE//NICE", size=75)