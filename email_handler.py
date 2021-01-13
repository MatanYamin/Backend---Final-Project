import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText





def email_handle(data):
    content_message = email_content(data)
    # mail_content = "Hello, This is a simple mail. There is only text," \
    #                " no attachments are there The mail is sent using Python SMTP library.Thank You"
    #The mail addresses and password
    sender_address = 'matanyamin01@gmail.com'
    sender_pass = 'Beitar$123'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = data["email"]
    message['Subject'] = 'עוד רגע ואנחנו אצלכם'   #The subject line
    #The body and the attachments for the mail
    message.attach(content_message)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, data["email"], text)
    session.quit()
    print('Mail Sent')


def email_content(data):
    html = """\
        <html dir="rtl">
          <head> <img src="https://i.ibb.co/yh7CyXp/Sky-Cleaner.jpg" width="500">
           <meta charset="utf-8">
           </head>
          <body>
            <p>שלום """ + data["full name"] + """<br>
              תודה רבה על זימון פגישה עם סקייקלינר! פרטי התור שלך נמצאים למטה.<br>
              שעת התור:<br> """ + data["time"] + """ <br>
              ב""" + data["day"] + ", " + data["number date"] + """ <br>
              מיקום: <br> 
              """ + data["full address"] + """ <br>
              סוג השירות: <br>
              """ + data["service"] + """
            </p>
          </body>
        </html>
        """
    plain_text = MIMEText(html, 'html')
    return plain_text

# email_handle(data, "yamin2211@gmail.com")