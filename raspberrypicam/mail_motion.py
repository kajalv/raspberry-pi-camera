import smtplib

def mail_motion_send():
    server = 'smtp.gmail.com' # If not Gmail, this module may have to be written. This module uses SMTP protocol to send mail.
    smtpUser = 'sender@gmail.com' # To be configured such that we know it is coming from the Raspberry Pi. Perhaps create a notification ID.
    smtpPass = 'senderpass'

    toAdd = 'receiver@gmail.com' # User's email ID, so that email can be checked on the smartphone.
    fromAdd = smtpUser

    subject = 'Someone is in your house!'
    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
    body = 'Alert! Motion has been detected in your house using your Raspberry Pi Home Surveillance System. Beware!'
    # Generated montage too large to send, so sending a text body.
    # Module can be changed to send just a single picture if desired.
    # Refer the explicit launch method which sends a picture.

    s = smtplib.SMTP_SSL(server)

    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

    s.quit()
