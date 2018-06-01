__author__ = 'sloanyang'

import os
import time
import techindicators
import gfunction

profit = 1.25
test_group1 = ['sloanyang0255@gmail.com', 'jmapapa@gmail.com', 'chionnian@gmail.com', 'hant883@gmail.com']
test_group = ['sloanyang0255@gmail.com']

def read_test_list():
    fp = open('Document/test_list', 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    return lines


def delete_stock(stock):
    fp = open('Document/test_list', 'r')
    lines = fp.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    fp.close()



    for i in range(0, len(lines)):
        if stock in lines[i]:
            del lines[i]
            break

    fp = open('Document/test_list', 'w')
    for i in range(0, len(lines)):
        fp.writelines(lines[i] + '\n')
    fp.close()





def add_stock(list, stock, price, direction):
    if(direction == '1'):
        st1 = '%s,%s,+\n'%(stock,price)
    elif(direction == '2'):
        st1 = '%s,%s,-\n'%(stock,price)
    fp = open('Document/test_list', 'a')
    fp.writelines(st1)
    fp.close()

def record_profit(stock, sell_price, direction):
    buy_price = 0.00
    fp = open('Document/test_list', 'r')
    lines = fp.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    fp.close()
    for line in lines:
        if(stock in line):
            list = line.split(',')
            buy_price = float(list[1])
            break
    profit = 0.00
    ration = (float(sell_price)-buy_price)/buy_price*100
    if (direction == '+' and ration > 0):
       profit = ration
    elif (direction == '+' and ration < 0):
        profit = ration
    elif (direction == '-' and ration > 0):
       profit = 0 - ration
    elif (direction == '-' and ration < 0):
        profit = abs(ration)

    path = ('Document/porfit_%s')%(time.strftime("%Y%m"))
    fp = open(path, 'a+')
    fp.writelines('%s,%.02f\n'%(stock, profit))
    fp.close()




def main():
    while True:
        list = read_test_list()
        print('模擬交易系統')
        direction = input("(1)多(2)空(3)CDP:")
        if(direction == '3'):
            stock = input("輸入股票:")
            cdp_5price = techindicators.cdp(stock)
            ah = float(cdp_5price[0])
            nh = float(cdp_5price[1])
            cdp = float(cdp_5price[2])
            nl = float(cdp_5price[3])
            al = float(cdp_5price[4])
            print('-----------ah %.02f------------'%(ah))
            print('-----------nh %.02f------------'%(nh))
            print('-----------cdp %.02f------------'%(cdp))
            print('-----------nl %.02f------------'%(nl))
            print('-----------al %.02f------------'%(al))


        elif(direction == '1' or direction == '2'):
            type = input("(1)買(2)賣:")
            stock = input("輸入股票:")
            if(type == '1'):
                price = input("輸入交易價位:")
                add_stock(list, stock, price, direction)
                if(direction == '1'):
                    profit_price = float(price)*(1 + profit/100)
                    title = '買入%s於%s塊，建議%.02f塊賣出'%(stock, price, float(profit_price))
                elif(direction == '2'):
                    profit_price = float(price)*(1 - profit/100)
                    title = '放空%s於%s塊，建議%.02f塊回補'%(stock, price, float(profit_price))

                gfunction.send_email(title, '', test_group1)
                print('建議賣價=%.02f'%(profit_price))
            elif(type == '2'):
                #record_profit(stock, price, direction)
                delete_stock(stock)


        print('交易成功')
        time.sleep(2)
        #os.system('clear')


if __name__ == "__main__":
    main()