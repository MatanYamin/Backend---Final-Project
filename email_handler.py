# Programmed by Matan Yamin - Final Project.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email_handle(data):
    """this function gets an html content and send an Email using SMTP protocol
    to the customer and to the manager"""
    content_message = email_content_to_customer(data)  # content will hold the HTML content in email
    # mail_content = "Hello, This is a simple mail. There is only text," \
    #                " no attachments are there The mail is sent using Python SMTP library.Thank You"
    #The mail addresses and password
    sender_address = 'matanyamin01@gmail.com'  # for now, this is my email
    sender_pass = 'Beitar$123'  # pass
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = data["email"]
    message['Subject'] = 'עוד רגע ואנחנו אצלכם'  # The subject line
    #The body and the attachments for the mail
    message.attach(content_message)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port 587
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, data["email"], text)
    session.quit()
    print("Customer mail sent")
    email_handle_manager(data)  # after we sent to customer, we will send to manager
    print("all is sent")
    return "all is sent"


def email_handle_manager(data):
    """this function get an html content specially for the manager and send it to him
    after finding a nwe booking"""
    content_message = email_content_to_manager(data)  # containing the manager email content
    # mail_content = "Hello, This is a simple mail. There is only text," \
    #                " no attachments are there The mail is sent using Python SMTP library.Thank You"
    #The mail addresses and password
    sender_address = 'matanyamin01@gmail.com'  # manager email
    sender_pass = 'Beitar$123'  # password for connecting
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    # message['To'] = 'matanyamin01@gmail.com'
    message['Subject'] = 'זומן תור חדש!'   #The subject line
    #The body and the attachments for the mail
    message.attach(content_message)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port 587 on SMTP protocol
    session.starttls() #enable security
    session.login(sender_address, sender_pass) # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, "matanyamin01@gmail.com", text)
    session.quit()
    print('Admin Mail Sent')
    return 'Admin Mail Sent'


# NEW FOR NOW
def email_content_to_customer(data):
    """this is html content for the customer email
    will get some changes in the future
    needs to add more features"""
    html = """\
        <html dir="RTL">
          <head> <img src="https://i.ibb.co/yh7CyXp/Sky-Cleaner.jpg" width="200">
           <meta charset="utf-8">
           </head>
          <body> 
            <p style="direction: rtl; text-align: right; font-family:georgia,garamond,serif;font-size:20px;font-style:italic;">שלום """ + \
           data["fullName"] + """<br>
              תודה על זימון הפגישה עם סקייקלינר, עוד קצת ואתם נקיים! הפגישה נקבעה בהצלחה והועברה אל צוות המומחים שלנו!  <br> <br> פרטי התור שלך נמצאים למטה.<br>&#8986;
            מתי? ב """ + data["day"] + """ <br>
              בשעה """ + data["hour"] + """ <br><br> &#128467;  
               איפה?  <br>  	
              """ + data["fullAddress"] + """ <br><br>
              &#129532; מה אנחנו מנקים? <br>
              """ + data["service"] + """ <br><br> 
              """ + data["price"] + """
              הערות: """ + data["comments"] + """ <br/><br/>
              לכל שאלה אפשר לפנות דרך כל אחד מהקישורים שנמצאים למטה. <br><br>
              מחכים לראותכם, צוות סקאי קלינר. <br>
              <p style="direction: rtl; text-align: center; font-family:georgia,garamond,serif;font-size:25px;font-style:italic;">
              <br> <br>עקבו אחרינו באינסטגרם ובפייסבוק והתעדכנו אחר ההגרלות החדשות! <br <br>
              </p>
            </p>
          <footer style="direction: rtl; text-align: center;">

            <a href="https://www.facebook.com/SkyCleanerIsrael">
            <img src='https://purpleironingservices.com/wp-content/uploads/2017/02/facebook-footer-share.png' style='width: 6%;'>
            </a>
            &nbsp;
            <a href="https://www.instagram.com/skycleaner1/">
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/1024px-Instagram_icon.png' style='width: 6%;'>
            </a>
            &nbsp;
            <a href="https://easy.co.il/page/10080031">
            <img src='https://play-lh.googleusercontent.com/LaVRvqc6Hxy2EQj8G6-qsuOUz66Q5GZBOhAOs6n7YjsaopFbQwjDhYqurw_RS5grRQ' style='width: 6%;'>
            </a>
            &nbsp;
            <a href="mailto:skycleanerisrael@gmail.com">
            <img src='https://image.flaticon.com/icons/png/512/281/281769.png' style='width: 6%;'>
            </a>
            &nbsp;
            <a href="tel:054-220-1042" target="_blank">
            <img src='https://simpleicon.com/wp-content/uploads/phone-symbol-1.png' style='width: 6%;'>
            </a>
            &nbsp;
            <a href="https://api.whatsapp.com/send?phone=972542201042&lang=he">
            <img src='https://cdn2.iconfinder.com/data/icons/social-messaging-ui-color-shapes-2-free/128/social-whatsapp-circle-512.png' style='width: 6%;'>
            </a>
            </footer>

          </body>
        </html>
        """
    plain_text = MIMEText(html, 'html')
    return plain_text


# NEW FOR NOW
def email_content_to_manager(data):
    """this is an html content for the managers"""
    if not data["comments"]:
        data["comments"] = "אין"
    if not data["addons"]:
        data["addons"] = "אין"
    html = """\
            <html dir="RTL">
              <head>
               <meta charset="utf-8">
               </head>
              <body> 
                <p style="direction: rtl; text-align: right;">תור חדש נקבע כרגע! <br> <br>
                 שם הלקוח: """ + \
           data["fullName"] + """<br>
                  כתובת: <br> """ + data["fullAddress"] + """ <br>
                  תאריך: """ + data["day"] + """
                  בשעה: """ + data["hour"] + """ <br>
                  מספר הטלפון של הלקוח: 
                  <a href="tel:""" + data["phone"] + """">""" + data["phone"] + """</a> <br>
                  מייל של הלקוח: """ + data["email"] + """ <br>
                  סוג השירות שהוזמן: """ + data["service"] + """ <br> 
                  תוספות: """ + data["addons"] + """ <br> 
                  הערות של הלקוח: """ +  data["comments"] + """ <br>
                  """ + data["price"] + """
                   <br>
                </p>
              </body>
            </html>
            """
    plain_text = MIMEText(html, 'html')
    return plain_text