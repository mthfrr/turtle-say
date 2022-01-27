#!/usr/bin/env python3

from cgi import test
from enum import Flag
from discord import InvalidArgument
import svgwrite
from cairosvg import svg2png
import cairo
import logging

logging.basicConfig(level=logging.DEBUG)

SIZE = 512
IMG_SCALE = 3.5
IMG_INSERT = SIZE - 128 * IMG_SCALE

txt = "OUI OUI ALLER"

txt_box_insert = (180, 6)
txt_box_size = (SIZE - txt_box_insert[0] - 6, 250)


def textsize(text: str, fontsize: float = 14, font: str = "Arial"):
    try:
        import cairo
    except Exception as e:
        return len(str) * fontsize
    surface = cairo.SVGSurface('undefined.svg', 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(
        text)
    return width, height


class line():
    def __init__(self, size: float, font: str) -> None:
        self.line = ""
        self.size = size
        self.font = font

    def testadd(self, txt, sep=" "):
        l = line(self.size, self.font)
        l.line = self.line + sep + txt
        return l

    def add(self, word: str, maxwidth: int, sep=" ") -> bool:
        tmpline = self.testadd(word)
        if tmpline.width() > maxwidth:
            logging.debug(f"'{tmpline.line}' too wide: {tmpline.width():.2f}/{maxwidth}")
            return False
        self.line += sep + word
        return True

    def width(self) -> float:
        return textsize(self.line, self.size, self.font)[0]

    def height(self) -> float:
        return textsize(self.line, self.size, self.font)[1]


class paragraphe():
    def __init__(self, size: float, font: str, maxwidth: int) -> None:
        self.para = [line(size, font)]
        self.size = size
        self.font = font
        self.maxwidth = maxwidth
        self.interline = textsize("O", size, font)[1] * .3

    def add(self, txt) -> bool:
        if not self.para[-1].add(txt, self.maxwidth):
            self.para.append(line(self.size, self.font))
            if not self.para[-1].add(txt, self.maxwidth):
                return False  # could not fit in empty line
        return True

    def addList(self, l: list[str]) -> bool:
        for w in l:
            if not self.add(w):
                return False
        return True

    def width(self) -> float:
        return max(self.para, key=lambda x: x.width()).width()

    def height(self) -> float:
        return sum(map(lambda x: x.height(), self.para)) + self.interline * (len(self.para) - 1)

    def makeText(self):
        yoffset = 0
        res = []

        for l in self.para:
            yoffset += l.height()
            res.append(svgwrite.text.Text(
                l.line,
                insert=(0, yoffset),
                stroke='none',
                fill='#900',
                font_size=self.size,
                font_weight="bold",
                font_family=self.font))
            yoffset += self.interline

        return res


class textBuilder():
    def __init__(self, text: str, width: int, font: str = "Arial"):
        self.text = text
        self.width = width
        self.font = font

    def findsize(self, size: float = 10.0):
        words = self.text.split()
        while size > 5:
            para = paragraphe(size, self.font, self.width)
            if para.addList(words):
                return para
            size -= 1
        raise InvalidArgument("Unable to make text fit")


dwg = svgwrite.Drawing(profile='tiny', size=(SIZE, SIZE), debug=True)

# loading turtle
base_img = svgwrite.image.Image(
    "base/turtle.svg", insert=(0, 0), size=(SIZE, SIZE))
base_img.translate(0, IMG_INSERT)
base_img.scale(IMG_SCALE)
dwg.add(base_img)

rect = svgwrite.shapes.Rect(txt_box_insert, txt_box_size)
#dwg.add(rect)

rect = svgwrite.shapes.Rect((0, 0), (150, 100))
dwg.add(rect)

txtbld = textBuilder("OUI OUI ALLER", 100)
for t in txtbld.findsize(30).makeText():
    dwg.add(t)    

text = svgwrite.text.Text(
    txt,
    insert=(180, 230),
    stroke='none',
    fill='#900',
    font_size='90px',
    font_weight="bold",
    font_family="Arial")
#dwg.add(text)

# export as image
svg_code = dwg.tostring()
dwg.saveas('turtle.svg')
print(svg_code)
svg2png(bytestring=svg_code, write_to='output.png')
