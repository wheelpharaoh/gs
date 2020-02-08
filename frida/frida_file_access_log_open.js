Interceptor.attach(ObjC.classes.NSFileManager['- fileExistsAtPath:'].implementation, {
    onEnter: function (args) {
    	var opened_file = ObjC.Object(args[2]).toString();
    	//if (opened_file.includes('.db')) {
    	if (opened_file.includes('.dat')) {
    		this.flag = true
	        console.warn('open' , opened_file); //open /var/mobile/Containers/Data/Application/D1A33E6C-B8CA-4294-8DBB-C82FAE72DD69/Library/Caches/dlc/db/encrypted_app.db
	     	var backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join("\n\t");
      		console.log("arg2 [ " + opened_file + " ]\nBacktrace:" + backtrace);
      	}
   
    },
  	onLeave: function(retval) {
        if (this.flag) // passed from onEnter
      		console.warn("\nretval: " + retval);
  }
});


