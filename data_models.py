from dataclasses import dataclass

# from, date, subject, body

@dataclass
class Message():
    to : str
    msg_from : str
    date: str
    subject: str
    body : str

    def __init__(self,to,msg_from,date,subject,body):
        self.to = to
        self.msg_from = msg_from
        self.date =  date
        self.subject =  subject
        self.body =  body





