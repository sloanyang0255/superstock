__author__ = 'sloanyang'

import techindicators
import history
import getwarrants
import time
import stockinfo
import realtime
import download

def testwarrants():
    history.emhistory('1563', '2018/02')







def main():
    #ret = realtime.yahoo_crawler()
    download.today_all_price()
    #ids = stockinfo.exchangestockid()
    #ids = stockinfo.overthecounterstockid()
    #print(ret)
    #print(techindicators.cdp('8027'))

if __name__== "__main__":
    main()