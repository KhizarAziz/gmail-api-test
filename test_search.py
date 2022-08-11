from my_gmail_api import MyGmailAPI


api = MyGmailAPI()
api.auth_user()# authentication and connection

USER_ID = 'me' # id for corresponding email. ('me' can be used if wanna use default logged in)
search_string = 'United' # search string for email filtering

messages_list = api.search_messages(USER_ID,search_string) # getting list of similar emails

if messages_list:
    for ID in messages_list:
        message = api.get_message(user_id=USER_ID, message_id=ID)
        print(f'To: {message.to}\nFrom: {message.msg_from}\nDate:'
              f'{message.date}\nSubject:{message.subject}\nBody:{message.body}')
