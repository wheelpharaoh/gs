#!/usr/bin/env python3
import os

from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import ctx

import math
import base64
import ujson as json
import loot


class DumpLoot:
	def __init__(self, default_key='ZFlyUU0ycFJaTVlFRkVoaA=='):
		self.default_key = default_key
		self.game_init_key = base64.b64encode("dYrQM2pRZMYEFEhh\\ZgAEi{I[?ZToT@G".encode('utf-8'))
		self.c = loot.Crypter()
		self.enc_key = ''
		self.hack = True


		blist = body['result']['quest']['battle_list']
		for i in blist:
			for j in i['enemy_list']:
				if isinstance(j, dict):
					if j['drop_list']:
						enemy_drops.append(j['drop_list'])
		drops_list = []
		for i in enemy_drops:
			for j in i:
				drops_list.append(j)
		return drops_list


	def drops(self, body):
		# drop_typs:
		drop_types = {
			4: '',
			5: 'materials',
			8: 'equipment',
			9: 'unit',
			13: 'quest material',
			17: '',
			22: 'shop currency',
			28: 'crest'
		}

		food_id = {
			'1028': 'unit exp',
			'1034': 'light cake',
			'1013': 'salad'
		}

		crest_type = {
			101: 'HP UP',
			102: 'ATK UP',
			103: 'DEF UP',
			104: 'All Status UP',
			105: 'Arts Gauge UP',
			106: 'Heal Amount UP',
			107: 'Poison res',
			108: 'Paralyze res',
			109: 'Curse res',
			110: 'Seal res',
			111: 'Blind res',
			112: 'Disease res',
			113: 'Freeze res',
			114: 'Burn res',
			115: 'Status Ailment res',
			116: 'CRI DMG UP',
			117: 'Skill CT DOWN',
			118: 'Equipment CT DOWN',
			119: 'BE Output UP',
			120: 'Unit EXP UP',
			121: 'Player EXP UP',
			122: 'Gren up',
			123: 'Fire res',
			124: 'Water res',
			125: 'Earth res',
			126: 'Light res',
			127: 'Dark res',
			128: 'CRI Rate UP',
			129: 'Break power UP',
			130: 'Promisee of Funeral God',
			131: 'Cursed poison',
			132: 'Mind of Stillness',
			133: 'Incandescence',
			134: 'Glittering Dragon Blessing'
		} 

		crest_level = {
			"040": "4",
			"041": "4+",
			"030": "3",
			"031": "3+",
			"020": "2",
			"021": "2+",
			"010": "1",
			"011": "1+",
		}

		runes = []
		units = []
		equips = []
		mats = []

		luck_drops = []

		enemy_drops = []
		crest_drops = []
		crest_drops_boss = None


		enemy_drops = self.drops_enemy(body)

		luck_drops = body['result']['quest']['fortune_drop_list']

		crest_drops_boss = body['result']['quest']['rune']


		print('player')
		for i in enemy_drops:
			if i['drop_type'] == 28:
				first_three = str(i['drop_id'])[:3]

				last_three = str(i['drop_id'])[-3:]        
				print('lvl {1} {0}'.format(crest_type[int(first_three)], crest_level[last_three]))
			else:
				print("{} drop_id - {} x{}".format(drop_types[i['drop_type']], i['drop_id'], i['value']))
		print("\n")

		print('luck')
		for i in luck_drops:
			if i['drop_type'] == 28:
				first_three = str(i['drop_id'])[:3]

				last_three = str(i['drop_id'])[-3:]           
				print('lvl {1} {0}'.format(crest_type[int(first_three)], crest_level[last_three]))                
			else:
				print("{} drop_id - {} x{}".format(drop_types[i['drop_type']], i['drop_id'], i['value']))
		print("\n")

		if crest_drops_boss:
			print('crest')
			first_three = str(crest_drops_boss['rune_id'])[:3]

			last_three = str(crest_drops_boss['rune_id'])[-3:]
			print('lvl {1} {0}'.format(crest_type[int(first_three)], crest_level[last_three]))
			print('\n')


	def request(self, flow):
		if flow.request.host == 'g-api.grandsummoners.com':
			if flow.request.path == '/app/rune_equipment':
				if self.hack:
					req_payload = json.loads(flow.request.content)
					enc_req_body = req_payload['body']
					req_body = json.loads(self.c.decrypt(enc_req_body, self.enc_key))
					if 'consume_id' in req_body:
						req_body['consume_id'] = 70039800
						re_enc_content = self.c.encrypt(req_body, self.enc_key)
						re_encoded_body = re_enc_content.decode('utf-8')
						req_payload['body'] = re_encoded_body
						modified_payload = json.dumps(req_payload)

						flow.request.content = modified_payload.encode('utf-8')

	def response(self, flow):
		if flow.request.host == 'g-api.grandsummoners.com':
			if flow.request.path == '/app/login':
				resp_payload = json.loads(flow.response.content)
				enc_body = resp_payload['body']

				body = json.loads(self.c.decrypt(enc_body, self.default_key))

				self.enc_key = base64.b64encode(body['encryption_key'].encode('utf-8'))


			else:
				try:
					resp_payload = json.loads(flow.response.content)
					enc_body = resp_payload['body']
					
					req_payload = json.loads(flow.request.content)
					enc_req_body = req_payload['body'] 
					try:
						req_body = json.loads(self.c.decrypt(enc_req_body, self.enc_key))
					except:
						req_body = json.loads(self.c.decrypt(enc_req_body, self.default_key))

					body = json.loads(self.c.decrypt(enc_body, self.enc_key))

					self.enc_key = base64.b64encode(body['encryption_key'].encode('utf-8'))

					if flow.request.path == '/app/quest_start':
						self.drops(body)


				except Exception as e:
					ctx.log.error("something failed")
					raise(e)



def start():
	myaddon = DumpLoot()
	opts = options.Options(listen_host='0.0.0.0', listen_port=8080, confdir=os.path.expanduser('~/.mitmproxy'), ignore_hosts=['^(.+\.)?apple\.com:443$', '^(.+\.)?icloud\.com', '^(.+\.)?evernote\.com', '^(.+\.)?.googleapis\.com'])
	pconf = proxy.config.ProxyConfig(opts)
	m = DumpMaster(opts)
	m.server = proxy.server.ProxyServer(pconf)
	m.addons.add(myaddon)

	try:
		m.run()
	except KeyboardInterrupt:
		m.shutdown()

start()