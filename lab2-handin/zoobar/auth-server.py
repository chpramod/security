#!/usr/bin/python

import rpclib
import sys
import auth
from debug import *

class AuthRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
	def rpc_login(self, username,password):
		token = auth.login(username,password)    	
		return token

	def rpc_register(self,username,password):
		token = auth.register(username,password)
		return token

	def rpc_check_token(self,username,token):
		valid = auth.check_token(username,token)
		return valid

	def rpc_get_token(self,username):
		token = auth.get_token(username)
		return token

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)
