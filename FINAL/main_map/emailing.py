import smtplib, ssl
from getpass import getpass
def send_email(recievers = ""):
    port = 465  # For SSL
    password = getpass()
    # Create a secure SSL context
    context = ssl.create_default_context()
    sender = "testingmech888@gmail.com"
    receivers = ['tumiolason@gmail.com']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <tumiolason@gmail.com>
    Subject: bottle

    The Water in your bottle is empty
    """
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)         
            print ("Successfully sent email")
        except:
            print("Email was unable to send.")

