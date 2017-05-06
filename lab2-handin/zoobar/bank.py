from zoodb import *
from debug import *
import auth_client
import time

def transfer(sender,token,recipient, zoobars):
    bankdb = bank_setup()
    senderp = bankdb.query(Bank).get(sender)
    recipientp = bankdb.query(Bank).get(recipient)
    if not auth_client.check_token(sender,token):
        #invalid token
        raise Exception('Token of sender could not be validated')
    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankdb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    db = bank_setup()
    person = db.query(Bank).get(username)
    return person.zoobars

def adduser(username):
    db = bank_setup()
    person = db.query(Bank).get(username)
    if not person:
        newperson = Bank()
        newperson.username = username
        db.add(newperson)
        db.commit()

def get_log(username):
    db = transfer_setup()
    result = db.query(Transfer).filter((Transfer.sender==username) | (Transfer.recipient==username))
    # Result is not in proper json format
    def pretty_out(result):
        out = []
        for transfer in result:
            curr = {'username':username,
               'time':transfer.time,
               'sender':transfer.sender,
               'recipient':transfer.recipient,
               'amount':transfer.amount}
            out.append(curr)
        return out   
    return pretty_out(result)
    # return [format_transfer(transfer) for transfer in result]
