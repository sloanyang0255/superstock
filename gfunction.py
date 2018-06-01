__author__ = 'sloanyang'


import smtplib


exids = []
otcids = []
emids = []

def getlasttime(stime):
    ret = stime.split('/')
    if int(ret[1]) == 1:
        return ("%d/12"% (int(ret[0])-1))
    else:
        return ("%d/%02d"% (int(ret[0]), int(ret[1])-1))

def next_month(stime):
    ret = stime.split('/')
    if int(ret[1]) == 12:
        return ("%d/01"% (int(ret[0])+1))
    else:
        return ("%d/%02d"% (int(ret[0]), int(ret[1])+1))

def transferwesttochinese(stime):
    ret = stime.split('/')
    return ("%d/%d"% (int(ret[0])-1911, int(ret[1])))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


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

