from debug import *
from zoodb import *
import rpclib

def transfer(sender,token, recipient, zoobars):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('transfer', sender=sender,token=token,recipient=recipient,zoobars=zoobars)
        return ret

def balance(username):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance', username=username)
        return ret    

def adduser(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('adduser', username=username)
        return ret

def get_log(username):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('get_log', username=username)
        return ret