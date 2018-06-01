__author__ = 'sloanyang'

import requests
from bs4 import BeautifulSoup
import re
import realtime

def exchangestockid():  # 取得上市公司id一覽
    url = 'http://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    list = soup.select('tr')

    list1 = []
    for item in list:
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('', str(item))
        dd = dd.split('\n')
        list1.append(dd[3].strip(' '))
        list1.append(dd[4].strip(' '))

    return list1

def overthecounterstockid():  # 取得上櫃公司id一覽
    url = 'http://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    list = soup.select('tr')
    list1 = []
    for item in list:
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('', str(item))
        dd = dd.split('\n')
        list1.append(dd[3].strip(' '))
        list1.append(dd[4].strip(' '))

    return list1

def emergingstockid():  # 取得興櫃公司id一覽
    url = 'http://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=4&issuetype=R&industry_code=&Page=1&chklike=Y'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    list = soup.select('tr')
    list1 = []
    for item in list:
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('', str(item))
        dd = dd.split('\n')
        list1.append(dd[3].strip(' '))
        list1.append(dd[4].strip(' '))

    return list1

def decideidtype(stockid, ex_ids, otc_ids, em_ids):
    if stockid in ex_ids:
        return 'ex'
    elif stockid in otc_ids:
        return 'otc'
    else:
        return 'em'

def id_full_name(stockid, ex_ids, otc_ids, em_ids):
    if stockid in ex_ids:
        return '%s%s'%(ex_ids[ex_ids.index(stockid)],ex_ids[ex_ids.index(stockid)+1])
    elif stockid in otc_ids:
        return otc_ids[otc_ids.index(stockid)]+otc_ids[otc_ids.index(stockid)+1]
    elif stockid in otc_ids:
        return em_ids[em_ids.index(stockid)]+em_ids[em_ids.index(stockid)+1]
    else:
        return ''