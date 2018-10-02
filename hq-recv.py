#-*-coding:utf-8-*-
# 2018.09.29
import os
import logging
import time
import pickle
import gzip

import paho.mqtt.client as mqtt

import alib3.acrypt as acrypt

CONF = pickle.load(open('user.conf', 'rb'))
PATH_FRIENDS = 'friends/'

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
# py hq-recv.py [ch] <PSK>
# argv           1    2

logging.basicConfig(level=logging.INFO)

def writeout(fname, raw):
    with open(fname, 'wb') as o:
        o.write(raw)

def readin(fname):
    with open(fname, 'rb') as o:
        return o.read()

class Client():
    def __init__(self, host, port, timeout, psk):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(host, port, timeout)
        self.channel = ''
        self.psk = psk
    
    def updateChannel(self, channel):
        self.channel = channel
        self.client.subscribe(self.channel)
        logging.info('Tune in channel: [%s]' % channel)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info('Connect to server successfully')
        else:
            logging.error('Server error!')
    
    def on_message(self, client, userdata, msg):
        timenow = int(time.time())
        print('%d bytes data received' % int(len(msg.payload) / 8))
        try:
            msg = gzip.decompress(acrypt.AES256.decrypt(msg.payload, self.psk))
        except:
            logging.error('*** PSK ERROR ***')
            print('')
            return -1
        sender = msg[:32].replace(b'\x99', b'').decode('utf-8')
        logging.info('New msg from: [%s]' % sender)

        timeStamp = int(msg[32:42])
        if int(timeStamp - timenow) >= 1800:
            logging.error('*** INVALID TIMESTAMP ***')
    
        sign = msg[42:298]

        stype = msg[298:299]

        addition = msg[299:331]

        payload = msg[331:]

        if os.path.exists(PATH_FRIENDS+'%s@%s'%(sender, self.channel)) == False:
            logging.warn('*** [%s] CANNOT BE VERIFIED ***' % sender)
        
        if stype == b'\x00':
            print(payload.decode('utf-8'))
        
        elif stype == b'\x01':
            print('[Get a file]')
            writeout('test', payload)
        
        else:
            print(msg)
        
        print('')

    def loop(self):
        self.client.loop_forever()

if __name__ == '__main__':
    import sys
    ch = sys.argv[1]
    if len(sys.argv) == 3:
        psk = sys.argv[2].encode('utf-8')
    else:
        psk = b'henChatQ'
    print('Listening on %s:%d...' % (CONF['server'], CONF['port']))
    c = Client(CONF['server'], CONF['port'], CONF['timeout'], psk)
    c.updateChannel(ch)
    c.loop()