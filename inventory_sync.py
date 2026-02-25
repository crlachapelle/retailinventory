import csv
import time

def do_stuff(f):
    out = []
    with open(f, 'r') as file:
        r = csv.reader(file)
        next(r)
        for x in r:
            if int(x[2]) < 10:
                out.append({'id': x[0], 'n': x[1], 'q': x[2], 'flag': True})
            else:
                out.append({'id': x[0], 'n': x[1], 'q': x[2], 'flag': False})
    return out

def up(data):
    time.sleep(1)
    for d in data:
        if d['flag']:
            print("ALERT: Low stock for " + d['n'])
