import json
import os
import subprocess
from subprocess import call
from celery import Celery

celery = Celery('parse', broker='amqp://worker:pw@130.238.29.102:5672/host', backend='amqp')

def counter(word, dic):
    keys = dic.keys()
    for key in keys:
        if word == key:
            dic[key] +=1

@celery.task()
def parse(tweets):
    name = 'curl -O http://smog.uppmax.uu.se:8080/swift/v1/tweets/' + tweets
    subprocess.check_call(name, shell=True)
    dic = {'han': 0, 'hon': 0, 'den': 0, 'det': 0,
            'denna': 0, 'denne': 0, 'hen': 0}

    with open(tweets, 'r') as f:
        rows = f.readlines()
        for row in rows:
            if not row == '\n':
                json_row = json.loads(row)
                if 'retweeted_status' not in json_row:
                    words = json_row['text'].split()
                    for word in words:
                        counter(word.lower(), dic)
    return dic
