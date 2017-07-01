import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import Encoders

def mail_android_send():
    server = 'smtp.gmail.com' # If not Gmail, this module may have to be written. This module uses SMTP protocol to send mail.
    smtpUser = 'sender@gmail.com' # To be configured such that we know it is coming from the Raspberry Pi. Perhaps create a notification ID.
    smtpPass = 'senderpass'

    toAdd = 'receiver@gmail.com' # User's email ID, so that email can be checked on the smartphone.
    fromAdd = smtpUser

    subject = 'Here is your picture!'
    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
    body = 'Dear User, please find attached the picture you just requested from your Android application. We hope there is nothing to worry about!'
    # This explicit launch method which sends a picture attached.

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromAdd
    msg['To'] = toAdd
 
    print header + '\n' + body
    s = smtplib.SMTP_SSL(server)

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("captured-image.jpg","rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename="captured-image.jpg")

    msg.attach(part)

    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, toAdd, msg.as_string())

    s.quit()
