__author__ = 'sloanyang'

# -*- encoding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys

def send_mesg():
    fp = open('Document/buy_menu', 'r')
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')     # 去掉\n

    #你要寫的內容
    info = ''
    info += ('\n'+'您好，這是「*****」發出的例行預警通知信，請勿回信'+'\n')
    info += ('\n'+'因資訊安全，請至(http://******.nchu-cm.com/)， 登入後觀看預警內容'+'\n')

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
    toaddrs = ['jmapapa@gmail.com', 'sloanyang0255@gmail.com', 'chionnian@gmail.com', 'hant883@gmail.com', 'tzuyinshen@gmail.com']
#nycusher731@gmail.com
    #toaddrs = ['sloanyang0255@gmail.com']
  #  message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
  #  message['From'] = Header("菜鸟教程", 'utf-8')
  #  message['To'] =  Header("测试", 'utf-8')

   # subject = 'Python SMTP 邮件测试'
   # message['Subject'] = Header(subject, 'utf-8')

    #設定寄件資訊

    for i in range(len(lines)):
        lines[i]+='\n'
        #lines[i]=lines[i].encode('utf-8')
    #    msg = ''.join(lines)
    #    msg += '\n'
    Subject = 'testing'
    msg = "Subject : 推薦標的\n" + ''.join(lines)
    msg=msg.encode('utf-8')


    smtpserver.sendmail(fromaddr, toaddrs, msg)

    #記得要登出
    smtpserver.quit()

def main():
    send_mesg()

if __name__== "__main__":
    main()