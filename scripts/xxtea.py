#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import struct

_DELTA = 0x9E3779B9

def _long2str(v, w):
	n = (len(v) - 1) << 2
	if w:
		m = v[-1]
		if (m < n - 3) or (m > n): return ''
		n = m
	s = struct.pack('<%iL' % len(v), *v)
	#print(s[0:n])
	return s[0:n] if w else s

def _str2long(s, w):
	n = len(s)
	m = (4 - (n & 3) & 3) + n
	s = s.ljust(m, b"\0")
	v = list(struct.unpack('<%iL' % (m >> 2), s))
	if w: v.append(n)
	return v

def do_xxtea_encrypt(str, key):
	if str == '': return str
	v = _str2long(str, True)
	k = _str2long(key.ljust(16, "\0"), False)
	n = len(v) - 1
	z = v[n]
	y = v[0]
	sum = 0
	q = 6 + 52 // (n + 1)
	while q > 0:
		sum = (sum + _DELTA) & 0xffffffff
		e = sum >> 2 & 3
		for p in xrange(n):
			y = v[p + 1]
			v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
			z = v[p]
		y = v[0]
		v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff
		z = v[n]
		q -= 1
	return _long2str(v, False)

def do_xxtea_decrypt(str, key):
	if str == b'': return str
	v = _str2long(str, False)
	k = _str2long(key.ljust(16, b"\0"), False)
	n = len(v) - 1
	z = v[n]
	y = v[0]
	q = 6 + 52 // (n + 1)
	sum = (q * _DELTA) & 0xffffffff
	while (sum != 0):
		e = sum >> 2 & 3
		for p in range(n, 0, -1):
			z = v[p - 1]
			v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
			y = v[p]
		z = v[n]
		v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff
		y = v[0]
		sum = (sum - _DELTA) & 0xffffffff
	return _long2str(v, True)

def fix_key_length(key):
	key = key + ('\x00'  * (16 - len(key))) 
	return key

def decrypt(str, key):
	if len(key) < 16:
		res = do_xxtea_decrypt(str, fix_key_length(key))
	else:
		res = do_xxtea_decrypt(str, key)
	return res

def encrypt(str, key):
	if len(key) < 16:
		res = do_xxtea_encrypt(str, fix_key_length(key))
	else:
		res = do_xxtea_encrypt(str, key)

def main():
	_xsign = "XXTEA"
	_key = "g5kgGYr3peprprGU" 

	def _remove_header(str, sign):
		return str[len(sign):]

	filein = '/Users/jo/dev/gs/dat/4000117.dat'
	fileout = filein + ".lua"
	with open(filein, 'rb') as raw:
		with open(fileout, 'wb') as output:
				rawdata = raw.read()
				#print(rawdata)
				data = _remove_header(rawdata, _xsign)
				#print('\n', data)
				plain = decrypt(data, _key)
				#print(plain)

				output.write(plain)      

if __name__== "__main__": 
	main()

