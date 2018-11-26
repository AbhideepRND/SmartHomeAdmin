(function($) {

    $.fn.macFilterModel = function(title,action,id) {
            $(this).fnOpenNormalDialog(title,action,id,285, 400);
    }

    $.fn.moduleModel = function(title,url,id) {

        if('Add Module' === title){
            console.log(id)
            urlString = requestObject.appURL.Module.Search+"?serial="+id+"&action=CONF"
            requestObject.call(requestObject.methodType.GET, urlString, null, function(response){
                if(response.errorCode == undefined || response.errorCode === null){

                    $('#DialogModel #moduleName').val(response['moduleName'])
                    $("#DialogModel").find('tbody').empty()
                    $.each(response.pinList, function(indx,data){

                   $("#DialogModel").find('tbody')
                        .append($('<tr>')
                            .append($('<td scope="row">').text(indx))
                            .append($('<td>').text(data.pinNo))
                            .append($('<td>').append($('<input>').attr('class', 'form-group').attr('type','text').attr('value',data.pinName)))
                            .append($('<td>').append($('<button>').attr('class', 'btn btn-info btn-sm test').attr('onclick','$(this).testModule(this)').text('Test')))
                            .append($('<td>').append($('<div>').attr('class', 'led-box').append('<div class="led-green"></div>')))
                        );
                    });
                     $.fn.fnOpenNormalDialog('DialogModel',title,url,id,450, 650, {
                                                                    "Yes": function () {
                     pinList = requestObject.responseData.pinList
                     $.each(pinList, function(index, value){
                        value.pinName = $($("#DialogModel input[class='form-group']")[index]).val()
                     })
                     pinList[1].pinName=null
                     requestObject.responseData.pinList = pinList;
                     requestObject.responseData.moduleName=$('#DialogModel #moduleName').val()
                     console.log(requestObject.responseData)
                     urlString = requestObject.appURL.Module.Add
                     requestObject.call(requestObject.methodType.POST, urlString, JSON.stringify(requestObject.responseData), function(response){$(this).dialog('close');})
                            },
                            "No": function () {$(this).dialog('close');}
                            });
                }else{
                    $("#AlertDialogModel").find('message').text(response.message)
                    $.fn.fnOpenNormalDialog('AlertDialogModel','Error Message',url,id,170, 300,{"Ok": function () {$(this).dialog('close');} });
                }
            })
        }
    }
    $.fn.testModule=function(obj){
        moduleData = new Array();
        moduleData.push(requestObject.responseData.pinList[$(obj).closest('tr')[0].rowIndex-1]);
        var json={};
        json['serial']=requestObject.responseData.serial;
        json['pinList']=moduleData;
        console.log(json)
        var payload = requestObject.call(requestObject.methodType.POST,
                    urlString = requestObject.appURL.Module.TestModule, JSON.stringify(json),function(response){
                if(response.errorCode == undefined || response.errorCode === null){

                    $("#DialogModel").find('tbody').empty()
                    $.each(response.pinList, function(indx,data){

                   $("#DialogModel").find('tbody')
                        .append($('<tr>')
                            .append($('<td scope="row">').text(indx))
                            .append($('<td>').text(data.pinNo))
                            .append($('<td>').append($('<input>').attr('class', 'form-group').attr('value',data.pinName)))
                            .append($('<td>').append($('<button>').attr('class', 'btn btn-info btn-sm test').attr('onclick','$(this).testModule(this)').text('Test')))
                            .append($('<td>').append($('<div>').attr('class', 'led-box').append('<div class="led-green"></div>')))
                        );
                    });
                }else{
                    $("#AlertDialogModel").find('message').text(response.message)
                    $.fn.fnOpenNormalDialog('AlertDialogModel','Error Message',url,id,170, 300,{"Ok": function () {$(this).dialog('close');} });
                }
            });
            console.log(payload);
    }


})(jQuery);