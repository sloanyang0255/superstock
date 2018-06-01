__author__ = 'sloanyang'

import time
import realtime
import gfunction
import stockinfo
import techindicators
import os
from decimal import Decimal

version = '1.0.0.1'
info = []
raw_data = []
stock_status = []
notice_group = ['jmapapa@gmail.com', 'sloanyang0255@gmail.com', 'chionnian@gmail.com', 'hant883@gmail.com', 'tzuyinshen@gmail.com']
test_group = ['sloanyang0255@gmail.com']
test_group1 = ['sloanyang0255@gmail.com', 'jmapapa@gmail.com', 'chionnian@gmail.com', 'hant883@gmail.com']
black_yellow_num = 0
max_stock_num = 2000
fall_ratio = 2.00
stop_loss_ratio = 1.50
times_vol = 3.0
monitor_transaction_block = 5
before_break_back_ratio = 0.9
big_vol_price = 0.00
big_vol_times = 0.00
big_vol_time = ''
g_stock = ''
stocks = {}
# define stock status index
max_index_num = 6
index_id_name = 0
index_status = 1
index_time = 2
index_based_vol = 3
index_tick_cnt = 4


def read_test_list():
    fp = open('Document/test_list', 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    return lines


def to_dict(data):
    ret = {'stock': '', 'now':0.00, 'yesterday':0.00,
                           'start':0.00, 'high':0.00, 'low':0.00}

    ret['stock'] = data[0]
    ret['now'] = float(data[1])
    ret['yesterday'] = float(data[2])
    ret['start'] = float(data[3])
    ret['high'] = float(data[4])
    ret['low'] = float(data[5])
    return ret

def how_much_tick(source, next):
    if(source == next):
        return 0
    else:
        if(source < next):
            n1 = source
            n2 = next
            val = 1
        else:
            n2 = source
            n1 = next
            val = -1
        n1 = Decimal(str(n1))
        n2 = Decimal(str(n2))
        if(n1 < 10 and n2 <= 10):
            return (Decimal(str(n2)) - Decimal(str(n1))) / Decimal('0.01') * val
        elif(n1 < 10 and n2 > 10):
            return (10 - Decimal(str(n1))) / Decimal('0.01') + (Decimal(str(n2)) - 10) / Decimal('0.05')*val
        elif(n1 >= 10 and n1 < 50 and
            n2 > 10 and n2 <= 50):
            return (Decimal(str(n2)) - Decimal(str(n1))) / Decimal('0.05')*val
        elif(n1 >= 10 and n1 < 50 and
            n2 > 50):
            return (50 - Decimal(str(n1))) / Decimal('0.05') + (Decimal(str(n2)) - 50) / Decimal('0.1')*val
        elif(n1 >= 50 and n1 < 100 and
            n2 > 50 and n2 <= 100):
            return (Decimal(str(n2)) - Decimal(str(n1))) / Decimal('0.1')*val
        elif(n1 >= 50 and n1 < 100 and
            n2 > 100):
            return (100 - Decimal(str(n1))) / Decimal('0.1') + int((Decimal(str(n2)) - 100) / Decimal('0.5'))*val
        elif(n1 >= 100 and n1 < 500 and
            n2 > 100 and n2 <= 500):
            return (Decimal(str(n2)) - Decimal(str(n1))) / Decimal('0.5')*val
        elif(n1 >= 100 and n1 < 500 and
            n2 > 500):
            return (500 - Decimal(str(n1))) / Decimal('0.5') + (Decimal(str(n2)) - 500 / 1)*val
        elif(n1 >= 500 and n1 < 1000 and
            n2 > 500 and n2 <= 1000):
            return (Decimal(str(n2)) - Decimal(str(n1))) / 1*val
        elif(n1 >= 500 and n1 < 1000 and
            n2 > 1000):
            return (1000 - Decimal(str(n1))) / 1 + (Decimal(str(n2))- 1000) / 5*val
        elif(n1 >= 1000 and n2 > 1000):
            return (Decimal(str(n2)) - Decimal(str(n1))) / 5*val
    return 0


def is_break_high_point(stock, real_time_info, index, point_num_dict, cdp_prices):
    if(stock_status[index][index_status] == 'break-red-high-point'):
        return False
    ah = float(cdp_prices[0])
    nh = float(cdp_prices[1])
    cdp = float(cdp_prices[2])
    nl = float(cdp_prices[3])
    al = float(cdp_prices[4])
    if (real_time_info['start'] > real_time_info['yesterday'] and
     real_time_info['low'] > real_time_info['yesterday'] and
     real_time_info['low'] < real_time_info['start'] and
     real_time_info['high'] == real_time_info['start']):
        if(real_time_info['high'] < ah and real_time_info['high'] > nh and
         real_time_info['low'] < ah and real_time_info['low'] > nh):
            if((float(real_time_info['high'])-float(real_time_info['low']))/float(real_time_info['low'])
             *100 >= before_break_back_ratio):
                stock_status[index][index_status] = 'break-red-high-point'
                point_num_dict['break-red-high-point'] += 1
                return True
        if(real_time_info['high'] < nh and real_time_info['high'] > cdp and
         real_time_info['low'] < nh and real_time_info['low'] > cdp):
            if((float(real_time_info['high'])-float(real_time_info['low']))/float(real_time_info['low'])
             *100 >= before_break_back_ratio):
                stock_status[index][index_status] = 'break-red-high-point'
                point_num_dict['break-red-high-point'] += 1
                return True
        else:
            return False
    else:
        return False


def is_fall_big_vol(t_detail, num):
    global big_vol_price
    global big_vol_times
    global big_vol_time

    for i in range(0, len(t_detail)-num):
        sum = 0.00
        fall_flag = True

        for j in range(i+1, i+num+1):
            sum += float(t_detail[j][5])


            #if(how_much_tick(float(t_detail[j][3]), float(t_detail[j-1][3]))
            #  > -1):
            if(float(t_detail[j-1][3]) > float(t_detail[j][3])):
                fall_flag = False
                break
            else:
                fall_flag = True

        avg = float(sum) / float(num)

        if (float(t_detail[i][5]) > avg*times_vol and
        fall_flag == True):
            big_vol_time = t_detail[i][0]
            big_vol_price = float(t_detail[i][3])
            big_vol_times = float(t_detail[i][5]) / avg
            return True
    return False


def is_near_cdp_floor(price, cdp_price):
    ah = float(cdp_price[0])
    nh = float(cdp_price[1])
    cdp = float(cdp_price[2])
    nl = float(cdp_price[3])
    al = float(cdp_price[4])


    if(price < cdp and price > nl):
        if((cdp - price) > (price - nl)):
            return  True
    elif(price < nl and price > al):
        if((nl - price) > (price - al)):
            return  True
    elif(price == nl or price == al):
        return  True
    elif(price < al):
        return  True
    else:
        return  False
    return  False

def is_botton_rebound(stock, real_time_info, index, point_num_dict, cdp_prices):
    ah = float(cdp_prices[0])
    nh = float(cdp_prices[1])
    cdp = float(cdp_prices[2])
    nl = float(cdp_prices[3])
    al = float(cdp_prices[4])
    # type 1 - strong to strong
    if(stock_status[index][index_status] == 'cdp-big-vol-point'):
        return False
    if(real_time_info['start'] >= real_time_info['yesterday']):
        return False
    if(real_time_info['high'] >= real_time_info['yesterday']):
        return False
    if(is_near_cdp_floor(real_time_info['low'], cdp_prices) == False):
        return False
    if(((float(real_time_info['yesterday'])-float(real_time_info['low']))/float(real_time_info['low'])*100
         < fall_ratio)):
        return False

    if(real_time_info['start'] >= nl and real_time_info['start'] < cdp and
     real_time_info['low'] < cdp and
     real_time_info['now'] < cdp and
     real_time_info['now'] >= real_time_info['low']):
        t_detail = realtime.transaction_detail(stock)
        if(is_fall_big_vol(t_detail, monitor_transaction_block)):
            stock_status[index][index_status] = 'cdp-big-vol-point'
            point_num_dict['cdp-big-vol-point'] += 1
            return True
        else:
            return False
    return False

def is_rebound_fail(real_time_info, index, point_num_dict, cdp_prices):
    if(stock_status[index][index_status] == 'cdp-break-al'):
        return False
    al = float(cdp_prices[4])

    if(stock_status[index][index_status] == 'cdp-big-vol-point' and
     real_time_info['low'] < al):
        stock_status[index][index_status] = 'cdp-break-al'
        point_num_dict['cdp-break-al'] += 1
        return True
    else:
        return False


def is_cdp_to_weak(stock, real_time_info, index, point_num_dict, cdp_prices):
    ah = float(cdp_prices[0])
    nh = float(cdp_prices[1])
    cdp = float(cdp_prices[2])
    nl = float(cdp_prices[3])
    al = float(cdp_prices[4])

    if(stock_status[index][index_status] == 'cdp-weak-point'):
        return False
    if (real_time_info['start'] < ah and real_time_info['start'] > nh and
     real_time_info['now'] < nh and real_time_info['now'] > cdp and
     real_time_info['low'] > real_time_info['yesterday']):
        stock_status[index][index_status] = 'cdp-weak-point'
        point_num_dict['cdp-weak-point'] += 1
        return True
    elif (real_time_info['start'] < nh and real_time_info['start'] > cdp and
     real_time_info['now'] < cdp and real_time_info['now'] > nl and
     real_time_info['low'] > real_time_info['yesterday']):
        stock_status[index][index_status] = 'cdp-weak-point'
        point_num_dict['cdp-weak-point'] += 1
        return True
    elif (real_time_info['start'] < cdp and real_time_info['start'] > nl and
     real_time_info['now'] < al and
     real_time_info['high'] < real_time_info['yesterday']):
        stock_status[index][index_status] = 'cdp-weak-point'
        point_num_dict['cdp-weak-point'] += 1
        return True
    else:
        return False


def is_stop_loss_point(realtime_info, index, point_num, type, price, cdp):
    al = float(cdp[4])
    '''if(type == '+' and realtime_info['now'] < al):
        point_num['stop-loss'] += 1
        stock_status[index][1] = 'stop-loss'
        return True'''
    if(type == '+' and realtime_info['now'] < float(price)):
        if((float(price) - realtime_info['now'])/float(price)*100 > stop_loss_ratio):
            point_num['stop-loss'] += 1
            stock_status[index][index_status] = 'stop-loss'
            return True
    elif(type == '-' and realtime_info['now'] > float(price)):
        if((realtime_info['now'] - float(price))/float(price)*100 > stop_loss_ratio):
            point_num['stop-loss'] += 1
            stock_status[index][index_status] = 'stop-loss'
            return True
    else:
        return False


def init_stock_status(num):
    ret = []
    for i in range(0, num+1):
        stock_status.append([])
        for j in range(0, max_index_num):
            stock_status[i].append("")
    #return ret





def notice_become_red(id):
    gfunction.send_email('由黑翻紅', id, test_group1)


def notice_break_high(stock, id, cdp):
    url = 'https://tw.stock.yahoo.com/q/bc?s=***'
    url = url.replace('***', id)
    msg = '%s\n%s\n%s'%(stock, url, str(cdp))
    gfunction.send_email('開盤強勢回檔中，突破開盤價可買進', msg, test_group)

def notice_rebound_fail(id):
    gfunction.send_email('跌破AL轉空', id, test_group1)


def notice_stop_loss(id):
    gfunction.send_email('停損通知', id, test_group)

def notice_cdp_strong(stock, id, cdp):
    global big_vol_price
    global big_vol_times
    global big_vol_time
    url = 'https://tw.stock.yahoo.com/q/bc?s=***'
    url = url.replace('***', id)
    msg = '%s\n%s\n%s在%.02f塊出量%.02f倍\n%s'%(stock, url, big_vol_time,
                                           big_vol_price,
                                        big_vol_times, str(cdp))
    gfunction.send_email('下跌出量', msg, test_group)


def notice_cdp_weak(stock, id, cdp):
    url = 'https://tw.stock.yahoo.com/q/bc?s=***'
    url = url.replace('***', id)
    msg = '%s\n%s\n%s'%(stock, url, str(cdp))
    gfunction.send_email('CDP轉弱', msg, test_group)


def init_point_num(point_num):
    point_num['black-point'] = 0
    point_num['black-yellow-point'] = 0
    point_num['black-yellow-red-point'] = 0
    point_num['red-point'] = 0
    point_num['red-high-point'] = 0
    point_num['break-red-high-point'] = 0
    point_num['stop-loss'] = 0
    point_num['s2-stop-loss'] = 0
    point_num['cdp-strong-point'] = 0
    point_num['cdp-big-vol-point'] = 0
    point_num['cdp-weak-point'] = 0
    point_num['cdp-break-al'] = 0




def record_status(num):
    fp = open('Output/stock_status', "w")
    for i in range(0, num+1):
        fp.writelines(str('%s, %s'%(stock_status[i][index_id_name], stock_status[i][index_status]))+'\n')
    fp.close()


def get_rise_fall_ration(list, now):
    return (float(now)-float(list[1]))/float(list[1])*100



def main():
    global stocks

    em_ids = []
    tse_ids = stockinfo.exchangestockid()
    otc_ids = stockinfo.overthecounterstockid()


    point_num_dict = {'black-point': 0, 'black-yellow-point': 0,
                      'black-yellow-red-point': 0, 'red-point': 0,
                          'red-high-point': 0, 'break-red-high-point': 0,
                          'cdp-big-vol-point': 0, 'cdp-strong-point': 0,
                          'cdp-weak-point': 0, 'cdp-break-al': 0,
                          'stop-loss': 0, 's2-stop-loss': 0}
    while True:
        test_ids = read_test_list()
        init_stock_status(max_stock_num)
        info.clear()
        raw_data = realtime.yahoo_crawler()
        stock_num = len(raw_data)
        info.append('====================超級監控員%s===================='%(version))
        info.append('時間:%s'%(time.strftime("%H:%M:%S")))
        info.append('監控數量:%d'%(len(raw_data)))
        info.append('====================購買清單====================')
        cnt = 0
        rise_num = 0
        fall_num = 0
        for i in range(0, stock_num):
            if(gfunction.is_number(raw_data[i][1])  == False or
             gfunction.is_number(raw_data[i][2])  == False or
             gfunction.is_number(raw_data[i][3])  == False or
             gfunction.is_number(raw_data[i][4])  == False or
             gfunction.is_number(raw_data[i][5])  == False):
                continue
            data_dict = to_dict(raw_data[i])
            id_name = stockinfo.id_full_name(data_dict['stock'],
                                             tse_ids, otc_ids, em_ids)
            if(id_name != ''):
                stock_status[i][index_id_name] = id_name
            else:
                stock_status[i][index_id_name] = data_dict['stock']



            if(data_dict['now'] > data_dict['yesterday']):
                rise_num += 1
            elif(data_dict['now'] < data_dict['yesterday']):
                fall_num  += 1

            cdp_5price = techindicators.cdp(data_dict['stock'])
            if(is_botton_rebound(data_dict['stock'], data_dict, i, point_num_dict, cdp_5price)):
                notice_cdp_strong(id_name, data_dict['stock'], cdp_5price)
            #if(is_rebound_fail(data_dict, i, point_num_dict, cdp_5price)):
            #    notice_rebound_fail(id_name, data_dict['stock'], cdp_5price)

            #if(is_break_high_point(data_dict['stock'], data_dict, i, point_num_dict, cdp_5price)):
            #    notice_break_high(id_name, data_dict['stock'], cdp_5price)
           # if(is_cdp_to_weak(data_dict['stock'], data_dict, i, point_num_dict, cdp_5price)):
           #     notice_cdp_weak(id_name, data_dict['stock'], cdp_5price)


            # show test stock status
            for line in test_ids:
                list = str(line).split(',')
                if(list[0] == data_dict['stock']):
                    ration = get_rise_fall_ration(list, data_dict['now'])
                    if(list[2] == '+'):
                        info.append('(多)%s %.02f %.02f%% %.02f'%
                                    (id_name, float(data_dict['now']),
                                     ration, float(list[1])))
                    elif(list[2] == '-'):
                        info.append('(空)%s %.02f %.02f%% %.02f'%
                                    (id_name, float(data_dict['now']),
                                     ration, float(list[1])))
                    if(is_stop_loss_point(data_dict, i, point_num_dict, list[2], float(list[1]), cdp_5price)):
                        notice_stop_loss(id_name)
                    break
        info.append('====================監控狀態====================')

        info.append('上漲家數%.02f%% 下跌家數%.02f%%'%
                    (float(rise_num) / float(stock_num) * 100,
                     float(fall_num) / float(stock_num) * 100))
        info.append('s1[CDP底部出量:%d, CDP底部轉強:%d]'%
                    (point_num_dict['cdp-big-vol-point'],
                     point_num_dict['cdp-strong-point']))
        info.append('s2[CDP轉弱:%d, 跌破AL:%d]'%
                    (point_num_dict['cdp-weak-point'],
                     point_num_dict['cdp-break-al']))
        os.system('clear')



        record_status(stock_num)

        for line in info:
            print(line)



if __name__== "__main__":
    main()

'''
#if(is_break_high_point(data_dict, i, point_num_dict)):
            #    notice_break_high(id_name)
info.append('s1[由黑上升:%d, 由黑到平盤:%d, 由黑翻紅:%d, 停損:%d]'%
                    (point_num_dict['black-point'],
                     point_num_dict['black-yellow-point'],
                     point_num_dict['black-yellow-red-point'],
                     point_num_dict['s1-stop-loss']))
        info.append('s2[高點回測:%d, 回測至高點:%d, 突破高點:%d, 停損:%d]'%
                    (point_num_dict['red-point'],
                     point_num_dict['red-high-point'],
                     point_num_dict['break-red-high-point'],
                     point_num_dict['s2-stop-loss']))


 def is_botton_rebound(stock, real_time_info, index, point_num_dict, cdp_prices):
    ah = float(cdp_prices[0])
    nh = float(cdp_prices[1])
    cdp = float(cdp_prices[2])
    nl = float(cdp_prices[3])
    al = float(cdp_prices[4])
    # type 1 - strong to strong
    if(stock_status[index][1] == 'cdp-big-vol-point'):
        return False
    if(real_time_info['start'] >= real_time_info['yesterday']):
        return False
    if(real_time_info['high'] >= real_time_info['yesterday']):
        return False
    if(is_near_cdp_floor(real_time_info['low'], cdp_prices) == False):
        return False
    if(((float(real_time_info['yesterday'])-float(real_time_info['low']))/float(real_time_info['low'])*100
         < fall_ratio)):
        return False

    if(real_time_info['start'] >= nl and real_time_info['start'] < cdp and
     real_time_info['low'] < cdp and
     real_time_info['now'] < cdp and
     real_time_info['now'] >= real_time_info['low']):
        t_detail = realtime.transaction_detail(stock)
        if(is_fall_big_vol(t_detail, monitor_transaction_block)):
            stock_status[index][1] = 'cdp-big-vol-point'
            point_num_dict['cdp-big-vol-point'] += 1
            return True
        else:
            return False
    return False


    def is_fall_big_vol(t_detail, num):
    global big_vol_price
    global big_vol_times
    global big_vol_time

    for i in range(0, len(t_detail)-num):
        sum = 0.00
        fall_flag = True

        for j in range(i+1, i+num+1):
            sum += float(t_detail[j][5])


            #if(how_much_tick(float(t_detail[j][3]), float(t_detail[j-1][3]))
            #  > -1):
            if(float(t_detail[j-1][3]) > float(t_detail[j][3])):
                fall_flag = False
                break
            else:
                fall_flag = True

        avg = float(sum) / float(num)

        if (float(t_detail[i][5]) > avg*times_vol and
        fall_flag == True):
            big_vol_time = t_detail[i][0]
            big_vol_price = float(t_detail[i][3])
            big_vol_times = float(t_detail[i][5]) / avg
            return True
    return False

                     '''