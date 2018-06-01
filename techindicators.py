__author__ = 'sloanyang'

import history
import gfunction

def moving_average(id, day_index, data, type):
    res = []
    p_sum = [0.00, 0.00, 0.00, 0.00]    # 價均線[五日, 十日, 二十日, 六十日]
    v_sum = [0, 0]    # 量均線[五日, 十日]
    deal_index = 0
    if type == 'ex' or type == 'otc':
        deal_index = 6
        # print(eval(data[day_index])[6])
        #p_sum[0] = float(nowprice)
        #v_sum[0] = int(nowvolume)
        #   五日均線總和
        index = -4
        '''for i in range(index, 0):
            print(data[i][6])
            psum[0] = psum[0] + float(data[i][6])
            vsum[0] = vsum[0] + int(int(data[i][1].replace(',', ''))/1000)
        #   十日均線總和
        index = -9
        psum[1] = psum[0]
        vsum[1] = vsum[0]
        for i in range(index, -4):
            psum[1] = psum[1] + float(data[i][6])
            vsum[1] = vsum[1] + int(int(data[i][1].replace(',', ''))/1000)
        #   二十日均線總和
        index = -29
        psum[2] = psum[1]
        vsum[2] = vsum[1]
        for i in range(index, -9):
            #print(vsum[2])
            psum[2] = psum[2] + float(data[i][6])
            vsum[2] = vsum[2] + int(int(data[i][1].replace(',', ''))/1000)'''
    else:
        #   五日均線總和
        '''index = -4
        for i in range(index, 0):
            print(i)
            print(int(int(data[i][1].replace(',', ''))/1000))
            psum[0] = psum[0] + float(data[i][4])
            vsum[0] = vsum[0] + int(int(data[i][2].replace(',', ''))/1000)
        #   十日均線總和
        index = -9
        psum[1] = psum[0]
        vsum[1] = vsum[0]
        for i in range(index, -4):
            #print(vsum[1])
            psum[1] = psum[1] + float(data[i][4])
            vsum[1] = vsum[1] + int(int(data[i][2].replace(',', ''))/1000)
        #   二十日均線總和
        index = -29
        psum[2] = psum[1]
        vsum[2] = vsum[1]
        for i in range(index, -9):
            #print(vsum[2])
            psum[2] = psum[2] + float(data[i][4])
            vsum[2] = vsum[2] + int(int(data[i][2].replace(',', ''))/1000)'''
    '''res.extend(psum)
    res.extend(vsum)
    res[0] = res[0]/5'''
    avg_index = 4
    for j in range(day_index - avg_index, day_index):
        p_sum[0] = p_sum[0] + float(eval(data[j])[6])
    #print(p_sum[0])
    return res

def cdp(stock_id):  # AH, NH, CDP, NL, AL
    # read lastday file
    list1 = []
    fp = open('Output/lastday', 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    # calculate cdp 5 price
    for i in range(len(lines)):
        list1 = lines[i].split(',')
        if(list1[0] == stock_id):
            break
    # stock, now, yesterday, start, high, low
    if(gfunction.is_number(list1[1]) == False or
        gfunction.is_number(list1[4]) == False or
        gfunction.is_number(list1[5]) == False):
        return [0.00, 0.00, 0.00, 0.00, 0.00]

    now = float(list1[1])
    high = float(list1[4])
    low = float(list1[5])
    cdp = (high + low + 2*now)/4
    ah = cdp + (high - low)
    nh = 2*cdp - low
    nl = 2*cdp - high
    al = cdp - (high - low)
    return [ah, nh, cdp, nl, al]


