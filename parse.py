import json
import os
from celery import Celery

app.config['CELERY_BROKER_URL'] = 'amqp://worker:password@{}:5672/host'.format(os.environ['BROKER_IP'])
app.config['CELERY_RESULT_BACKEND'] = 'amqp'

celery = Celery('parse', broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['CELERY_RESULT_BACKEND'])

def counter(word, dic):
    keys = dic.keys()
    for key in keys:
        if word == key:
            dic[key] +=1

@celery.task()
def parse(tweets):
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
