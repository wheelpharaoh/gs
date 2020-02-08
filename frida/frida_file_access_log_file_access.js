Interceptor.attach(ObjC.classes.NSFileManager['- fileExistsAtPath:'].implementation, {
    onEnter: function (args) {
        console.log('open' , ObjC.Object(args[2]).toString());
    }
});