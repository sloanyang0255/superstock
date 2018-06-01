__author__ = 'sloanyang'

import requests
import realtime
import time

def large_volume():
    ret = []
    res = requests.get("https://tw.stock.yahoo.com/d/i/rank.php?t=down&e=tse")
    requests.get("https://tw.stock.yahoo.com/d/i/rank.php?t=down&e=tse", headers={'Connection':'close'})
    return ret

def today_all_price():
    data = realtime.yahoo_crawler()
    fp = open('Output/lastday', "w")
    for i in range(len(data)):
        for j in range(len(data[i])):
            st1 = ('%s,'%(data[i][j]))
            fp.writelines(st1)
        fp.writelines('\n')
    fp.close()

#def update_today_data():
