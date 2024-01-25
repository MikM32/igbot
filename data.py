"""
#   modulo para el manejo de las cookies en bases de datos
"""
import sqlite3
import json.decoder
from json import JSONDecoder
from json import JSONEncoder
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from bot_exceptions import CookiesDontExists

KEY = '9a4cd918a18eea0c9e3f72203ecaafa1'

def dontgonnatellyou(data: str) -> bytes:


    key = bytes(KEY, 'ansi')
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(bytes(data,'ansi'))

    enc_str = cipher.nonce + tag + ciphertext

    enc_str_64 = b64encode(enc_str)
    
    return enc_str_64.decode()

def gonnatellyou(edata64:str) -> str:

    edata = b64decode(bytes(edata64, 'utf-8'))
    
    nonce = edata[0:16]
    tag = edata[16:32]
    cdata = edata[32:]

    key = bytes(KEY, 'ansi')
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(cdata, tag)

    return data.decode('ansi')

def db_create(db: str):
    pass

def db_load_cookies(db: str, social:str, username: str) -> list[dict]:

    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        load_sql = f"SELECT * FROM {social}_cookies WHERE Usuario LIKE '{username}'"
        cur.execute(load_sql)
        filas = cur.fetchall()
        if filas == []:
            raise CookiesDontExists(username)

        cookies = gonnatellyou(filas[0][1])
        cookies = JSONDecoder().decode(cookies)
        return cookies
    

def db_save_cookies(db: str, social:str, username: str, cookies: list[dict]):

    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cookies_str = JSONEncoder().encode(cookies)
        enc_cookies = dontgonnatellyou(cookies_str)

        insert_sql = f"INSERT INTO {social}_cookies(Usuario, Enc_Cookies) VALUES('{username}','{enc_cookies}')"
        cur.execute(insert_sql)
        conn.commit()

    
