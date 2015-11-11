# coding=utf-8
from PIL import Image
from PIL import ImageChops
import pytesseract
import requests
import shutil
import hashlib

url = "http://uems.sysu.edu.cn/elect/login/code"
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

def dealWithNoise(raw):
    return raw.replace(" ", "").replace("]", "J")

def string_to_MD5(input_string):
    return hashlib.md5(input_string.encode("utf-8")).hexdigest().upper()

if __name__ == "__main__":
    s = requests.Session()
    # s.add_header(headers)
    r = s.get("http://uems.sysu.edu.cn/elect/", headers=headers)

    r = s.get(url, stream=True)
    im = Image.open(r.raw)
    im = im.convert('L')
    im = im.point(lambda x:255 if x > 128 or x==0 else x)
    im = im.point(lambda x:0 if x < 255 else 255)
    box = (2, 2, im.size[0] - 2, im.size[1] - 2)
    im = im.crop(box)

    raw = pytesseract.image_to_string(im, lang="eng", config="-psm 7")
    loginData = {
        "username": "13331193",
        "password":"CB2E042D880E62DC8D4C7873AA296421",
        "j_code":dealWithNoise(raw),
        "lt":"",
        "_eventId":"submit",
        "gateway":"true"
    }
    r = s.post("http://uems.sysu.edu.cn/elect/login", data=loginData)
    print(r.status_code)
    print(r.url[r.url.find("sid=")+4:len(r.url)])

    