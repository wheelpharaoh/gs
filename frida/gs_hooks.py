import codecs
import frida
from time import sleep

#session = frida.get_usb_device().attach('Grand Summoners')

session = frida.get_usb_device().spawn("jp.goodsmile.grandsummonersglobal")
# frida -U --no-pause -f "jp.goodsmile.grandsummonersglobal" -l ./hooks.js

with codecs.open('./hooks.js', 'r', 'utf-8') as f:
    source = f.read()

script = session.create_script(source)
script.load()

#rpc = script.exports

#session.detach()