#!/usr/bin/python

import rpclib
import sys
import bank
from debug import *

class BankRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
	def rpc_transfer(self, sender,token, recipient, zoobars):
		bank.transfer(sender,token, recipient, zoobars)    	

	def rpc_balance(self,username):
		balance = bank.balance(username)
		return balance

	def rpc_adduser(self,username):
		bank.adduser(username)

	def rpc_get_log(self,username):
		return bank.get_log(username)
		

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)
