var requestObject = {
    formRegex: {
                 'name':/^([a-zA-Z0-9])+$/,
                 'email':/^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/,
                 'contact':/^([0-9]){10}$/,
                 'dateformat':/^([0][0-9]{1}|[1][0-9]{1})\/([0,1,2][0-9]{1}|[3][0-1]{1})\/([19,20]{1}[0-9]{2})$/
    },
    formMessage:{
        error:{
            'NotFound': 'Device not found'
        },
        success:{
            'success':'Added your device'
        }
    },
    appURL:{
        Module:{
             Search:'/service/module/search',
             Add:'',
             Modify:'',
             Delete:'',
             TestModule:'/service/module/testModule'
        }	
    },
    methodType:{
        POST:'post',
        GET:'get'
    },
    applyRegex:function(regexName, value){
          return this.formRegex[regexName].test(value)
    },
    call:function(methodType, appurl, jsonData, callback){
        var returnPayload="";
        $.ajax({
               url: appurl,
               dataType: 'json',
               type: methodType,
               contentType: 'application/json',
               data: jsonData,
               async : false,
               success: function( data, textStatus, jQxhr ){
                   if(data.error !== null && data.error !== undefined){
                       alert(data.error);
                       requestObject.responseData="";
                       return false;
                   }  else{
                      // alert(data.success);
                       requestObject.responseData =data;
                       callback(requestObject.responseData)
                       return true;
                }
               },
               error: function( jqXhr, textStatus, errorThrown ){
                   if(jqXhr.status === 400){
                       var msg;
                       $.each(jqXhr.responseJSON.error, function(index,val){
                           msg=val+"\n";
                       })
                       alert(jqXhr.status + ":"+ msg);
                   } else{
                       alert(jqXhr.status + ": Please contact system administrator");
                   }
                   
                   requestObject.responseData=null;
               }
           });
        return requestObject.responseData;
    }
};
