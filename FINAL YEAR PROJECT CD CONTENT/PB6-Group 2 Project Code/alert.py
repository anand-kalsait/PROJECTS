from fileinput import filename
import smtplib
import imghdr
import time
from email.message import EmailMessage
def emailalert():
    curtime = time.ctime()
    NM = EmailMessage()
    
    sender_email = "anand1124134@gmail.com"
    rec_email = "alex99mercer26263@gmail.com"
    password = "ukdvuayctymeegkv"
    message = "The driver is sleeping!!!\n {}\n See my real-time location on Maps:\n https://maps.app.goo.gl/yjGwhcS9FgUnGxeQ8".format(curtime)

    NM['Subject'] = "This is an SOS Message"                                         ##use the live location link here^^
    NM['From'] = sender_email
    NM['To'] = rec_email
    NM.set_content('Image Attachment')
    with open("Pictures0.jpg", 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    NM.add_attachment(file_data, maintype = 'image', subtype = file_type, filename = file_name)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, password)
    print("Login success")
    server.sendmail(sender_email, rec_email, message)
    server.send_message(NM)
    print("EMAIL IS SENT")
    print(time.ctime())
    
#emailalert()
