# Extract exports & demangle it

import frida
import cxxfilt


session = frida.get_usb_device().attach("Grand Summoners")
script = session.create_script("""
	var exports = Module.enumerateExportsSync("megamistrike");
	for (var i = 0; i < exports.length; i++) {
		send(exports[i].name);
	}
		""");

def on_message(message, data):
	#print(message);
	print(message["payload"] + " - " + cxxfilt.demangle(message["payload"]));

script.on('message', on_message)
script.load()
