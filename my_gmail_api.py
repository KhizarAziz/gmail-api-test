import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from data_models import Message



SCOPES = ['https://mail.google.com/']

class MyGmailAPI():

    service = None
    creds = None


    def auth_user(self):
        if os.path.exists('token.json'): # if user already authenticated load creds from generated file
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid: # refresh user if required
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else: # authenticated user if doesnt exist.
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=self.creds)
            return self.service
        except HttpError as error:
            print(f'An error occurred: {error}')

    '''
       This method takes the message id and return corresponding message as Message object defined in data_models  
    '''
    def get_message(self,user_id: str, message_id: str) -> Message:
        # getting all messages based on id
        message = self.service.users().messages().get(userId=user_id, id=message_id, format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII')) # decoding raw message
        msg_str = email.message_from_bytes(msg_raw) # converting bytes to email message object
        content_types = msg_str.get_content_maintype() # type of content of message (multipart/digest)

        msg_body : str
        if content_types == 'multipart':
            plain_content, html_content = msg_str.get_payload()
            msg_body =  plain_content.get_payload()
        else:
            msg_body = msg_str.get_payload()


        # parsing msg to our custom message model
        message = Message(to=msg_str['to'],msg_from=msg_str['from'],date=msg_str['date'],
                          subject=msg_str['subject'],body=msg_body)
        return message

    '''
       This method takes the userid and search string to filter out messages based on that
        and return list of message ids.   
    '''
    def search_messages(self,user_id: str, search_string: str) -> list:
        results = self.service.users().messages().list(userId=user_id, q=search_string).execute()
        if results['resultSizeEstimate'] > 0:
            message_ids = [x['id'] for x in results['messages']]
            print(f'Found  {results["resultSizeEstimate"]} results.')
            return message_ids
        else:
            print('No search results matching :', search_string)
            return None

    '''
       This method takes email information such as to,subject,message and sends an email from user_id's email.  
    '''
    def send_email(self,user_id: str, to:str, subject: str, body:str):

        # MIMEMUltipart for attaching parts of email into Mime Object
        msg = MIMEMultipart()
        msg['to'] = to
        msg['subject'] = subject
        msg_body = body
        msg.attach(MIMEText(msg_body, 'plain'))
        raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        # Sending Mime email object
        self.service.users().messages().send(userId=user_id, body={'raw': raw_string}).execute()

        print('Email Sent...!')







