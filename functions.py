from __future__ import print_function
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np


def text_to_rgb(text, fill=None):
    font = ImageFont.truetype('5×5.ttf', 10)
    image_width = font.getsize(text)
    image = Image.new('RGB', image_width)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, fill=fill, font=font, anchor=None, spacing=1)
    # image.show()
    # image.save("test.png")
    arr_image = np.asarray(image, dtype=np.uint8)
    return arr_image


def blit(dest, src, loc):
    pos = [i if i >= 0 else None for i in loc]
    neg = [-i if i < 0 else None for i in loc]
    target = dest[tuple([slice(i, None) for i in pos])]
    lambda_add = lambda v: 0 if v is None else v
    end = (target.shape[0]+lambda_add(neg[0]), target.shape[1]+lambda_add(neg[1]))
    src = src[tuple([slice(i, j) for i, j in zip(neg, end)])]
    target[tuple([slice(None, i) for i in src.shape])] = src
    return dest
