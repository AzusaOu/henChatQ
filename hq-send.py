#-*-coding:utf-8-*-
# 2018.09.29
import time
import pickle
import sys
import gzip

import paho.mqtt.client as mqtt

import alib3.acrypt as acrypt

CONF = pickle.load(open('user.conf', 'rb'))

# Message formate:
# +----+----+----+----+--------+--------------------+
# | id |time|sign|type|addition|      payload       |
# +----+----+----+----+--------+--------------------+
#   32   10  256   1      32             x
# id: name of the sender, len = 32
# time: time stamp of the message, len = 10
# sign: of md5(timestamp + payload), len = 256
# type: type of the message, len = 1
#  0 - plain text
#  1 - file
# addition: reserve space, len = 32
# payload: body of the message

# Command:
# py hq-send.py [ch] [-t|-f] [plaintext|filepath] <PSK>
# argv           1    2       3                    4

def msgGen(stype, content, PSK):
    sender = acrypt.padding(CONF['user'], 32)
    timeStamp = bytes(str(int(time.time())), 'utf-8')
    content = content.encode('utf-8')
    ru = acrypt.RSAUtilize()
    # Plain text
    if stype == '-t':
        md5_msg = acrypt.str2md5(timeStamp + content)
        sign = ru.encrypt(CONF['pbk'], md5_msg)
        msg = sender + timeStamp + sign + b'\x00' + acrypt.padding(b'', 32) + content
    # File
    elif stype == '-f':
        with open(content, 'rb') as o:
            buf = o.read()
        if len(buf) > 99999:
            return -1
        msg = bytes(sender + token + '\x01' + '%05d'%len(buf), 'utf-8') + buf
    return acrypt.AES256.encrypt(gzip.compress(msg), PSK)

if __name__ == '__main__':
    ch = sys.argv[1]
    tp = sys.argv[2]
    ms = sys.argv[3]
    if len(sys.argv) == 5:
        psk = sys.argv[4].encode('utf-8')
    else:
        psk = b'henChatQ'
    client = mqtt.Client()
    client.connect(CONF['server'], CONF['port'], CONF['timeout'])
    msg = msgGen(tp, ms, psk)
    print('%d bytes data has been sent' % int(len(msg)/8))
    if msg:
        client.publish(str(sys.argv[1]), msg)

    # sent = gzip.decompress(acrypt.AES256.decrypt(msg, psk))
    # print(sent)
    