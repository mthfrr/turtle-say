#!/usr/bin/env python3

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
    dwg.add(rect)
    
    txt = svgtextbox.textBuilder(text, txt_box_size[0] - side_pad, size, interline_ratio, font="James Tan Dinawanao")
    txt.center(txt_box_size[1])
    txt.translate(txt_box_insert[0] + side_pad, txt_box_insert[1])
    dwg.add(txt)

    # export as image
    svg_code = dwg.tostring()
    logging.debug(svg_code)
    out = svg2png(bytestring=svg_code, write_to=None)
    with open("output.png", "wb") as f:
        f.write(out)
    return out


if __name__ == "__main__":
    turtle_say("OUI OUI ALLER")