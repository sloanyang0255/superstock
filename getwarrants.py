__author__ = 'sloanyang'

# -*- coding: utf-8 -*-
import csv
import requests
import time
import re

def searchinsnbr(id):
    url = 'https://warrant.kgi.com/EDWebService/WSInterfaceSwap.asmx/GetService'
    payload = {'Menukey':'S0600017_GetUnderlyingList',
        'ParametersOfJson':'{"LocationPathName":"/EDWebSite/Views/WarrantSearch/WarrantSearch.aspx"}'
    }
    res = requests.post(url, data=payload)
    str1 = res.text[res.text.find('[')+1: res.text.find(']')]
    start = 0
    pos = 0
    tmp_dic = {}
    while pos < len(str1):
        pos = str1.find('}', start, len(str1))
        if pos == -1 or pos+1 > len(str1):
            break
        tmp_dic = eval(str1[start : pos+1])
        if(tmp_dic['INSTR_STKID_NAME'].find(id) != -1):
            return tmp_dic['INSTR_INSNBR']
        start = pos + 2


def getwarrantslist(id, type):
    url = 'https://warrant.kgi.com/EDWebService/WSInterfaceSwap.asmx/GetService'
    payload = {
        'Menukey':'S0600013_GetWarrants',
        'ParametersOfJson':'{"NORMAL_OR_CATTLE_BEAR":0,"INSWRT_ISSUER_NAME":"ALL",'
                           '"STRIKE_FROM":-1,"STRIKE_TO":-1,"VOLUME":-1,'
                           '"UND_INSTR_INSNBR":"SNBR***","LAST_DAYS_FROM":"-1",'
                           '"LAST_DAYS_TO":"-1","IMP_VOL":-1,"CP":"CP***",'
                           '"IN_OUT_PERCENT_FROM":"-1","IN_OUT_PERCENT_TO":"-1",'
                           '"BID_ASK_SPREAD_PERCENT":"-1","LEVERAGE":"-1",'
                           '"EXECRATE":"-1","OUTSTANDING_PERCENT":"-1",'
                           '"BARRIER_DEAL_PERCENT":-1,'
                           '"LocationPathName":"/EDWebSite/Views/WarrantSearch/WarrantSearch.aspx"}'
    }
    s1 = payload['ParametersOfJson']
    s1 = s1.replace('SNBR***', str(searchinsnbr(id)))
    if type == 'b':
        payload['ParametersOfJson'] = s1.replace('CP***', '認購')
    elif type == 's':
        payload['ParametersOfJson'] = s1.replace('CP***', '認售')
    res = requests.post(url, data=payload)
    str1 = res.text[res.text.find('[')+1: res.text.find(']')]
    start = 0
    pos = 0
    ret_list = []
    tmp_dic = {}
    while pos < len(str1):
        pos = str1.find('}', start, len(str1))
        if pos == -1 or pos+1 > len(str1):
            break
        tmp_dic = eval(str1[start : pos+1])
        ret_list.append(tmp_dic)
        start = pos + 2
    return ret_list


def checkcondition(condition, compare, val):
    detail = []
    if compare.find('more') != -1:
        detail.append('more')
        detail.append(float(compare.replace('more', '')))
    elif compare.find('less') != -1:
        detail.append('less')
        detail.append(float(compare.replace('less', '')))
    elif compare.find('between') != -1:
        detail.append('between')
        d1 = compare.find('and')
        detail.append(float(compare[7:d1]))
        detail.append(float(compare[d1+3:]))

    if detail[0] == 'more'\
        and detail[1] < float(val) :
        return True
    elif detail[0] == 'less'\
        and detail[1] > float(val) :
        return True
    elif detail[0] == 'between'\
        and (detail[1] < float(val) and detail[2] > float(val)):
        return True
    return False




    return True

def getgoodwarrants(stockid, type, part, lev, vol, day, swrt, inout):
    ret = []
    warrantslist = []
    warrantslist = getwarrantslist(stockid, type)

    for item in warrantslist:
        if part == 'all':
            ret.append(("['代號:%s','名稱:%s','槓桿:%s','成交量:%s','剩餘天數:%s'"
                        ",'行使比例:%s', '價內外:%s']"
                  % (str(item['INSTR_STKID'])
                     , str(item['INSTR_NAME'])
                     , str(item['LEVERAGE'])
                     , str(item['VOLUME'])
                     , str(item['LAST_DAYS'])
                     , str(item['INSWRT_EXECRATE'])
                     , str(item['IN_OUT_PERCENT']))))
        elif part == 'part':
            if checkcondition('LEVERAGE', lev, item['LEVERAGE'])\
               and checkcondition('VOLUME', vol, item['VOLUME'])\
                and checkcondition('LAST_DAYS', day, item['LAST_DAYS'])\
                and checkcondition('INSWRT_EXECRATE', swrt, item['INSWRT_EXECRATE'])\
                    and checkcondition('IN_OUT_PERCENT', inout, item['IN_OUT_PERCENT']):
                ret.append(("['代號:%s','名稱:%s','槓桿:%s','成交量:%s','剩餘天數:%s'"
                        ",'行使比例:%s', '價內外:%s']"
                  % (str(item['INSTR_STKID'])
                     , str(item['INSTR_NAME'])
                     , str(item['LEVERAGE'])
                     , str(item['VOLUME'])
                     , str(item['LAST_DAYS'])
                     , str(item['INSWRT_EXECRATE'])
                     , str(item['IN_OUT_PERCENT']))))
    return ret

def good_warrants(stockid, type, part):
    day = 'more50'
    inout = 'between-10and5'

    ret = []
    g1 = []
    g2 = []
    others = []
    warrantslist = []
    warrantslist = getwarrantslist(stockid, type)

    for item in warrantslist:
        if part == 'all':
            ret.append(("['代號:%s','名稱:%s','槓桿:%s','成交量:%s','剩餘天數:%s'"
                        ",'行使比例:%s', '價內外:%s']"
                  % (str(item['INSTR_STKID'])
                     , str(item['INSTR_NAME'])
                     , str(item['LEVERAGE'])
                     , str(item['VOLUME'])
                     , str(item['LAST_DAYS'])
                     , str(item['INSWRT_EXECRATE'])
                     , str(item['IN_OUT_PERCENT']))))
        elif part == 'part':
            if checkcondition('LAST_DAYS', day, item['LAST_DAYS'])\
                    and checkcondition('IN_OUT_PERCENT', inout, item['IN_OUT_PERCENT']):
                if item['INSTR_NAME'].find('元大') != -1:
                    g1.append(("['代號:%s','名稱:%s','槓桿:%s','成交量:%s','剩餘天數:%s'"
                        ",'行使比例:%s', '價內外:%s']"
                  % (str(item['INSTR_STKID'])
                     , str(item['INSTR_NAME'])
                     , str(item['LEVERAGE'])
                     , str(item['VOLUME'])
                     , str(item['LAST_DAYS'])
                     , str(item['INSWRT_EXECRATE'])
                     , str(item['IN_OUT_PERCENT']))))
                elif item['INSTR_NAME'].find('凱基') != -1:
                    g2.append(("['代號:%s','名稱:%s','槓桿:%s','成交量:%s','剩餘天數:%s'"
                            ",'行使比例:%s', '價內外:%s']"
                      % (str(item['INSTR_STKID'])
                         , str(item['INSTR_NAME'])
                         , str(item['LEVERAGE'])
                         , str(item['VOLUME'])
                         , str(item['LAST_DAYS'])
                         , str(item['INSWRT_EXECRATE'])
                         , str(item['IN_OUT_PERCENT']))))
                else:
                    others.append(("['代號:%s','名稱:%s','槓桿:%s','成交量:%s','剩餘天數:%s'"
                            ",'行使比例:%s', '價內外:%s']"
                      % (str(item['INSTR_STKID'])
                         , str(item['INSTR_NAME'])
                         , str(item['LEVERAGE'])
                         , str(item['VOLUME'])
                         , str(item['LAST_DAYS'])
                         , str(item['INSWRT_EXECRATE'])
                         , str(item['IN_OUT_PERCENT']))))

    return g1, g2, others
