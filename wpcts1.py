__author__ = 'sloanyang'

import time
import pygal
import history
import stockinfo
import gfunction
import os
import sys

expect_profit = 2.5
max_day = 7

def getidlist(file_name):
    fp = open(file_name, 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n
    return lines


def trace_day_profit(stock_id, b_time, b_price, ex_ids, otc_ids, em_ids):
    profits = []
    b_day_index = -1
    data = history.history_data(stock_id, b_time,
                                         stockinfo.decideidtype(stock_id, ex_ids, otc_ids, em_ids))
    # 找出起始天數的index
    for i in range(len(data)):
        if data[i][0][-5:] == b_time[-5:]:
            b_day_index = i
            break
    if b_day_index == -1:
        return []
    # 逐天取出profit
    for j in range(max_day):
        if b_day_index+j+1 < len(data):
            profits.append((float(data[b_day_index+j+1][4])-float(b_price))/float(b_price)*100)
        elif b_time[5:7] != time.strftime("%m"):  # 繼續從下個月找
            data1 = history.history_data(stock_id, gfunction.next_month(b_time),
                                         stockinfo.decideidtype(stock_id, ex_ids, otc_ids, em_ids))
            for k in range(max_day-j):
                if k < len(data1):
                    profits.append((float(data1[k][4])-float(b_price))/float(b_price)*100)
                else:
                    break
            break
    return profits

def output_file(stock_name, data):
    for i in range(len(data)):
        file_name = 'Output/day%02d'%(i+1)
        fp = open(file_name, 'a')
        fp.writelines('%s,%.02f\n'%(stock_name, data[i]))
        fp.close()

def count_profit(profits, s_total, p_total, e_total, win):
    if profits != []:
        st1 = '最大漲幅%.02f%%'%(sorted(profits)[-1])
        print(st1, end='')
    b_win = win
    for i in range(len(profits)):
        s_total[i] += 1
        if profits[i] >= expect_profit:
            p_total[i] += 1
        if profits[i] >= 0:
            e_total[i] += 1
    for i in range(len(profits)):
        if profits[i] >= expect_profit:
            win += 1
            print('(Pass)')
            break
    if b_win == win and len(profits) < max_day:
        print(' (Continue)')
    elif b_win == win and len(profits) == max_day:
        print(' (Fail)')
    return win

def get_wpct(s_total, p_total):
    wpcts = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    for i in range(len(wpcts)):
        if s_total[i] != 0:
            wpcts[i] = p_total[i]/s_total[i]*100
    return wpcts

def get_epct(s_total, e_total):
    epcts = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    for i in range(len(epcts)):
        if s_total[i] != 0:
            epcts[i] = e_total[i]/s_total[i]*100
    return epcts

def output_screen(s_total, p_total, wpcts, epcts, transaction, win):
    print('設定獲利 = %.02f%%'%(expect_profit))

    print('----------勝率----------')
    print('共交易%d筆成功%d筆'%(transaction, win))
    print('勝率 ＝%.02f%%'%(float(win)/float(transaction)*100))

    print('----------獲利率----------')
    for i in range(len(wpcts)):
        print('第%d天%d筆 ＝%.02f%%'%(i+1, s_total[i], wpcts[i]))

    print('----------保本率----------')
    for i in range(len(wpcts)):
        print('第%d天%d筆 ＝%.02f%%'%(i+1, s_total[i], epcts[i]))


def main():
    os.system('clear')
    sample_total = [0, 0, 0, 0, 0, 0, 0]
    profit_total = [0, 0, 0, 0, 0, 0, 0]
    equal_total = [0, 0, 0, 0, 0, 0, 0]
    transaction = 0
    win = 0
    exids = stockinfo.exchangestockid()     # 上市id一覽
    otcids = stockinfo.overthecounterstockid()      # 上櫃id一覽
    emids = stockinfo.emergingstockid()        # 興櫃id一覽
    # 刪除上一次輸出結果
    for i in range(max_day):
        file_name = 'Output/day%02d'%(i+1)
        if os.path.exists(file_name):
            os.remove(file_name)
    for line in getidlist(sys.argv[1]):     # 讀取id檔案 ex.6226,2018/02/09,8.99,抄抵多
        transaction += 1
        line = line.split(',')

        print(stockinfo.id_full_name(line[0], exids, otcids, emids)
              + ',' + line[1]
        + ',' + line[3])
        profits = trace_day_profit(line[0], line[1], line[2], exids, otcids, emids)
        win = count_profit(profits, sample_total, profit_total, equal_total, win)
        output_file(line[0], profits)
        time.sleep(0.5)
    wpcts = get_wpct(sample_total, profit_total)
    epcts = get_epct(sample_total, equal_total)
    output_screen(sample_total, profit_total, wpcts, epcts, transaction, win)





if __name__== "__main__":
    main()