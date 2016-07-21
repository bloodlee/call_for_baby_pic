"""
This script is for me to get the baby picture taken from home.
"""

import urllib
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import datetime
import time

MONITORING_PAGE = "http://www.innoli.com/wordpress/?p=1214"
PICTURE_LINK = "http://localhost:8080/?action=snapshot"
SEND_TO_EMAIL = 'jasonleehust@gmail.com'
PIC_LOCATION = '/tmp/a.jpg'

IDEL_TIME_SEC = 20 * 60
WORKING_WAITING_SEC = 15 * 60

WORKING_HOUR = range(9, 24)


def get_image():
    urllib.urlretrieve(PICTURE_LINK, PIC_LOCATION)


def send_email(current):
    get_image()

    msg = MIMEMultipart()
    msg['From'] = 'yongqiangli.china@gmail.com'
    msg['To'] = SEND_TO_EMAIL
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "henry's picture at {}".format(current)

    msg.attach(MIMEText('See the attachment'))

    with open(PIC_LOCATION, 'rb') as fil:
        part = MIMEApplication(fil.read(), Name='picture.jpg')
        part['Content-Disposition'] = 'attachment; filename="picture.jpg"'
        msg.attach(part)

    # smtp = smtplib.SMTP('localhost')
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('your_email', 'your_password')
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()


def main():
    while True:
        current = datetime.datetime.now()

        print "current time is {}".format(current)

        if current.hour not in WORKING_HOUR:

            print "not in work hour, wait for 20 minutes"
            time.sleep(IDEL_TIME_SEC)
            continue

        try:
            print "going to send email to Yongqiang"
            send_email(current)

            print "email has been sent. Wait for another 15 minutes"
            time.sleep(WORKING_WAITING_SEC)
        except Exception as e:
            print "got an exception {}".format(e)
            print "wait for 20 minutes"
            time.sleep(IDEL_TIME_SEC)


if __name__ == '__main__':
    main()

