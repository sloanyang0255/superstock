__author__ = 'sloanyang'

import requests
import re
from bs4 import BeautifulSoup
import json
import time
import gfunction

def exchangehistory(stockid, searchtime):
    url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=date***01&stockNo=id***&_=1517841111531"
    url = url.replace('id***', stockid)
    url = url.replace('date***', searchtime)
    res = requests.get(url)
    time.sleep(0.01)
    requests.get(url, headers={'Connection':'close'})
    time.sleep(3)
    son_data = json.loads(res.text)
    if('data' in son_data):
        return son_data['data']
    else:
        return 'none'

def overthecounterhistory(stockid, searchtime):
    url = "http://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d=date***&stkno=id***&_=1517841994133"
    url = url.replace('id***', stockid)
    url = url.replace('date***', searchtime)
    res = requests.get(url)
    time.sleep(0.01)
    requests.get(url, headers={'Connection':'close'})
    time.sleep(3)
    son_data = json.loads(res.text)
    if('aaData' in son_data):
        return son_data['aaData']
    else:
        return 'none'


def emhistory(stockid, searchtime):
    ret = []
    ret = searchtime.split('/')
    searchtime = ("%d/%02d"% (int(ret[0]), int(ret[1])))
    ret.clear()
    url = "http://www.tpex.org.tw/web/emergingstock/single_historical/result.php?l=zh-tw"
    payload = {
        'ajax':'true'
        ,'input_month':'---'
        ,'input_emgstk_code':'---'
    }
    payload['input_month'] = searchtime
    payload['input_emgstk_code'] = stockid
    res = requests.post(url, data=payload)
    time.sleep(0.01)
    res = requests.post(url, data=payload, headers={'Connection':'close'})
    time.sleep(3)
    soup = BeautifulSoup(res.text, "html.parser")
    res = soup.find_all('tr')

    for i in res:
        ret.append(i.text.split('\n'))
    del ret[0]
    del ret[0]
    return ret
    # format:
    # ['', '107/02/02', '2,423,079', '76.00', '71.00', '74.71', '1,509', '0', '0.00', '0.00', '0.00', '0', '']

def history_data(stock_id, time, type):
    if type == 'ex':
        ret = time.split('/')
        res = exchangehistory(stock_id, ("%d%02d"% (int(ret[0]), int(ret[1]))))
    elif type == 'otc':
        ret = time.split('/')
        res = overthecounterhistory(stock_id, ("%d/%02d"% (int(ret[0])-1911, int(ret[1]))))
    else:
        ret = time.split('/')
        res = emhistory(stock_id, ("%d/%02d"% (int(ret[0])-1911, int(ret[1]))))
    return res

def day60info(stockid, type):
    res = []
    nowtime = time.strftime("%Y/%m")
    lasttime = gfunction.getlasttime(nowtime)
    if type == 'ex':
        ret = lasttime.split('/')
        res.extend(exchangehistory(stockid, ("%d%02d"% (int(ret[0]), int(ret[1])))))
        ret = nowtime.split('/')
        res.extend(exchangehistory(stockid, ("%d%02d"% (int(ret[0]), int(ret[1])))))
    elif type == 'otc':
        ret = lasttime.split('/')
        res.extend(overthecounterhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1])))))
        ret = nowtime.split('/')
        res.extend(overthecounterhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1])))))
    else:
        ret = lasttime.split('/')
        res.extend(emhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1])))))
        ret = nowtime.split('/')
        res.extend(emhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1])))))
    return res


def thismonthinfo(stockid, type):
    nowtime = time.strftime("%Y/%m")
    if type == 'ex':
        ret = nowtime.split('/')
        res = exchangehistory(stockid, ("%d%02d"% (int(ret[0]), int(ret[1]))))
    elif type == 'otc':
        ret = nowtime.split('/')
        res = overthecounterhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1]))))
    else:
        ret = nowtime.split('/')
        res = emhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1]))))
    return res

def rangedata(stockid, type, stime, etime):
    print('download ' + stockid)
    slidertime = stime
    while(slidertime != etime):
        print(slidertime + '...')
        ret = slidertime.split('/')
        if type == 'ex':
            res = exchangehistory(stockid, ("%d%02d"% (int(ret[0]), int(ret[1]))))
        elif type == 'otc':
            res = overthecounterhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1]))))
        else:
            res = emhistory(stockid, ("%d/%02d"% (int(ret[0])-1911, int(ret[1]))))
        # 開啟檔案
        fp = open(stockid, "a")
        # 寫入檔案
        for line in res:
            #s1 = line
            fp.write(str(line)+'\n')
        # 關閉檔案
        fp.close()

        if ret[1] != '12':
            slidertime = "%d/%02d"%(int(ret[0]), int(ret[1])+1)
        else:
            slidertime = "%d/01"%(int(ret[0])+1)