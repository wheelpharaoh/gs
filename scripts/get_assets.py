import asyncio
from builtins import FileExistsError
from contextlib import closing
from hashlib import md5
import io
import json
import logging
import os
import zipfile

from aiofile import AIOFile, Reader
from aiohttp import ClientSession, ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN)


cdn = 'https://dlkrtysgey8gg.cloudfront.net/resource/dlc_1579226984' #

skipped = 0
downloaded = 0


# async def get_file_md5(file_name):
def get_file_md5(file_name):
	#Note that sometimes you won't be able to fit the whole file in memory. In that case, you'll have to read chunks of 4096 bytes sequentially and feed them to the Md5 functio
	# Open,close, read file and calculate MD5 on its contents 
	hash_md5 = md5()
	#async with AIOFile(file_name, 'rb') as file_to_check:
	with open(file_name, 'rb') as file_to_check:
		#data = file_to_check.read() # assume-whole-file-into-memory
		for chunk in iter(lambda: file_to_check.read(4096), b""): # synchronous
		#reader = Reader(file_to_check, chunk_size=4096 * 14)
		#async for chunk in reader:
			hash_md5.update(chunk)

		md5_returned = hash_md5.hexdigest()
		logger.debug('md5_returned {0}'.format(md5_returned))
		return md5_returned

#async def is_new(asset, asset_md5):
def is_new(asset, asset_md5):
	if os.path.exists(asset):
		#dest_md5 = await get_file_md5(asset)
		dest_md5 = get_file_md5(asset)
		logger.debug('SRC md5:{0}, DEST md5:{1}'.format(asset_md5, dest_md5))
		if asset_md5 == dest_md5:
			logger.debug('OLD file.')
			return False
		else:
			logger.debug('NEW(2) file.')
			return True
	else:
		logger.debug('NEW(1) file.')
		return True

async def fetch(session, url, dlc_dir, asset):
	global skipped, downloaded
	local_download_path = os.path.join(dlc_dir, asset[0])
	#if await is_new(local_download_path, asset[1]):
	if is_new(local_download_path, asset[1]):

		data = None
		while data is None:
			try:
				async with session.get(url) as response:
					response.raise_for_status()
					data = await response.read()
			except asyncio.TimeoutError:
				logger.warn('timed out on: {0}'.format(asset))
				# sleep a little and try again
				await asyncio.sleep(1)	

		async with AIOFile(local_download_path, 'wb') as afp:
			await afp.write(data)
			await afp.fsync()
			downloaded += 1
			logger.info('done %s', asset)
		return data
	else:
		skipped += 1
		logger.info('skipping: {0}'.format(asset))
		return None


async def fetch_assets(assets, dlc_dir, sem):
	tasks = []
	
	async with ClientSession() as session:
		for i in list(assets):
			url = '{0}/{1}'.format(cdn, i[0])
			logger.info('asset URL: {0}'.format(url))
			task = asyncio.ensure_future(bound_fetch(sem, session, url, dlc_dir, i))
			tasks.append(task)
		responses = await asyncio.gather(*tasks)

def prepare_paths(assets_path, version, assets):
	dlc_dir = os.path.join(assets_path, version)
	dlc_dir = assets_path
	
	try:
		os.mkdir(dlc_dir)
		logger.debug('creating {0}'.format(dlc_dir))
	except FileExistsError:
		pass

	for asset in assets:
		folder = os.path.join(dlc_dir, os.path.dirname(asset[0]))
		try:
			os.makedirs(folder)
			logger.debug('creating {0}'.format(dlc_dir))
		except FileExistsError:
			pass
	return dlc_dir 

async def bound_fetch(sem, session, url, dlc_dir, asset):
	# getter funcion with semaphor
	async with sem:
		await fetch(session, url, dlc_dir, asset)

async def fetch_file(url):
	async with ClientSession() as session:
		async with session.get(url) as response:
			response.raise_for_status()
			data = await response.read()

			return data

async def get_zip_data(zipfile_url):
	data = await fetch_file(zipfile_url)
	zip_data = zipfile.ZipFile(io.BytesIO(data))
	return zip_data


async def get_manifest_data(zip_data):
	for name in zip_data.namelist():
		logger.debug(name)
	manifest = zip_data.open('initial_main.manifest.temp')
	manifest_data = json.loads(manifest.read())
	return manifest_data


async def main():

	assets_path = os.path.expanduser("~/dev/gs-assets")
	manifest = "https://dlkrtysgey8gg.cloudfront.net/resource/dlc_1579226984/project.manifest.zip"
	assets = {}
	version = ''

	sem = asyncio.Semaphore(1800)


	zd = await get_zip_data(manifest)
	md = await get_manifest_data(zd)

	version = md['version']
	print('version: {0}'.format(version))
	assets = md['assets']

	asset_tuples = [(k, v['md5'])  for k,v in assets.items()]
	dlc_dir = prepare_paths(assets_path, version, asset_tuples)

	await fetch_assets(asset_tuples, dlc_dir, sem)

	print('skipped: {0}'.format(skipped))
	print('downloaded: {0}'.format(downloaded))

if __name__ == '__main__':
	
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())



#version: 20191213175103
  #logger.warn('timed out on: {0}'.format(asset))
#WARNING:__main__:timed out on: ('unit/100732311idle.zip', '11cc249468a73b667e7280d997ace65d')
#skipped: 7207
#downloaded: 2469
#[Finished in 315.9s]



