__author__ = 'sloanyang'

import time
import realtime
import history
import stockinfo
import sys

profit = 2.23

def getidlist(file_name):
    fp = open('traceid', 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    return lines

def countmaxprofit(method, info, buyday, buyprice):
    index = -1
    v1 = []
    if method.find('多') != -1:  # 多方策略，找最大值
        while(info[index][0] != buyday):
            v1.append(info[index][4])
            index = index - 1
        if v1 != []:
            maxprice = max(v1)
        else:
            return 0
    elif method.find('空') != -1:    # 空方策略，找最小值
        while(info[index][0] != buyday):
            index = index - 1
        if v1 != []:
            maxprice = min(v1)
        else:
            return 0
    return (float(maxprice)-float(buyprice))/float(buyprice)*100



def main():
    ids = getidlist(sys.argv[1])   # 讀取id檔案
    '''for content in idscontent:
        content = content.split(',')
        info = history.thismonthinfo(content[0], stockinfo.decideidtype(content[0]))
        maxprofit = countmaxprofit(content[3], info, content[1], content[2])
        m = '%.2f'%(maxprofit)
        if float(m) >= float(profit):   #滿足設定利潤
            text = '%s:%s,在%s以%s買進,最大幅度%s%%,%s'\
                   %(content
                    ,content[3]
                    ,content[1]
                    ,content[2]
                    ,str(m)
                    ,'滿足')
        else:
            text = '%s:%s,在%s以%s買進,最大幅度%s%%,%s'\
                   %(content
                    ,content[3]
                    ,content[1]
                    ,content[2]
                    ,str(m)
                    ,'未滿足')
        print(text)
        time.sleep(0.5)
    '''



if __name__== "__main__":
    main()