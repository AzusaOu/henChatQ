#-*-coding:utf-8-*-
# 2018.09.29
import os
import time
import pickle
import json
import gzip
import base64
import multiprocessing

from websocket import create_connection
import paho.mqtt.client as mqtt

from const import *
import alib3.acrypt as acrypt
from alib3.acrypt import RSAUtilize
from alib3.abasic import Log

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
#  0 - plain text
#  1 - file
# addition: reserve space, len = 32
# payload: body of the message

# Command:
# py hq-recv.py [ch] <PSK>
# argv           1    2

l = Log(Log.DEBUG)

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
        try:
            l.info('Creating WebSocket server...')
            self.ws = create_connection(('ws://%s:%s' % (SERVER['local_host'], SERVER['local_port'])))
        except:
            l.error('No websocket connection')
        self.channel = ''
        self.psk = psk

    def wsNotification(self, content):
        self.ws.send(content)

    def updateChannel(self, channel):
        self.channel = channel
        self.client.subscribe(acrypt.str2md5(channel.encode()).decode())
        l.info('Listening on channel: [%s]' % channel)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            l.info('Connect to server successfully')
        else:
            l.error('Server error!')
    
    def on_message(self, client, userdata, msg):
        verified = False
        sameTime = True

        timenow = int(time.time())
        l.info('%d bytes data received' % int(len(msg.payload) / 8))
        try:
            l.debug('Decrypting... (PSK=%s)' % self.psk)
            msg = gzip.decompress(acrypt.AES256.decrypt(msg.payload, self.psk))
        except:
            l.error('*** PSK ERROR ***\n')
            return -1

        sender = msg[:32].replace(b'\x99', b'').decode('utf-8')
        l.info('Sender: [%s]' % sender)

        timeStamp = int(msg[32:42])
        if int(timeStamp - timenow) >= 1800:
            l.error('*** INVALID TIMESTAMP ***')
            sameTime = False
    
        sign = msg[42:298]

        stype = msg[298:299]

        addition = msg[299:331].replace(b'\x99', b'')

        payload = msg[331:]

        idFile = PATH.PATH_FRIENDS + '%s@%s' % (sender, self.channel)
        l.debug('Search for key in %s' % idFile)
        if os.path.exists(idFile) == False:
            l.warning('*** UNKNOWN USER ***')
        else:
            try:
                recv_md5 = RSAUtilize.decrypt(pickle.load(open(idFile, 'rb')), sign)
                calc_md5 = acrypt.str2md5(msg[32:42] + payload)
                if recv_md5 != calc_md5:
                    l.error('*** SIGNATURE VERIFY FAILED ***')
                    print(recv_md5)
                    print(calc_md5)
                    return -1
                else:
                    verified = True
            except:
                l.error('*** FAKE USER ***')
                return -1
        
        if stype == STYPE.PLAINTEXT:
            origin = payload.decode('utf-8')
            l.msg(origin, 'MSG')
            toInterface = json.dumps(
                {'type': 0x04,
                'ch': self.channel,
                'from': sender,
                'time': timeStamp,
                'msg': origin,
                'verified': verified,
                'timeCheck': sameTime}
            )
            self.wsNotification(toInterface)
        
        elif stype == STYPE.FILE:
            # print('=== FILE ===')
            fname = base64.b64decode(addition)
            print('Name: %s' % fname.decode('utf-8'))
            writeout(fname, payload)
        
        elif stype == STYPE.FOLLOW:
            # print('=== FOLLOWING REQUEST ===')
            print(idFile)
            if os.path.exists(idFile) == False:
                print('Channel: %s' % self.channel)
                print('   User: %s' % sender)
                print('PublicH: %s' % acrypt.str2md5(payload).decode())
                newPBK = pickle.loads(payload)
                pickle.dump(newPBK, open(idFile, 'wb'))
                toInterface = json.dumps(
                    {'type': 0x04,
                    'ch': self.channel,
                    'from': sender,
                    'time': timeStamp,
                    'msg': '*** ID [%s] HAS BEEN ADDED INTO KONWN LIST ***'%sender,
                    'verified': verified,
                    'timeCheck': sameTime}
                )
                self.wsNotification(toInterface)
            else:
                l.info('You have added [%s]. Ignore' % sender)
        else:
            l.warn('*** UNKNOWN MESSAGE TYPE ***')
            print(msg)

    def loop(self):
        self.client.loop_forever()

def recvStart(ch, psk=b'henChatQ'):
    l.info('Listening on %s:%d...' % (SERVER['host'], SERVER['port']))
    try:
        c = Client(SERVER['host'], SERVER['port'], SERVER['timeout'], psk)
        c.updateChannel(ch)
        c.loop()
    except:
        l.error('*** ERROR PARAMETER ***')

if __name__ == '__main__':
    import sys
    ch = sys.argv[1]
    if len(sys.argv) == 3:
        psk = sys.argv[2].encode('utf-8')
    else:
        psk = b'henChatQ'
    recvStart(ch, psk)