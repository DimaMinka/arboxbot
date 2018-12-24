from requests import Request, Session
import json
from pprint import pprint
import datetime

s = Session()
userID = ''
membrshipUser = ''

WOD = 'W.O.D'
OPEN_GYM = 'Open Gym'

def bookClass(classDate, classTime, category):
    classDateStr = classDate.strftime("%Y-%m-%d")
    # Get the day schedule
    queryParams = box + '/?date=' + classDateStr + '&userId=' + userID
    url = 'https://apiapp.arboxapp.com/index.php/api/v1/scheduleByDateList/' + queryParams
    req = Request('GET', url)
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    print('GET scheduleByDateList:' + str(resp.status_code))

    scheduleDay = json.dumps(resp.json(), indent=4, separators=(',', ':'))
    with open('data.json', 'w') as outfile:
        outfile.write(scheduleDay)
    outfile.close()

    daySchedule = resp.json()['Kfar-Saba']

    for c in daySchedule[0]:
        if c['category'] == category and c['schedule']['time'] == classTime:
            print('Category: ' + c['category'])
            print('Schedule ID: ' + str(c['schedule']['id']))
            print('Schedule: ' + c['schedule']['time'])
            url = 'https://apiapp.arboxapp.com/index.php/api/v1/scheduleUser'
            data = f'''
            {
                "membrshipUserFk": {membrshipUser},
                "scheduleFk": {c['schedule']['id']},
                "userFk": {userID}
            }
            '''
            print('Data = ' + data)
            req = Request('POST', url, data=data)
            prepped = s.prepare_request(req)
            resp = s.send(prepped)
            print('POST scheduleUser:' + str(resp.status_code) + str(resp.content))
            if resp.status_code == 200:
                print('+++ Succesfully register %s, %s at %s' % (classDateStr, classDate.strftime("%A"), classTime))
            else:
                print('--- Fail to register %s, %s at %s' % (classDateStr, classDate.strftime("%A"), classTime))



# Login, get API token
url = 'https://apiapp.arboxapp.com/index.php/api/v1/user/avi.uziel@gmail.com/session'
data = '''{
  "email": "avi.uziel@gmail.com",
  "password": "avicf"
}'''
s.headers.update({'Content-Type': 'application/json;charset=UTF-8'})

req = Request('OPTIONS', url, data=data)
prepped = s.prepare_request(req)
resp = s.send(prepped)
print('OPTIONS:' + str(resp.status_code))

req = Request('POST', url, data=data)
prepped = s.prepare_request(req)
resp = s.send(prepped)
print('POST: ' + str(resp.status_code))
content = resp.json()
print(content)

userID = str(content[u"user"][u"id"])
token = content[u"token"]
box = str(content[u"user"][u"locationBox"][u"boxFk"])
print("userID: " + str(userID) + "\ntoken: " + str(token) + "\nbox: " + str(box))

s.headers.update({'accessToken': token})

url = 'https://apiapp.arboxapp.com/index.php/api/v1/membership/' + userID
req = Request('GET', url)
prepped = s.prepare_request(req)
resp = s.send(prepped)
print('GER membership: ' + str(resp.status_code))
content = resp.json()
print(content)
membrshipUser = content[0]['id']

# Find next friday

today = datetime.date.today()
sunday = (today + datetime.timedelta( (6-today.weekday()) % 7 ))
monday = (today + datetime.timedelta( (0-today.weekday()) % 7 ))
tuesday = (today + datetime.timedelta( (1-today.weekday()) % 7 ))
wednsday = (today + datetime.timedelta( (2-today.weekday()) % 7 ))
thurdsday = (today + datetime.timedelta( (3-today.weekday()) % 7 ))
friday = (today + datetime.timedelta( (4-today.weekday()) % 7 ))

# bookClass(sunday, '07:00:00', WOD)
# bookClass(monday, '06:00:00', WOD)
# bookClass(wednsday, '06:00:00', WOD)
bookClass(monday, '07:00:00', WOD)
