/** send update to number of buyers or sellers 
 * @param type : BUYER or SELLER
 * @param adjustment : 1 or -1
*/
sendUpdateSubjectCount(type, adjustment){
    app.cancelModal = false;
    app.working = true;
    app.sendMessage("update_subject_count", {"sessionID" : app.sessionID,
                                                "current_visible_period" : app.current_visible_period,
                                                "type" : type,
                                                "adjustment" : adjustment});
},

/** send update to number of periods
 * @param adjustment : 1 or -1
*/
sendUpdatePeriodCount(adjustment){
    app.cancelModal = false;
    app.working = true;
    app.sendMessage("update_period_count", {"sessionID" : app.sessionID,
                                            "adjustment" : adjustment});
},

/** send update to number of periods
*/
sendUpdateValuecost(){
    
    app.working = true;
    app.sendMessage("update_valuecost", {"sessionID" : app.sessionID,
                                         "id" : app.current_valuecost.id,
                                         "formData" :app.current_valuecost ,});
},

/** take update valuecost
 * @param messageData {json} result of update, either sucess or fail with errors
*/
takeUpdateValuecost(messageData){
    app.cancelModal=false;
    app.clearMainFormErrors();

    if(messageData.status.value == "success")
    {
        app.takeGetSession(messageData);       
        app.valuecostModal.hide();    
    } 
    else
    {
        app.cancelModal=true;                           
        app.displayErrors(messageData.status.errors);
    } 
},

/** update the current visible period
 * @param adjustment : 1 or -1
*/
updateCurrentPeriod(adjustment){
    
    if(adjustment == 1)
    {
        if(app.current_visible_period < app.session.parameter_set.number_of_periods)
        {
            app.current_visible_period += 1;
        }
    }
    else
    {
        if(app.current_visible_period > 1)
        {
            app.current_visible_period -= 1;
        }
    }

    Vue.nextTick(app.update_sdgraph_canvas());

},

/** shift the values or costs in the current period from one buyer or seller to the next
 * @param valueOrCost : 'value' or 'cost'
 * @param valueOrCost : 'up' or 'down'
*/
shiftValueOrCost(valueOrCost, direction){
    app.working = true;
    app.sendMessage("shift_value_or_cost", {"sessionID" : app.sessionID,
                                            "currentPeriod" : app.current_visible_period,
                                            "valueOrCost" : valueOrCost,
                                            "direction" : direction,});
},

/** shift the values or costs in the current period from one buyer or seller to the next
 * @param valueOrCost : 'value' or 'cost'
 * @param valueOrCost : 'up' or 'down'
*/
addToValueOrCost(valueOrCost){
    app.working = true;
    amount = 0;
    if (valueOrCost == 'value')
        amount = app.add_to_value_amount;
    else
        amount = app.add_to_cost_amount;

    app.sendMessage("add_to_all_values_or_costs", {"sessionID" : app.sessionID,
                                            "currentPeriod" : app.current_visible_period,
                                            "valueOrCost" : valueOrCost,
                                            "amount" : amount,});
},

/** copy values or costs from pervious period
 * @param valueOrCost : 'value' or 'cost'
 * @param valueOrCost : 'up' or 'down'
*/
    copyValueOrCost(valueOrCost){
    app.working = true;
    app.sendMessage("copy_value_or_cost", {"sessionID" : app.sessionID,
                                            "currentPeriod" : app.current_visible_period,
                                            "valueOrCost" : valueOrCost});
},

/** send update to number of periods
*/
sendUpdatePeriod(){
    
    app.working = true;
    app.sendMessage("update_period", {"sessionID" : app.sessionID,
                                      "periodID" : app.session.parameter_set.periods[app.current_visible_period-1].id,
                                      "formData" : app.session.parameter_set.periods[app.current_visible_period-1],});
},

/** take update period
 * @param messageData {json} result of update, either sucess or fail with errors
*/
takeUpdatePeriod(messageData){
    app.cancelModal=false;
    app.clearMainFormErrors();

    if(messageData.status.value == "success")
    {
        app.takeGetSession(messageData);       
        app.editPeriodModal.hide();    
    } 
    else
    {
        app.cancelModal=true;                           
        app.displayErrors(messageData.status.errors);
    } 
},

/** copy parameters from another period
*/
sendImportParameters(){
    
    app.working = true;
    app.sendMessage("import_parameters", {"sessionID" : app.sessionID,
                                          "formData" : {session:app.import_parameters_session},});
},

/** show parameters copied from another period 
*/
takeImportParameters(){
    //app.cancelModal=false;
    //app.clearMainFormErrors();

    if(messageData.status.status == "success")
    {
        app.current_visible_period = 1;
        app.takeGetSession(messageData);       
        app.import_parameters_message = messageData.status.message;
    } 
    else
    {
        app.import_parameters_message = messageData.status.message;
    } 
},

/** send request to download parameters to a file 
*/
sendDownloadParameters(){
    
    app.working = true;
    app.sendMessage("download_parameters", {"sessionID" : app.sessionID,});
},

/** download parameter set into a file 
 @param messageData {json} result of file request, either sucess or fail with errors
*/
takeDownloadParameters(messageData){

    if(messageData.status == "success")
    {                  
        console.log(messageData.parameter_set);

        var downloadLink = document.createElement("a");
        var jsonse = JSON.stringify(messageData.parameter_set);
        var blob = new Blob([jsonse], {type: "application/json"});
        var url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = "Double_Auction_Session_" + app.session.id + "_Parameter_Set.json";

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);                     
    } 

    app.working = false;
},

/**upload a parameter set file
*/
uploadParameterset:function(){  

    let formData = new FormData();
    formData.append('file', app.upload_file);

    axios.post('/staff-session/{{id}}/', formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                    }
                } 
            )
            .then(function (response) {     

                app.uploadParametersetMessaage = response.data.message.message;
                app.session = response.data.session;
                app.uploadParametersetButtonText= 'Upload <i class="fas fa-upload"></i>';
                Vue.nextTick(app.update_sdgraph_canvas());

            })
            .catch(function (error) {
                console.log(error);
                app.searching=false;
            });                        
},

//direct upload button click
uploadAction:function(){
    if(app.upload_file == null)
        return;

    app.uploadParametersetMessaage = "";
    app.uploadParametersetButtonText = '<i class="fas fa-spinner fa-spin"></i>';

    if(app.upload_mode == "parameters")
    {
        this.uploadParameterset();
    }
    else
    {
        
    }

},

handleFileUpload:function(){
    app.upload_file = this.$refs.file.files[0];
    app.upload_file_name = app.upload_file.name;
},

/** show upload parameters modal
*/
showUploadParameters:function(upload_mode){
    app.upload_mode = upload_mode;
    app.uploadParametersetMessaage = "";

    app.parameterSetModal.toggle();
},

/**hide upload parameters modal
*/
hideUploadParameters:function(){
},

/** show edit valuecost modal
*/
showEditValuecost:function(value_cost, type){
    app.clearMainFormErrors();
    app.cancelModal=true;
    app.sessionBeforeEdit = Object.assign({}, app.session);

    app.current_valuecost = Object.assign({}, value_cost);

    if(type == "value")
    {
        app.valuecost_modal_label = "Edit value";
    }
    else
    {
        app.valuecost_modal_label = "Edit cost";
    }

    app.valuecostModal.toggle();
},

/** hide edit valuecost modal
*/
hideEditValuecost:function(){
    if(app.cancelModal)
    {
        Object.assign(app.session, app.sessionBeforeEdit);
        app.sessionBeforeEdit=null;
    }
},

/** show edit session modal
*/
showEditSession:function(){
    app.clearMainFormErrors();
    app.cancelModal=true;
    app.sessionBeforeEdit = Object.assign({}, app.session);
    
    app.editSessionModal.toggle();
},

/** hide edit session modal
*/
hideEditSession:function(){
    if(app.cancelModal)
    {
        Object.assign(app.session, app.sessionBeforeEdit);
        app.sessionBeforeEdit=null;
    }
},

/** show edit session modal
*/
showEditPeriod:function(){
    app.clearMainFormErrors();
    app.cancelModal=true;
    app.periodBeforeEdit = Object.assign({}, app.session.parameter_set.periods[app.current_visible_period-1]);

    app.editPeriodModal.toggle();
},

/** hide edit session modal
*/
hideEditPeriod:function(){
    if(app.cancelModal)
    {
        Object.assign(app.session.parameter_set.periods[app.current_visible_period-1], app.periodBeforeEdit);
        app.periodBeforeEdit=null;
    }
},

/** show edit session modal
*/
showImportParameters:function(){

    app.importParametersModal.toggle();
},

/** hide edit session modal
*/
hideImportParameters:function(){
    
},
        
       

  