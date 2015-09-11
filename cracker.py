# coding=utf-8
from PIL import Image
from PIL import ImageChops
import pytesseract
import requests
import hashlib
from html.parser import HTMLParser
import json

WARNING = '\033[93m'
ENDC = '\033[0m'

class Cracker(object):
    """
    : @_user: student's account number
    : @_password: password in md5 form
    """
    __slots__ = ("_user", "_password", "_session", "_sid")
    def __init__(self, user, password):
        self._user = user
        self._password = hashlib.md5(password.encode("utf-8")).hexdigest().upper()
        self._session = requests.Session()

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def isLogin(self):
        return self._isLogin

    @user.setter
    def user(self, value):
        self._user = value

    @password.setter
    def password(self, value):
        self._password = hashlib.md5(value.encode("utf-8")).hexdigest().upper()
    
    """
    : @return True/False depends on login status
    """
    def login(self):
        req = self._session.get(
            "http://uems.sysu.edu.cn/elect/",
            headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        )

        req = self._session.get("http://uems.sysu.edu.cn/elect/login/code", stream=True)
        im = Image.open(req.raw)
        im = im.convert('L')
        im = im.point(lambda x:255 if x > 128 or x==0 else x)
        im = im.point(lambda x:0 if x < 255 else 255)
        box = (3, 3, im.size[0] - 3, im.size[1] - 3)
        im = im.crop(box)

        raw = pytesseract.image_to_string(im, lang="eng", config="-psm 7")
        loginData = {
            "username": self._user,
            "password": self._password,
            "j_code": raw.replace(" ", "").replace("]", "J").replace("5", "S"),
            "lt":"",
            "_eventId":"submit",
            "gateway":"true"
        }
        req = self._session.post("http://uems.sysu.edu.cn/elect/login", data=loginData)

        if req.status_code == 200:
            self._sid = req.url[req.url.find("sid=")+4:len(req.url)]
            return True
        else:
            return False

    """
    : @return selection status
    """
    def selectCourse(self, courseID):
        selectData = {
            "jxbh": str(courseID),
            "sid": self._sid
        }
        req = self._session.post(
            "http://uems.sysu.edu.cn/elect/s/elect",
            data=selectData
        )
        content = req.content
        html_parser = HTMLParser()
        txt = html_parser.unescape(content.decode("utf-8"))

        start = txt.find("<textarea>")
        end = txt.find("</textarea>")
        txt = txt[start + len("<textarea>"):end]
        infoData = json.loads(txt)
        if infoData["err"]["code"] == 0:
            return "select %s successfully" % str(courseID)
        elif infoData["err"]["caurse"]:
            return infoData["err"]["caurse"]
        else:
            return "select %s failed" % str(courseID)