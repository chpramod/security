from zoodb import *
from debug import *

import hashlib
import pbkdf2
import random
import bank_client
from base64 import b64encode
from os import urandom

def newtoken(db, person):
    hashinput = "%s%.10f" % (person.password, random.random())
    person.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return person.token

def login(username, password):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if not person:
        return None
    hash_password = pbkdf2.PBKDF2(password,person.salt).hexread(32)
    if person.password == hash_password:
        return newtoken(db, person)
    else:
        return None

def register(username, password):
    db_cred = cred_setup()
    db_person = person_setup()
    person_cred = db_cred.query(Cred).get(username)
    #Check if user exists in cred table
    if person_cred:
        return None
    #Add to cred table
    newperson_cred = Cred()
    newperson_cred.username = username
    # newperson_cred.password = password
    # salt = os.urandom
    salt_bytes = urandom(64)
    salt = b64encode(salt_bytes).decode('utf-8')
    hash_password = pbkdf2.PBKDF2(password,salt).hexread(32)
    newperson_cred.password = hash_password
    newperson_cred.salt = salt
    db_cred.add(newperson_cred)
    db_cred.commit()
    #Add to person table
    newperson = Person()
    newperson.username = username
    db_person.add(newperson)
    db_person.commit()
    bank_client.adduser(username)
    return newtoken(db_cred, newperson_cred)

def check_token(username, token):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if person and person.token == token:
        return True
    else:
        return False

def get_token(username):
    db = cred_setup()
    person = db.query(Cred).get(username)
    return person.token

