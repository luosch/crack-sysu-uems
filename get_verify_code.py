# coding=utf-8
from PIL import Image
from PIL import ImageChops
from io import StringIO
import pytesseract
import requests
import shutil

url = "http://uems.sysu.edu.cn/elect/login/code"
point_table = ([0] + ([255] * 255))

if __name__ == "__main__":
    r = requests.get(url, stream=True)

    im = Image.open(r.raw)
    im = im.convert('L')
    im = im.point(lambda x:255 if x>128 or x==0 else x)
    im = im.point(lambda x:0 if x<255 else 255)
    box = (3, 3, im.size[0] - 3, im.size[1] - 3)
    im = im.crop(box)
    im.show()
    im.save("test.tif")
    print(pytesseract.image_to_string(im, lang="eng", config="-psm 7"))

    