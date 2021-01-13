import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email_content(data):
    html = """\
        <html>
          <head> first </head>
          <body>
            <p>שלום """ + data["full_name"] + """<br>
              תודה רבה על זימון פגישה עם סקייקלינר! פרטי התור שלך נמצאים למטה.<br>
              שעת התור: """ + data["start_date"] + """ <br>
              מיקום: <br> 
              """ + data["full_address"] + """ <br>
              סוג השירות: <br>
              """ + data["service"] + """
               Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """
    plain_text = MIMEText(html, 'html')
    return plain_text


def email_handle(data, email):
    content_message = email_content(data)
    # mail_content = "Hello, This is a simple mail. There is only text," \
    #                " no attachments are there The mail is sent using Python SMTP library.Thank You"
    #The mail addresses and password
    sender_address = 'matanyamin01@gmail.com'
    sender_pass = 'Beitar$123'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = email
    message['Subject'] = 'אישור תור - סקייקלינר'   #The subject line
    #The body and the attachments for the mail
    message.attach(content_message)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, email, text)
    session.quit()
    print('Mail Sent')


mail = email_content("matan yamin")
email_handle(mail, "yamin2211@gmail.com")