import time
from parse import parse
from celery import group, subtask
from flask import jsonify, Flask
from collections import Counter

app = Flask(__name__)

@app.route('/', methods=['GET'])
def count_tweets():

    time_start = time.time()
    queue = [parse.s('tweets_{}.txt'.format(x)) for x in xrange(0,20)]
    g = group(queue)

    res = g()

    while (res.ready() == False):
        time.sleep(3)

    dicts = res.get()
    counter = Counter()
    for dic in dicts:
        counter.update(dic)

    time_end = time.time()
    elapsed_time = time_end - time_start
    d = dict(counter)
    dic_time = {'Elapsed Time:' : elapsed_time}
    d.update(dic_time)


    return jsonify(d), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
