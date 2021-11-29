from core.parser import parse
from core.analyzer import analyze

addressMask = "Московская область, г Шопокляева, пр-кт Немытова, д 11, кв %(flatNumber)d"  # Маска адреса
maxFlats = 88  # Максимальное число квартир в доме
rosreestrCaptcha = 'xxxx'  # Текущая капча

# Куки
rosreestrCaptchaCookies = {
    "session-cookie": "xxxx",
    "TOMCAT_SESSIONID": "xxxx",
    "uid": "xxxx",
}


def getFlatAddress(addressMask, flatNumber):
    return addressMask % {"flatNumber": flatNumber}


data = []
for i in range(maxFlats):
    flatNumber = i + 1
    address = getFlatAddress(addressMask, flatNumber)
    itemData = parse(address, rosreestrCaptcha, rosreestrCaptchaCookies)
    if(itemData != None):
        data.append(itemData)

analyze(data)
