import json
import multiprocessing
import threading

from ws.websocket_server import WebsocketServer
import init, rx, tx

VERSION = '181005'

class HCS:
	def __init__(self, port, host='127.0.0.1'):
		self.host = host
		self.port = port
		self.client_interface = None
		self.channels = []

	def commandReceived(self, client, server, msg):
		cmd = json.loads(msg)

		# Interface online
		if cmd['type'] == 0x00:
			print('Interface online.')
			self.client_interface = client
			reply = json.dumps({'type': 0x00, 'msg': 'henChatQ.v%s'%VERSION})
			server.send_message(self.client_interface, reply)

		# Create new user
		# {'type': 0x01, 'username': 'xxx'}
		if cmd['type'] == 0x01:
			init.initNew(cmd['username'])
		
		# Send a message
		# {'type': 0x02,
		#  'ch': 'xxx',
		#  'stype': 'xxx',
		#  'msg': 'xxx',
		#  'psk': 'xxx',
		#  'qos': 1}
		elif cmd['type'] == 0x02:
			tx.sendMsg(cmd['ch'], cmd['stype'], cmd['msg'], cmd['psk'], cmd['qos'])

		# Listen on a channel
		# {'type': 0x03,
		#  'ch': 'xxx',
		#  'psk': b'xxx'}
		elif cmd['type'] == 0x03:
			print('Listen on channel: [%s]' % cmd['ch'])
			# if cmd['ch'] in self.channels == False:
			self.channels.append(cmd['ch'])
			th = threading.Thread(target=rx.recvStart, name='ch-%s'%cmd['ch'], args=(cmd['ch'], cmd['psk'].encode('utf-8')))
			th.start()
			# p.join()
		
		# New message comes
		# {'type': 0x04,
		#  'ch': 'xxx',
		#  'from': 'xxx',
		#  'msg': 'xxx'}
		elif cmd['type'] == 0x04:
			if self.client_interface:
				packet = json.dumps({'type': 0x01, 'ch': cmd['ch'], 'from': cmd['from'], 'msg': cmd['msg']})
				server.send_message(self.client_interface, packet)
			else:
				print('Receive a message from %s. Content:\n%s' % (cmd['ch'], cmd['from'], cmd['msg']))

	def start(self):
		server = WebsocketServer(self.port, host=self.host)
		server.set_fn_message_received(self.commandReceived)
		server.run_forever()

def main():
	hcs = HCS(43210)
	hcs.start()

if __name__ == '__main__':
	main()