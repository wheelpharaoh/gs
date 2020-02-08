'use strict';

//const fs = require('frida-fs');

Interceptor.attach(Module.findExportByName(null, "fopen"), {
  onEnter: function(args) {
    this.flag = false;
    var filename = Memory.readCString(ptr(args[0]));
    console.log('filename =', filename);
    //if (filename.endsWith(".db")) {
    if (filename.endsWith(".dat")) {
      this.flag = true;
      var backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join("\n\t");
      console.warn("file name [ " + Memory.readCString(ptr(args[0])) + " ]\nBacktrace:" + backtrace);
    }

  },
  onLeave: function(retval) {
    if (this.flag) // passed from onEnter
      console.warn("\nretval: " + retval);
  }
});

Interceptor.attach(Module.findExportByName(null, 'remove'), {
  onEnter(args) {
    /*
     * This code block will be called before the real 'unlink'
     * method. Allowing us to change its behaviour.
     */
    const fileName = Memory.readUtf8String(args[0]);
    console.log('delete: ' + fileName);
  }
});