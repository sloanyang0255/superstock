__author__ = 'sloanyang'

# -*- encoding: utf-8 -*-

import time
import os
import realtime
import smtplib

list1 = []
y_5price = []
last_prices = ()    #最近n檔的價格，用來判斷趨勢
last_prices_num = 5
times_vol = 5
notice_group = ['jmapapa@gmail.com', 'sloanyang0255@gmail.com', 'chionnian@gmail.com', 'hant883@gmail.com', 'tzuyinshen@gmail.com']
test_group = ['sloanyang0255@gmail.com']
test_group1 = ['sloanyang0255@gmail.com', 'jmapapa@gmail.com']
stock_status = []
fall_rise_ratio =2

def getidlist():
    fp = open('monitorid', 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    return lines

def get_5price():
    fp = open('test/y_5price', 'r')
    lines = fp.readlines()
    fp.close()
    for line in lines:
        y_5price.append(line.strip('\n'))

def send_email(subject, context, recivers):
    #寄件人的信箱，通常自己去申請個GMAIL信箱即可
    gmail_user = 'sloanyang0255@gmail.com'
    gmail_pwd = '1qaz2wsx4rfv'
    #這是GMAIL的SMTP伺服器，如果你有找到別的可以用的也可以換掉
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()


    #登入系統
    smtpserver.login(gmail_user, gmail_pwd)

    #寄件人資訊
    fromaddr = "sloanyang0255@gmail.com"
    #收件人列表，格式為list即可
    #toaddrs = ['jmapapa@gmail.com', 'sloanyang0255@gmail.com', 'chionnian@gmail.com', 'hant883@gmail.com', 'tzuyinshen@gmail.com']

    #toaddrs = ['sloanyang0255@gmail.com']


    #設定寄件資訊



    msg = "Subject : %s\n%s"%(subject, context)
    msg=msg.encode('utf-8')


    smtpserver.sendmail(fromaddr, recivers, msg)

    #記得要登出
    smtpserver.quit()




def send_remind(id):
    #你要寫的內容
    info = ''
    info += ('\n'+'您好，這是「*****」發出的例行預警通知信，請勿回信'+'\n')
    info += ('\n'+'因資訊安全，請至(http://******.nchu-cm.com/)， 登入後觀看預警內容'+'\n')

    #寄件人的信箱，通常自己去申請個GMAIL信箱即可
    gmail_user = 'sloanyang0255@gmail.com'
    gmail_pwd = '1qaz2wsx4rfv'
    #這是GMAIL的SMTP伺服器，如果你有找到別的可以用的也可以換掉
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()


    #登入系統
    smtpserver.login(gmail_user, gmail_pwd)

    #寄件人資訊
    fromaddr = "sloanyang0255@gmail.com"
    #收件人列表，格式為list即可
    #toaddrs = ['jmapapa@gmail.com', 'sloanyang0255@gmail.com', 'chionnian@gmail.com', 'hant883@gmail.com', 'tzuyinshen@gmail.com']

    toaddrs = ['sloanyang0255@gmail.com']


    #設定寄件資訊



    msg = "Subject : 注意標的\n" + id + '假跌破反彈'
    msg=msg.encode('utf-8')


    smtpserver.sendmail(fromaddr, toaddrs, msg)

    #記得要登出
    smtpserver.quit()


def init_last_prices(ids):
    ret = []
    for i in range(len(ids)):
        ret.append([])
        for j in range(0, last_prices_num):
            ret[i].append(0.00)
    return ret


def get_all_dict(list):
    ret = {'stock': '', 'start': 0.00, 'yesterday': 0.00, 'now': 0.00,
           'high': 0.00, 'low': 0.00 }
    #if(list[7] == '-'):
     #   return
    ret['stock'] = list[0]
    #print(list[7])
    if(list[7] == '-'):
        ret['start'] = 0.00
        ret['now'] = 0.00
        ret['high'] = 0.00
        ret['low'] = 0.00
    else:
        ret['start'] = float(list[7])
        ret['now'] = float(list[2])
        ret['high'] = float(list[8])
        ret['low'] = float(list[9])
    ret['yesterday'] = float(list[6])

    return ret

def is_fall_big_vol(id, list, num, d_prices, index):
    for i in range(0, len(list)-num):
        sum = 0.00
        if (list[i][0] == stock_status[index][0] and
            stock_status[index][1] == 'fall_big-vol'):
            continue

        if (float(list[i][3]) >= d_prices['yesterday']):
            continue

        for j in range(i+1, i+num+1):
            sum += float(list[j][5])
        avg = float(sum) / float(num)

        if (float(list[i][5]) > avg*times_vol and
        list[i][3] < list[i+num][3]):
            stock_status[index][0] = list[i][0]
            stock_status[index][1] = 'fall_big-vol'
            return True
    return False

def is_break_high_point(id, _realtime_info, _transaction_detail, index):
    if(_realtime_info['now'] > _realtime_info['yesterday'] and
     _realtime_info['now'] < _realtime_info['high'] and
     _realtime_info['low'] > _realtime_info['yesterday']):
        stock_status[index][1] = 'before-red-high-point'
        stock_status[index][2] = str(_realtime_info['high'])

    if(stock_status[index][1] == 'before-red-high-point' and
     _realtime_info['now'] > float(stock_status[index][2])):
        stock_status[index][1] = 'break-red-high-point'
        return True

    if(stock_status[index][1] == 'before-red-high-point' and
     _realtime_info['now'] < _realtime_info['yesterday']):
        stock_status[index][1] = ''

    return False


def is_become_red_point(id, _realtime_info, _transaction_detail, index):
    if(_realtime_info['low'] < _realtime_info['yesterday'] and
     _realtime_info['now'] > _realtime_info['low'] and
     _realtime_info['low'] < _realtime_info['yesterday'] and
     _realtime_info['now'] < _realtime_info['yesterday']):
        stock_status[index][1] = 'before-become-red-point'

    if(stock_status[index][1] == 'before-become-red-point' and
     _realtime_info['now'] > _realtime_info['yesterday']):
        fall_dis = _realtime_info['low'] - _realtime_info['yesterday']
        raise_dis = _realtime_info['high'] - _realtime_info['yesterday']
        if(fall_dis > fall_rise_ratio*raise_dis):
            stock_status[index][1] = 'become-red-point'
            return True
    return False


def is_stop_loss_point(_realtime_info):
    if(_realtime_info['now'] < _realtime_info['yesterday']):
        return True
    else:
        return False


'''
def is_become_red(id, _realtime_info, _transaction_detail, index):
    for i in range(0, len(_transaction_detail)-last_prices_num):
        if (_transaction_detail[i][0] == stock_status[index][0] and
         stock_status[index][1] == 'become-red'):
            continue

        if(stock_status[index][1] == 'fall-equal-price'
        and _realtime_info['now'] > _realtime_info['yesterday']):
            stock_status[index][0] = _transaction_detail[i][0]
            stock_status[index][1] = 'become-red'
            return True

        if(_transaction_detail[i][3] > _transaction_detail[i+last_prices_num][3] and
         _realtime_info['now'] == _realtime_info['yesterday']):
            stock_status[index][0] = _transaction_detail[i][0]
            stock_status[index][1] = 'fall-equal-price'

        return False

    if(high > realtime_info['yesterday']):
        return False
    if(low > realtime_info['yesterday']):
        return False
    if(now == realtime_info['yesterday']):
        return True
    else:
        return False'''


def notice_vol(id):
    send_email('下跌出量提醒', id, test_group)

def notice_become_red(id):
    send_email('由黑翻紅', id, test_group1)

def notice_break_high(id):
    send_email('突破高點', id, test_group)

def notice_stop_loss(id):
    send_email('停損通知', id, test_group1)

def init_stock_status(ids):
    ret = []
    for i in range(len(ids)):
        stock_status.append([])
        for j in range(0, 3):
            stock_status[i].append("")
    return stock_status
            #stock_status[i][j] = '1'


def main():
    info = []
    ids = getidlist()   # 讀取id檔案
    stock_status = init_stock_status(ids)
    #last_prices = init_last_prices(ids)
    # 開始監控個股資訊
    while True:
        info.clear()
        info.append(time.strftime("%H:%M:%S"))
        #market_info = realtime.market()
        #info.append('[台指期] %s %s %s'%(market_info[0], market_info[1], market_info[2]))
        info.append('個股   成交  漲跌')
        index = 0
        for id in ids:
            list2 = realtime.info(id)

            price_dict = get_all_dict(list2)
            if(price_dict['start'] == 0.00):
                continue
            pricerange = (price_dict['now']-price_dict['yesterday'])\
                         /price_dict['yesterday']*100
            str1 = ('%.2f'%pricerange)

            t_detail = realtime.transaction_detail(id)

            if(is_become_red_point(id, price_dict, t_detail, index)):
                notice_become_red(price_dict['stock'])
            if(is_break_high_point(id, price_dict, t_detail, index)):
                notice_break_high(price_dict['stock'])

            if(stock_status[index][1] == 'become-red-point' or
             stock_status[index][1] == 'break-red-high-point'):
                if(is_stop_loss_point(price_dict)):
                    stock_status[index][1] = 'stop-loss-point'
                    notice_stop_loss(price_dict['stock'])

            info.append('%s %.02f %s%% %s'
                  %
                  (list2[0], price_dict['now'], str1, stock_status[index][1]))
            time.sleep(0.5)
            index += 1
        os.system('clear')
        for item in info:
            print(item)
        time.sleep(1)





if __name__== "__main__":
    main()