# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
 
import hashlib, binascii, os
from decouple import config
from datetime import date

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/


def hash_pass( password ):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash) # return bytes

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def get_sy():
    START_MONTH = config('START_MONTH', default=8, cast=int)

    today = date.today()
    current_year = today.year
    current_month = today.month

    if int(current_month) > int(START_MONTH):
        return dict(start=(today.year - 1), end=today.year)
    else:
        return dict(start=today.year, end=(today.year + 1))


