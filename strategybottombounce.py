__author__ = 'sloanyang'

import requests
import twstock
import time
from twstock import Stock
import realtime
import gfunction
import history
import stockinfo
import techindicators


def countavgprice(data):
    data = []



def main():
    data = []
    print('start time='+ time.strftime("%H:%M:%S"))
    for item in realtime.riserankids():    #抓取漲跌排名前面的個股
        list1 = item.split(' ')
        print(item)
        techindicators.movingaverage(list1[0])
        #realtime.info(list1[0])   #抓取現在資訊
        '''nowtime = time.strftime("%Y/%m")
        lasttime = gfunction.getlasttime(nowtime)
        data.append(history.history(list1[0], lasttime))#抓取上個月歷史資訊
        data.append(history.history(list1[0], nowtime)) #抓取這個月歷史資訊
        avgprice = countavgprice(data)'''  #計算價格均線
        #計算成交量均線
        #是否符合篩選條件
        #是則推薦
        time.sleep(3)
    print('end time='+ time.strftime("%H:%M:%S"))






if __name__== "__main__":
    main()