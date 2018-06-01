__author__ = 'sloanyang'

import requests
from bs4 import BeautifulSoup
import re
import time
import urllib3
import urllib

def info(stockid):
    html = 'https://tw.stock.yahoo.com/q/q?s=***'
    html = html.replace('***', stockid)
    res = requests.post(html)
    time.sleep(0.01)
    requests.post(html, headers={'Connection':'close'})
    soup = BeautifulSoup(res.text, "html.parser")
    tap = '/q/bc?s=***'
    tap = tap.replace('***', stockid)
    idname = soup.find_all('a', href=tap)
    list = soup.find_all('td', align="center", bgcolor="#FFFfff", nowrap="")

    list1 = [idname, list[0], list[1], list[2], list[3], list[5], list[6],list[7]
             , list[8], list[9]]
    list2 = []
    for item in list1:
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('',str(item))
        list2.append(dd)
    return list2

def riserankids():
    ret = []
    res = requests.get("https://tw.stock.yahoo.com/d/i/rank.php?t=down&e=tse")
    requests.get("https://tw.stock.yahoo.com/d/i/rank.php?t=down&e=tse", headers={'Connection':'close'})
    time.sleep(0.01)
    soup = BeautifulSoup(res.text, "html.parser")
    list = soup.select('.name')
    for item in list:
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('',str(item))
        ret.append(dd)
    return ret

def market():
    url = 'https://www.wantgoo.com/option/futures/quotes?StockNo=WTX%26'
    res = requests.get(url)
    requests.get(url, headers={'Connection':'close'})
    time.sleep(0.01)
    soup = BeautifulSoup(res.text, "html.parser")
    list = soup.find_all('div', attrs={'class':'i idx-change up'}) # dn up
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',str(list))
    list = dd.split('\n')

    #print(list)
    value = list[3].replace('%', '')
    return list[1], list[3], int(float(value)/100*float(list[1]))


def transaction_detail(id):
    ret = []
    url = 'https://tw.stock.yahoo.com/q/ts?s=***&t=50'
    #url = 'https://tw.stock.yahoo.com/q/ts?s=***'
    url = url.replace('***', id)
    res = requests.get(url)
    #requests.get(url, headers={'Connection':'close'})
    time.sleep(0.5)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.find_all('tr', align="center", bgcolor="#ffffff", height="25")

    for i in range(len(text)):
        ret.append([])
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub(',',str(text[i]))
        dc = dd.split(',')
        df = ''
        for d in dc:
            if(d != ''):
                ret[i].append(d)
    return ret

def yahoo_all_stock():
    url = 'https://tw.stock.yahoo.com/s/list.php?c={type}&pid={page}'
    for i in range(1, 10):
        url = url.replace('{type}', 'otc')

        url = url.replace('{page}', str(2))
        print(url)
        res = requests.get(url)
        requests.get(url, headers={'Connection':'close'})
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.find_all('tr', align="center", bgcolor="#FFFfff")
        print(text)
        time.sleep(3)

def get_price(string, pos):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub(',',string)
    dd = dd.split(',')
    return dd[pos]

# stock, now, yesterday, start, high, low
def yahoo_crawler():
    stock_info = []
    listed_url = "https://tw.stock.yahoo.com/s/list.php?c=tse&pid={page}"
    otc_url = "https://tw.stock.yahoo.com/s/list.php?c=otc&pid={page}"
    stock_index = 0
    for i in range(1, 10):
        crt_url = listed_url.format(page = i)
        #print (crt_url)
        response = urllib.request.urlopen(crt_url)
        lines = response.readlines()
        name_4_cnt = 0
        j = -1
        while j < len(lines) - 1:
            j += 1
            line = lines[j].strip()
            iline = str(line)
            if ("<td align=center bgcolor=#FFFfff nowrap>" in iline):
                stock_id = re.findall(u"href=/q/q_(.*?)\.html", iline)[0]
                if(len(stock_id) == 4):
                    #print(stock_id + '******')
                    stock_info.append([])
                    '''dic = {'stock':'', 'now':'', 'yesterday':'',
                           'start':'', 'high':'', 'low':''}
                    dic['stock'] = stock_id
                    dic['now'] = get_price(str(lines[j+3]),2)
                    dic['yesterday'] = get_price(str(lines[j+8]),1)
                    dic['start'] = get_price(str(lines[j+9]),1)
                    dic['high'] = get_price(str(lines[j+10]),1)
                    dic['low'] = get_price(str(lines[j+11]),1)
                    stock_info[stock_index].append(dic)'''
                    stock_info[stock_index].append(stock_id)
                    stock_info[stock_index].append(get_price(str(lines[j+3]),2))
                    stock_info[stock_index].append(get_price(str(lines[j+8]),1))
                    stock_info[stock_index].append(get_price(str(lines[j+9]),1))
                    stock_info[stock_index].append(get_price(str(lines[j+10]),1))
                    stock_info[stock_index].append(get_price(str(lines[j+11]),1))
                    stock_index += 1
                    name_4_cnt += 1
                    j += 3
        if(name_4_cnt == 0):
            break
    otc_url = "https://tw.stock.yahoo.com/s/list.php?c=otc&pid={page}"
    for i in range(1, 2):
        crt_url = otc_url.format(page = i)
        #print (crt_url)
        response = urllib.request.urlopen(crt_url)
        lines = response.readlines()
        name_4_cnt = 0
        j = -1
        while j < len(lines) - 1:
            j += 1
            line = lines[j].strip()
            iline = str(line)
            if ("<td align=center bgcolor=#FFFfff nowrap>" in iline):
                stock_id = re.findall(u"href=/q/q_(.*?)\.html", iline)[0]
                if(len(stock_id) == 4):
                    #print(stock_id + '******')
                    stock_info.append([])
                    '''dic = {'stock':'', 'now':'', 'yesterday':'',
                           'start':'', 'high':'', 'low':''}
                    dic['stock'] = stock_id
                    dic['now'] = get_price(str(lines[j+3]),2)
                    dic['yesterday'] = get_price(str(lines[j+8]),1)
                    dic['start'] = get_price(str(lines[j+9]),1)
                    dic['high'] = get_price(str(lines[j+10]),1)
                    dic['low'] = get_price(str(lines[j+11]),1)
                    stock_info[stock_index].append(dic)'''
                    stock_info[stock_index].append(stock_id)
                    stock_info[stock_index].append(get_price(str(lines[j+3]),2))
                    stock_info[stock_index].append(get_price(str(lines[j+8]),1))
                    stock_info[stock_index].append(get_price(str(lines[j+9]),1))
                    stock_info[stock_index].append(get_price(str(lines[j+10]),1))
                    stock_info[stock_index].append(get_price(str(lines[j+11]),1))
                    #print(stock_info[stock_index])
                    stock_index += 1
                    name_4_cnt += 1
                    j += 3
        if(name_4_cnt == 0):
            break
    return stock_info


'''price = float(re.findall(u"<b>(.*?)<", iline)[0])
if (len(stock_id)) == 4:
    if (stock_id) not in stock_info.keys():
        _have_id = True
        stock_info[stock_id] = price'''



