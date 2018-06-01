__author__ = 'sloanyang'

import stockinfo
import gfunction
import history
import time
import os
import datetime
import techindicators

def read_data_file(file_name):
    fp = open(file_name, 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    return lines

def download_data(from_t, to_t):
    #print('start time='+ time.strftime("%H:%M:%S"))
    a = datetime.datetime.now()
    exids = stockinfo.exchangestockid()     # 上市id一覽
    for i in range(1228, len(exids[2:])):
        if(gfunction.is_number(exids[2+i])):
            file_name = 'Output/%s_his'%(exids[2+i])
            if os.path.exists(file_name):
                os.remove(file_name)
            slide_t = from_t
            print('download %s'%(exids[2+i]))
            while True:
                print('%s ... downloading'% ( slide_t ))
                fp = open(file_name, "a")
                data = history.history_data(exids[2+i], slide_t, 'ex')
                for item in data:
                    fp.writelines(str(item)+'\n')
                fp.close()
                print('%s ... completed'% ( slide_t ))
                if(slide_t == to_t):
                    break
                slide_t = gfunction.next_month(slide_t)
                time.sleep(5)
            fp1 = open('compleled_list', "a")
            fp1.writelines(str(2+i)+ '=' + str(exids[2+i])+'\n')
            fp1.close()
    b = datetime.datetime.now()
    sec = (b-a).seconds
    min = int(sec) / 60
    sec = sec % 60
    print('total time = %d min %d sec'%(min, sec))
    #otcids = stockinfo.overthecounterstockid()      # 上櫃id一覽
    # = stockinfo.emergingstockid()        # 興櫃id一覽
    #download_data('201301', '201804')

def main():
    download_data('2018/02', '2018/05')
    print('下載完成')
    '''list = read_data_file('Output/1101_his')
    s_index = 0
    for i in range(s_index, len(list)):
        techindicators.moving_average('1101', i, list, 'ex')'''



if __name__== "__main__":
    main()
