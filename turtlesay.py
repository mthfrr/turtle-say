#!/usr/bin/env python3

from datetime import datetime
from io import BytesIO
import svgwrite
from cairosvg import svg2png
import cairo
import logging
import svgtextbox


logging.basicConfig(level=logging.DEBUG)

def turtle_say(text, size=75, interline_ratio=0.5, side_pad=10) -> BytesIO:
    SIZE = 512
    IMG_SCALE = 3.5
    IMG_INSERT = SIZE - 128 * IMG_SCALE

    txt_box_insert = (180, 6)
    txt_box_size = (SIZE - txt_box_insert[0] - 6, 250)

    dwg = svgwrite.Drawing(profile='tiny', size=(SIZE, SIZE), debug=True)

    # loading turtle
    base_img = svgwrite.image.Image(
        "base/turtle.svg", insert=(0, 0), size=(SIZE, SIZE))
    base_img.translate(0, IMG_INSERT)
    base_img.scale(IMG_SCALE)
    dwg.add(base_img)

    rect = svgwrite.shapes.Rect(txt_box_insert, txt_box_size)
    # dwg.add(rect)
    
    txt = svgtextbox.textBuilder(text, txt_box_size[0] - side_pad, size, interline_ratio, font="James Tan Dinawanao")
    txt.center(txt_box_size[1])
    txt.translate(txt_box_insert[0] + side_pad, txt_box_insert[1])

    txtgroup = svgwrite.container.Group()
    txtgroup.add(rect)
    txtgroup.add(txt)
    txtgroup.skewX(2)
    txtgroup.skewY(2)
    txtgroup.translate(-30, 0)

    dwg.add(txtgroup)

    # export as image
    svg_code = dwg.tostring()
    logging.debug(svg_code)
    out = svg2png(bytestring=svg_code, write_to=None)
    with open("output.png", "wb") as f:
        f.write(out)
    return BytesIO(out)


if __name__ == "__main__":
    turtle_say("OUI OUI ALLER")
    turtle_say("TA GUEULE", 60, side_pad=20)
    #turtle_say("NON", 140)
    #turtle_say("Ok ...", 140)
    turtle_say("Ok", 250, side_pad=25)
    turtle_say("SAY", 170, side_pad=23)
    turtle_say(str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")), 65)
    #turtle_say("RTFM", 130)
    turtle_say("OK MAIS TA GUEULE", 67, side_pad=18)