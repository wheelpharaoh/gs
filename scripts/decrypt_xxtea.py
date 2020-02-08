#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import argparse

import xxtea

def _remove_header(str, sign):
	return str[len(sign):]

def main(args):
	_xsign = "XXTEA"
	_key = "g5kgGYr3peprprGU" 

	filein = args.file #4000117.dat'
	fileout = filein + ".lua"
	with open(filein, 'rb') as raw:
		with open(fileout, 'wb') as output:
				rawdata = raw.read()
				#print(rawdata)
				data = _remove_header(rawdata, _xsign)
				#print('\n', data)
				plain = xxtea.decrypt(data, _key)
				#print(plain)

				output.write(plain)      

if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="xxtea encrypted file")
	args = parser.parse_args()        
	main(args)

