'use strict';

function memAddress(memBase, idaBase, idaAddr) {
    //console.log('memAddress:memBase: ' + memBase);
    //console.log('memAddress:idaBase: ' + idaBase);
    //console.log('memAddress:idaAddr: ' + idaAddr);

    var offset = ptr(idaAddr).sub(idaBase);
    //console.log('memAddress:offset: ' + offset);

    var result = ptr(memBase).add(offset);
    //console.log('memAddress:result: ' + result);
    return result;
}

function idaAddress(memBase, idaBase, memAddr) {
    var offset = ptr(memAddr).sub(memBase);
    var result = ptr(idaBase).add(offset);
    return result;
}

function getBaseAddress(executable) {
  var baseAddress = '';
  Process.enumerateModulesSync().forEach(
    function(mod) { 
      if (mod['name'] == executable)
        //console.log('getBaseAddress returning: ' + mod['base']);
        baseAddress = mod['base'];
    }
  );
  return baseAddress;
}

// Convert a byte array to a hex string
function bytesToHex(bytes) {
    for (var hex = [], i = 0; i < bytes.length; i++) {
        hex.push((bytes[i] >>> 4).toString(16));
        hex.push((bytes[i] & 0xF).toString(16));
    }
    return hex.join("");
}
 

var hopperBase = '0x100000000';
var process_name = "megamistrike";

var memBase = getBaseAddress(process_name);
//console.log('Mem Base: ' + memBase);

var sub_100223b9c = '0x100223b9c'; 
const sub_100223b9c_offset = memAddress(memBase, hopperBase, sub_100223b9c);
//console.log('sub_100223b9c offset: ' + sub_100223b9c_offset);

var sub_100223af8 = '0x100223af8'; 
const sub_100223af8_offset = memAddress(memBase, hopperBase, sub_100223af8);
//console.log('sub_100223af8 offset: ' + sub_100223af8_offset);



function replacer(key, value) {
  //console.log('key: ' + key);
  //console.log('val: ' + value);
  //console.log('val type: ' + typeof value);

  if (typeof value == 'string') {
    //console.log('this is string');
    try {
      console.log(Memory.readCString(ptr(value)));
      console.log(key + '-readByteArray: ');
      console.log(ptr(value).readPointer().readByteArray(128));
      return Memory.readCString(ptr(value));
    } catch (e) {
      return value;
    }
  } else {
    //console.log('this is NOT string');
    return value;
  }
}

function intercept_func(func_name) {
  console.log('split: ' + func_name.split('_'))
  var func_addr = '0x' + func_name.split('_')[1]; 
  const func_addr_offset = memAddress(memBase, hopperBase, func_addr);
  console.log('func: ' + func_name + ' offset: ' + func_addr_offset);


  Interceptor.attach(func_addr_offset, {
    onEnter: function(args) {

      console.log('[enter] Context information:');
      console.log('Context  : ' + JSON.stringify(this.context));
      console.log('parsed Context  : ' + JSON.stringify(JSON.parse(JSON.stringify(this.context)), replacer));
      console.log('Return   : ' + this.returnAddress);
      console.log('ThreadId : ' + this.threadId);
      console.log('Depth    : ' + this.depth);
      console.log('Errornr  : ' + this.err);

      this.flag = true;
      console.log('\nargs[0] addr: ' + args[0]);
      console.log('\nfunc_addr_offset args[0]: ' + args[0].readCString());
      //var keyDump = Memory.readByteArray(Memory.readPointer(args[0]), 32);
      //console.log('keydump: ' + new TextDecoder().decode(keyDump));      
      //console.log(Memory.readPointer(args[0]).readCString());
      //console.log(hexdump(args[0]));
      //console.log('readPointer: ' + Memory.readPointer(args[0]));
      console.log('\nargs[1] addr: ' + args[1]);
      console.log('\nfunc_addr_offset args[1]: ' + args[1].readCString());

      //var keyDump = Memory.readByteArray(Memory.readPointer(args[1]), 32);
      //console.log(new TextDecoder().decode(keyDump));
      //console.log(hexdump(keyDump, { offset: 0, length: 32, header: false, ansi: false }));;
      var backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join("\n\t");
      console.log("arg0 [ " + Memory.readCString(ptr(args[0])) + " ]\nBacktrace:" + backtrace);
    },
    onLeave: function(retval) {
      if (this.flag) // passed from onEnter
        console.log('[leave] Context information:');
        console.log('Context  : ' + JSON.stringify(this.context));
        console.log('parsed Context  : ' + JSON.stringify(JSON.parse(JSON.stringify(this.context)), replacer));        
        console.warn("\nretval: " + retval);
        console.warn("\nretval CString: " + retval.readCString());
    }
  });

}


intercept_func('loc_1003a3dc8'); 



