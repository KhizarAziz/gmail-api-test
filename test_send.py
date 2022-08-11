from my_gmail_api import MyGmailAPI



api = MyGmailAPI()
api.auth_user()# authentication and connection



USER_ID = 'me' # 'me' correspondes to id that you logged in with.
to = 'khizer.awan1992@gmail.com'
subject = '3rd emails'
body = ' hello ths email is to inform you that i have created the send email method inside my_gmail_api script...!'
api.send_email(USER_ID,to,subject,body)