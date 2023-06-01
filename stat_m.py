# Stat Module
import datetime

import requests
import cv2

cycle_cnt = 0

this_cycle_0 = 0

this_cycle_above0 = 0

frame = None
base_url = 'https://mg.markpolo.cn/api'
token = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwNzMxMGJkMGI0MzA0ZmI4YjhlYjZhNjVkYjFlODZiOSIsInN1YiI6IjEiLCJpc3MiOiJ4eWoiLCJpYXQiOjE2ODU1OTE2NDEsImV4cCI6MTY4NjE5NjQ0MX0.S9NTD0HoddR5ypT2x9jkvET8rjoXZEZLCgqeubDrbP8'


def add_record(num, _frame):
    global this_cycle_0
    global this_cycle_above0
    global cycle_cnt
    global frame
    if _frame is None:
        return
    else:
        frame = _frame
    if num == 0:
        this_cycle_0 += 1
    else:
        this_cycle_above0 += 1
    if this_cycle_above0 > 30 and this_cycle_0 > 60 and num > 0:
        make_req()
        clear()


def make_req():
    cv2.imwrite("temp.jpg", frame)
    res = requests.post(url=base_url + '/upload/file', headers={
        'token': token
    }, files={
        'file': ('1.jpg', open('temp.jpg', 'rb'))
    })
    url = res.json()["data"]
    res2 = requests.post(url=base_url + '/logs', headers={
        'token': token
    }, data={
        "level": "2",
        "message": "0",
        "sensorId": "5",
        "state": "0",
        "time": datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S'),
        "type": "2"
    })
    rid = res2.json()["data"]["id"]
    requests.post(url=base_url + 'logPicture', headers={
        'token': token
    }, data={
        'logId': rid,
        'picAddr': url
    })


def clear():
    global cycle_cnt
    global this_cycle_0
    global this_cycle_above0
    cycle_cnt = 0
    this_cycle_0 = 0
    this_cycle_above0 = 0
