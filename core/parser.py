import json
import time
from random import randint

import requests
import hashlib
from pathlib import Path

HTTP_CODE_SUCCESS = 200

urlCabinet = "https://lk.rosreestr.ru/eservices/real-estate-objects-online"
urlFindCadNum = "https://lk.rosreestr.ru/account-back/address/search"
urlData = "https://lk.rosreestr.ru/account-back/on"

myHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
}


class Error(Exception):
    pass


class ParseAddressError(Error):
    pass


class ParseFlatDataError(Error):
    pass


class Cache(object):
    @staticmethod
    def get(name):
        file = Cache.getFilePath(name)
        if Path(file).exists():
            return Path(file).read_text()
        else:
            return None

    @staticmethod
    def set(name, value):
        file = open(Cache.getFilePath(name), 'w+')
        file.write(value)
        file.close()

    @staticmethod
    def getFilePath(name):
        hash = hashlib.md5(name.encode()).hexdigest()
        return './cache/%(name)s.txt' % {"name": hash}


def parse(address, rosreestrCaptcha, cookies):
    try:
        cadNum = getCadnum(address=address, cookies=cookies)
        jsonData = getFlatData(cadNum=cadNum, rosreestrCaptcha=rosreestrCaptcha, cookies=cookies)
        if jsonData is not None:
            return json.loads(jsonData)
        else:
            return None

    except ParseAddressError as e:
        print("Не распарсено: " + str(e))
    except Exception as e:
        print(str(e))
        time.sleep(1)
        return parse(address, rosreestrCaptcha, cookies)


def getCadnum(address, cookies):
    cacheName = "address" + address
    cadNum = Cache.get(cacheName)

    if cadNum is None:
        params = {
            "term": address
        }
        response = requests.get(urlFindCadNum, headers=myHeaders, cookies=cookies, params=params, timeout=5)

        if response.status_code == HTTP_CODE_SUCCESS:
            responseJson = response.json()
            if len(responseJson) > 0 and responseJson[0].get('cadnum') is not None:
                cadNum = responseJson[0].get('cadnum')
                Cache.set(cacheName, cadNum)
            else:
                raise ParseAddressError(address)

    return cadNum


def getFlatData(cadNum, rosreestrCaptcha, cookies):
    cacheName = "data" + cadNum

    data = Cache.get(cacheName)

    if data is None:
        post = {
            "filterType": "cadastral",
            "cadNumbers": [cadNum],
            "captcha": rosreestrCaptcha
        }

        response = requests.post(urlData, headers=myHeaders, cookies=cookies, data=json.dumps(post), timeout=5)

        if response.json().get('error') == 'Wrong captcha':
            raise ParseFlatDataError('Wrong captcha')

        data = json.dumps(response.json())

        Cache.set(cacheName, data)

        time.sleep(randint(1, 5))

    return data
