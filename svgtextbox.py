#!/usr/bin/env python3

import svgwrite
from cairosvg import svg2png
import logging


def textsize(text: str, fontsize: float = 14, font: str = "Arial"):
    try:
        import cairo
    except Exception as e:
        return len(str) * fontsize
    surface = cairo.SVGSurface(None, 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(
        text)
    
    return width, height


class line():
    def __init__(self, size: float, font: str, sep=" ") -> None:
        self.line = []
        self.size = size
        self.font = font
        self.sep = sep

    def testadd(self, txt):
        l = line(self.size, self.font, self.sep)
        l.line = list(self.line)
        l.line.append(txt)
        return l

    def add(self, word: str, maxwidth: int) -> bool:
        tmpline = self.testadd(word)
        if tmpline.width() > maxwidth:
            logging.debug(f"'{tmpline}' too wide: {tmpline.width():.2f}/{maxwidth}")
            return False
        self.line.append(word)
        return True

    def width(self) -> float:
        return textsize(str(self), self.size, self.font)[0]

    def height(self) -> float:
        return textsize(str(self), self.size, self.font)[1]

    def __str__(self):
        return self.sep.join(self.line)


class paragraphe():
    def __init__(self, size: float, font: str, maxwidth: int, inter_ratio: float, color) -> None:
        self.para = [line(size, font)]
        self.size = size
        self.font = font
        self.maxwidth = maxwidth
        self.interline = textsize("O", size, font)[1] * inter_ratio
        self.color = color

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
        res = myCenteringGroup(self.height())

        for l in self.para:
            yoffset += l.height()
            res.add(svgwrite.text.Text(
                l,
                insert=(0, yoffset),
                stroke='none',
                fill=self.color,
                font_size=self.size,
                font_weight="bold",
                font_family=self.font))
            yoffset += self.interline

        return res

class myCenteringGroup(svgwrite.container.Group):
    def __init__(self, height: int) -> None:
        super().__init__()
        self.height = height
        
    def center(self, total_height: int):
        yoffset = (total_height - self.height) / 2
        self.translate(0, yoffset)
        

def textBuilder(text: str, width: int, size: float = 30, inter_ratio: float = .3, color='#fff', font: str = "Arial"):
        words = text.split()
        while size > 5:
            para = paragraphe(size, font, width, inter_ratio, color)
            if para.addList(words):
                return para.makeText()
            logging.debug(f"reduce font size: {size}->{size - 1}")
            size -= 1
        raise Exception("Unable to make text fit")