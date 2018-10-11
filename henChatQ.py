# 181010 - 1st live

import json
import pickle
## Do not use multiprocessing, or the .exe will be abnormal
# import multiprocessing
import threading
import os
import http.server
import socketserver
import webbrowser
import sys

VERSION = '0.0.1 - Beta'

bin_path = os.path.split(sys.argv[0])[:-1]
if len(bin_path) > 1:
	if os.name == 'nt':
		os.chdir('\\'.join(bin_path))
	else:
		os.chdir('/'.join(bin_path))

if os.path.exists('user.conf') == False:
	newUser = input('Create a new user: ')
	import init
	init.initNew(newUser)

from alib3.abasic import Log
from const import *
from ws.websocket_server import WebsocketServer
import rx, tx

SETTING = json.load(open('server.json', 'r'))
USER = pickle.load(open(PATH.PATH_USER, 'rb'))

l = Log(Log.DEBUG)

class HCS:
	def __init__(self, port, host='127.0.0.1'):
		self.host = host
		self.port = port
		self.client_interface = None
		if os.path.exists(PATH.INFO_CHANNELS):
			self.channels = json.load(open(PATH.INFO_CHANNELS, 'r'))
			for ch in self.channels.keys():
				th = threading.Thread(target=rx.recvStart, name='ch-%s'%ch, args=(ch, self.channels[ch].encode('utf-8')))
				th.start()
		else:
			self.channels = {}

	def commandReceived(self, client, server, msg):
		cmd = json.loads(msg)
		# print(cmd)

		# Interface online
		if cmd['type'] == API_CMD_IN.ONLINE:
			l.info('Interface online')
			self.client_interface = client
			reply = json.dumps(
				{'type': API_CMD_OUT.LOGIN,
				'msg': 'henChatQ.v%s'%VERSION,
				'user': USER['user'].decode(),
				'chs': self.channels,
				'server': '%s:%d' % (SETTING['host'], SETTING['port'])}
				)
			server.send_message(self.client_interface, reply)

		# Create new user
		# {'type': 0x01, 'username': 'xxx'}
		if cmd['type'] == API_CMD_IN.NEWUSER:
			init.initNew(cmd['username'])
		
		# Send a message
		# {'type': 0x02,
		#  'ch': 'xxx',
		#  'stype': 'xxx',
		#  'msg': 'xxx',
		#  'psk': 'xxx',
		#  'qos': 1}
		elif cmd['type'] == API_CMD_IN.SEND:
			tx.sendMsg(cmd['ch'], cmd['stype'], cmd['msg'], cmd['psk'].encode(), cmd['qos'])

		# Listen on a channel
		# {'type': 0x03,
		#  'ch': 'xxx',
		#  'psk': b'xxx'}
		elif cmd['type'] == API_CMD_IN.LISTEN:
			# print(cmd)
			cmd['ch'] = cmd['ch']
			if cmd['ch'] in self.channels.keys():
				l.error('You have already listened on the channel!')
				return -1
			self.channels[cmd['ch']] = cmd['psk']
			json.dump(self.channels, open(PATH.INFO_CHANNELS, 'w'))
			th = threading.Thread(target=rx.recvStart, name='ch-%s'%cmd['ch'], args=(cmd['ch'], cmd['psk'].encode('utf-8')))
			th.start()
			
		
		# New message comes
		# {'type': 0x04,
		#  'ch': 'xxx',
		#  'from': 'xxx',
		#  'msg': 'xxx'}
		elif cmd['type'] == RX_CMD.MSG:
			if self.client_interface:
				cmd['type'] = API_CMD_OUT.TEXTMSG
				packet = json.dumps(cmd)
				server.send_message(self.client_interface, packet)
			else:
				l.info('Receive a message from %s. Content:\n%s' % (cmd['ch'], cmd['from'], cmd['msg']))

	def start(self):
		server = WebsocketServer(self.port, host=self.host)
		server.set_fn_message_received(self.commandReceived)
		server.run_forever()

def httpServer(port=54321):
	Handler = http.server.SimpleHTTPRequestHandler
	with socketserver.TCPServer((SETTING['web_host'], port), Handler) as httpd:
		l.info('HTTP serving at port %d' % port)
		httpd.serve_forever()

def main():
	def hcs_start():
		hcs = HCS(SETTING['local_port'])
		hcs.start()
	if SETTING['front'] == 'web':
		p1 = threading.Thread(target=httpServer)
		p1.start()
		webbrowser.open('http://%s:%d' % (SETTING['web_host'], SETTING['web_port']))
	hcs_start()
	

if __name__ == '__main__':
	main()