__author__ = 'sloanyang'


def is_fall_big_vol(t_detail, num):
    global big_vol_price
    global big_vol_times
    global big_vol_time

    for i in range(0, len(t_detail)-num):
        sum = 0.00
        fall_flag = True

        for j in range(i+1, i+num+1):
            sum += float(t_detail[j][5])
            tick = how_much_tick(float(t_detail[j][3]), float(t_detail[j-1][3]))
            print('n1=%f' %(float(t_detail[j][3])))
            print('n2=%f' %(float(t_detail[j-1][3])))
            print('tick=%d' %(tick))
            if(how_much_tick(float(t_detail[j][3]), float(t_detail[j-1][3]))
              > -1):
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