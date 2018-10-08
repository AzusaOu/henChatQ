#-*-coding:utf-8-*-
# 2018.09.29
import time
import os
import pickle
import json
import sys
import gzip
import base64

import paho.mqtt.client as mqtt

from const import *
import alib3.acrypt as acrypt
from alib3.acrypt import RSAUtilize

USER = pickle.load(open(PATH.PATH_USER, 'rb'))
SERVER = json.load(open(PATH.SETTING_SERVER, 'r'))

# Message formate:
# +----+----+----+----+--------+--------------------+
# | id |time|sign|type|addition|      payload       |
# +----+----+----+----+--------+--------------------+
#   32   10  256   1      32             x
# id: name of the sender, len = 32
# time: time stamp of the message, len = 10
# sign: of md5(timestamp + payload), len = 256
# type: type of the message, len = 1
#  0x00 - plain text
#  0x01 - file
#  0x02 - request of add friend
# addition: reserve space, len = 32
# payload: body of the message

# Command:
# py tx.py [ch] [-t|-f] [plaintext|filepath] <PSK>
# argv      1    2       3                    4

def msgGen(stype, content, PSK):
    sender = acrypt.padding(USER['user'], 32)
    timeStamp = bytes(str(int(time.time())), 'utf-8')
    addition = acrypt.padding(b'', 32)
    b_stype = b''

    # Plain text
    if stype == '-t':
        content = content.encode('utf-8')
        b_stype = STYPE.PLAINTEXT

    # File
    elif stype == '-f':
        b_stype = STYPE.FILE
        addition = base64.b64encode(os.path.split(content)[-1].encode('utf-8'))
        if len(addition) > 32:
            addition = addition[-32:]
        with open(content, 'rb') as o:
            content = o.read()
        # if len(buf) > 99999:
        #     return -1

    # Add address
    elif stype == '-a':
        b_stype = STYPE.FOLLOW
        content = pickle.dumps(USER['pvk'])

    md5_msg = acrypt.str2md5(timeStamp + content)
    sign = RSAUtilize.encrypt(USER['pbk'], md5_msg)
    msg = sender + timeStamp + sign + b_stype + acrypt.padding(addition, 32) + content
    return acrypt.AES256.encrypt(gzip.compress(msg), PSK)

def sendMsg(ch, stype, msg, psk=b'henChatQ', qos=1):
	client = mqtt.Client()
	client.connect(SERVER['host'], SERVER['port'], SERVER['timeout'])
	msg = msgGen(stype, msg, psk)
	if msg:
		client.publish(acrypt.str2md5(ch.encode()).decode(), msg, qos)
		print('%d bytes data has been sent' % int(len(msg)/8))
	client.disconnect()

if __name__ == '__main__':
    ch = sys.argv[1]
    tp = sys.argv[2]
    ms = sys.argv[3]
    if len(sys.argv) == 5:
        psk = sys.argv[4].encode('utf-8')
    else:
        psk = b'henChatQ'
    sendMsg(ch, tp, ms, psk, 0)