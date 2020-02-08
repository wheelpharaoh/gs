import binascii
import io #import StringIO

class PKCS7Encoder(object):
	def __init__(self, k=16):
	   self.k = k

	def decode(self, text):
		nl = len(text)
		val = text[-1]
		#val = int(binascii.hexlify(text[-1]), 16)
		if val > self.k:
			raise ValueError('Input is not padded or padding is corrupt')

		l = nl - val
		return text[:l]

	def encode(self, text):
		l = len(text)
		output = io.StringIO()
		val = self.k - (l % self.k)
		print('val ', val)
		for _ in range(val):
			output.write('%02x' % val)
		print('output ', output.getvalue())
		#print('text ', text)
		print('output len ', len(output.getvalue()))
		print('text len ', len(text))

		return text.encode('utf-8') + binascii.unhexlify(output.getvalue())

import sys

try:
	import crypto
	sys.modules['Crypto'] = crypto
	from crypto.Cipher import AES
except:
	from Crypto.Cipher import AES 
import base64
import json


class Crypter(object):
	def __init__(self):
		self.encoder=PKCS7Encoder()
	
	def decrypt(self,input,key):
		aes_new = AES.new(base64.b64decode(key), AES.MODE_CBC, '\x00'*16)
		aes_decrypt = aes_new.decrypt(base64.b64decode(input))
		r = self.encoder.decode(aes_decrypt)
		return r

	def encrypt(self,input,key):
		padded_data=self.encoder.encode(json.dumps(input))
		return base64.b64encode(AES.new(base64.b64decode(key), AES.MODE_CBC, '\x00'*16).encrypt(padded_data))
