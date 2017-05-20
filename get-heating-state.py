#!/usr/bin/python

import fileinput
import re
import requests

for line in fileinput.input():
    log = re.match("(\d+) manchester decode:([01]+)", line)
    if log:
        time = log.group(1)
        data = log.group(2)
        ret = requests.get('http://192.168.100.52')
        if ret.status_code != 200:
            raise Exception('return code should be 200 but is {}'.format(ret.status_code))

        json = ret.json()
        light = json['raw1'] + json['raw2']
        print(time, data, light)
