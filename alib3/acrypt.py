# -*- coding: utf-8 -*-
# <-- AZLIBRARY PROJECT (Python2, 3) -->
# Started: 2018.02.02
# Latest: 2018.09.13

import hashlib
import base64

try:
	import rsa
	from Crypto.Hash import SHA256
	from Crypto.Cipher import AES
	from Crypto import Random
except:
	print('Some libraries are not installed...')
	raise

def padding(binary, maxlen, c=b'\x99'):
	if len(binary) > maxlen:
		return None
	elif len(binary) == maxlen:
		return binary
	else:
		for i in range(maxlen - len(binary)):
			binary += c
		return binary

def str2md5(plainText):
	hl = hashlib.md5()
	hl.update(base64.b64encode(plainText))
	return hl.hexdigest().encode('utf-8')

class RSAGen:
	def __init__(self, length=2048):
		(pubkey, privkey) = rsa.newkeys(length)
		self.pbk = pubkey
		self.pvk = privkey

	def saveAsPEM(self, fname_pbk='public.pem', fname_pvk='private.pem'):
		pub = self.pbk.save_pkcs1()
		pri = self.pvk.save_pkcs1()
		with open(fname_pbk, 'wb') as o:
			o.write(pub)
		with open(fname_pvk, 'wb') as o:
			o.write(pri)

	def get(self, pkcs1=False):
		if pkcs1:
			return self.pbk.save_pkcs1(), self.pvk.save_pkcs1()
		else:
			return self.pbk, self.pvk

class RSAUtilize:
	def loadKeyFromPEM(fname, pbk=True):
		with open(fname, 'rb') as o:
			if pbk:
				return rsa.PublicKey.load_pkcs1(o.read())
			else:
				return rsa.PrivateKey.load_pkcs1(o.read())

	def encrypt(key, msg):
		return rsa.encrypt(msg, key)

	def decrypt(key, msg):
		return rsa.decrypt(msg, key)

class AES256:
	def encrypt(msg, pwd):
		h = SHA256.new()
		h.update(pwd)
		key = h.hexdigest().encode()
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(key[:32], AES.MODE_GCM, iv)
		msg = iv + cipher.encrypt((msg))
		return msg
	
	def decrypt(msg, pwd):
		h = SHA256.new()
		h.update(pwd)
		key = h.hexdigest().encode()
		iv = msg[:AES.block_size]
		decipher = AES.new(key[:32], AES.MODE_GCM, iv)
		ori = decipher.decrypt((msg[AES.block_size:]))
		return ori
