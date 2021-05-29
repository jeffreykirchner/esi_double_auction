
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {chatSocket : "",
                    reconnecting : true,
                    working : false,
                    sessionID : {{session.id}},
                    session : {
                        parameter_set : {
                            number_of_buyers : 0,
                            number_of_sellers : 0,
                            number_of_periods : 0,
                            periods : [ {
                                period_number : 1,
                                price_cap : "0.00",
                                price_cap_enabled : "False",
                                sellers : [],
                                buyers : [],
                             }]
                         },
                     },
                    current_period : 1,
                    downloadParametersetButtonText:'Download <i class="fas fa-download"></i>',
                    valuecost_modal_label:'Edit Value or Cost',
                    current_valuecost:{
                        id:0,
                        valuecost:0,
                        enabled:false,
                    },
                    valuecost_form_ids: {{valuecost_form_ids|safe}},
                    period_form_ids: {{period_form_ids|safe}},
                }},
    methods: {

        /** fire when websocket connects to server
        */
        handleSocketConnected(){            
            app.sendGetSession();
        },

        /** take websocket message from server
        *    @param data {json} incoming data from server, contains message and message type
        */
        takeMessage(data) {

           console.log(data);

           messageType = data.message.messageType;
           messageData = data.message.messageData;

            switch(messageType) {                
                case "get_session":
                    app.takeGetSession(messageData);
                    break;
                case "update_session":
                    app.takeUpdateSession(messageData);
                    break;
                case "update_valuecost":
                    app.takeUpdateValuecost(messageData);
                    break;
                case "update_period":
                    app.takeUpdatePeriod(messageData);
                    break;   
                case "import_parameters":
                    app.takeImportParameters(messageData);
                    break;  
                
            }

            app.working = false;
        },

        /** send websocket message to server
        *    @param messageType {string} type of message sent to server
        *    @param messageText {json} body of message being sent to server
        */
        sendMessage(messageType, messageText) {
            

            app.$data.chatSocket.send(JSON.stringify({
                    'messageType': messageType,
                    'messageText': messageText,
                }));
        },

        /** take create new session
        *    @param messageData {json} session day in json format
        */
        takeGetSession(messageData){
            
            app.$data.session = messageData.session
        },

        /** send winsock request to get session info
        */
        sendGetSession(){
            app.sendMessage("get_session",{"sessionID" : app.$data.sessionID});
        },

        /** send session update form   
        */
        sendUpdateSession(){
            app.$data.cancelModal = false;
            app.sendMessage("update_session",{"formData" : $("#sessionForm").serializeArray(),
                                              "sessionID" : app.$data.sessionID});
        },

        /** take update session reponse
         * @param messageData {json} result of update, either sucess or fail with errors
        */
        takeUpdateSession(messageData){
            app.clearMainFormErrors();

            if(messageData.status == "success")
            {
                app.takeGetSession(messageData);       
                $('#editSessionModal').modal('hide');    
            } 
            else
            {
                app.$data.cancelModal=true;                           
                app.displayErrors(messageData.errors);
            } 
        },

        /** send update to number of buyers or sellers 
         * @param type : BUYER or SELLER
         * @param adjustment : 1 or -1
        */
        sendUpdateSubjectCount(type, adjustment){
            app.$data.cancelModal = false;
            app.$data.working = true;
            app.sendMessage("update_subject_count", {"sessionID" : app.$data.sessionID,
                                                     "current_period" : app.$data.current_period,
                                                     "type" : type,
                                                     "adjustment" : adjustment});
        },

        /** send update to number of periods
         * @param adjustment : 1 or -1
        */
        sendUpdatePeriodCount(adjustment){
            app.$data.cancelModal = false;
            app.$data.working = true;
            app.sendMessage("update_period_count", {"sessionID" : app.$data.sessionID,
                                                    "adjustment" : adjustment});
        },

        /** send update to number of periods
        */
        sendUpdateValuecost(){
            
            app.$data.working = true;
            app.sendMessage("update_valuecost", {"sessionID" : app.$data.sessionID,
                                                 "id" : app.$data.current_valuecost.id,
                                                 "formData" : $("#valuecostForm").serializeArray(),});
        },

        /** take update valuecost
         * @param messageData {json} result of update, either sucess or fail with errors
        */
        takeUpdateValuecost(messageData){
            app.$data.cancelModal=false;
            app.clearMainFormErrors();

            if(messageData.status.value == "success")
            {
                app.takeGetSession(messageData);       
                $('#valuecostModal').modal('hide');    
            } 
            else
            {
                app.$data.cancelModal=true;                           
                app.displayErrors(messageData.errors);
            } 
        },

        /** update the current visible period
         * @param adjustment : 1 or -1
        */
        updateCurrentPeriod(adjustment){
            
            if(adjustment == 1)
            {
                if(app.$data.current_period < app.$data.session.parameter_set.number_of_periods)
                {
                    app.$data.current_period += 1;
                }
            }
            else
            {
                if(app.$data.current_period > 1)
                {
                    app.$data.current_period -= 1;
                }
            }

        },

        /** shift the values or costs in the current period from one buyer or seller to the next
         * @param valueOrCost : 'value' or 'cost'
         * @param valueOrCost : 'up' or 'down'
        */
        shiftValueOrCost(valueOrCost, direction){
            app.$data.working = true;
            app.sendMessage("shift_value_or_cost", {"sessionID" : app.$data.sessionID,
                                                    "currentPeriod" : app.$data.current_period,
                                                    "valueOrCost" : valueOrCost,
                                                    "direction" : direction,});
        },

        /** copy values or costs from pervious period
         * @param valueOrCost : 'value' or 'cost'
         * @param valueOrCost : 'up' or 'down'
        */
         copyValueOrCost(valueOrCost){
            app.$data.working = true;
            app.sendMessage("copy_value_or_cost", {"sessionID" : app.$data.sessionID,
                                                    "currentPeriod" : app.$data.current_period,
                                                    "valueOrCost" : valueOrCost});
        },

        /** send update to number of periods
        */
        sendUpdatePeriod(){
            
            app.$data.working = true;
            app.sendMessage("update_period", {"sessionID" : app.$data.sessionID,
                                              "periodID" : app.$data.session.parameter_set.periods[app.$data.current_period-1].id,
                                              "formData" : $("#periodForm").serializeArray(),});
        },

        /** take update valuecost
         * @param messageData {json} result of update, either sucess or fail with errors
        */
        takeUpdatePeriod(messageData){
            app.$data.cancelModal=false;
            app.clearMainFormErrors();

            if(messageData.status.value == "success")
            {
                app.takeGetSession(messageData);       
                $('#editPeriodModal').modal('hide');    
            } 
            else
            {
                app.$data.cancelModal=true;                           
                app.displayErrors(messageData.errors);
            } 
        },

        /** copy parameters from another period
        */
        sendImportParameters(){
            
            app.$data.working = true;
            app.sendMessage("import_parameters", {"sessionID" : app.$data.sessionID,
                                                  "formData" : $("#importParametersForm").serializeArray(),});
        },

        /** show parameters copied from another period 
        */
        takeImportParameters(){
            app.$data.cancelModal=false;
            app.clearMainFormErrors();

            if(messageData.status.value == "success")
            {
                app.takeGetSession(messageData);       
                $('#importParametersModal').modal('hide');    
            } 
            else
            {
                app.$data.cancelModal=true;                           
                app.displayErrors(messageData.errors);
            } 
        },

        /** upload parameter set from file
        */
        uploadParameterset:function(){  

            let formData = new FormData();
            formData.append('file', app.$data.upload_file);

            axios.post('/session/{{id}}/', formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                            }
                        } 
                    )
                    .then(function (response) {     

                        app.$data.uploadParametersetMessaage = response.data.message;

                        app.updateSession(response);

                        app.$data.uploadParametersetButtonText= 'Upload <i class="fas fa-upload"></i>';

                    })
                    .catch(function (error) {
                        console.log(error);
                        app.$data.searching=false;
                    });                        
        },

        /** show edit valuecost modal
        */
         showEditValuecost:function(value_cost, type){
            app.clearMainFormErrors();
            app.$data.cancelModal=true;
            app.$data.sessionBeforeEdit = Object.assign({}, app.$data.session);

            app.$data.current_valuecost = Object.assign({}, value_cost);

            if(type == "value")
            {
                app.$data.valuecost_modal_label = "Edit value";
            }
            else
            {
                app.$data.valuecost_modal_label = "Edit cost";
            }


            var myModal = new bootstrap.Modal(document.getElementById('valuecostModal'), {
                keyboard: false
              })

            myModal.toggle();
        },

        /** hide edit valuecost modal
        */
        hideEditValuecost:function(){
            if(app.$data.cancelModal)
            {
                Object.assign(app.$data.session, app.$data.sessionBeforeEdit);
                app.$data.sessionBeforeEdit=null;
            }
        },

        /** show edit session modal
        */
        showEditSession:function(){
            app.clearMainFormErrors();
            app.$data.cancelModal=true;
            app.$data.sessionBeforeEdit = Object.assign({}, app.$data.session);

            
            var myModal = new bootstrap.Modal(document.getElementById('editSessionModal'), {
                keyboard: false
              })

            myModal.toggle();
        },

        /** hide edit session modal
        */
        hideEditSession:function(){
            if(app.$data.cancelModal)
            {
                Object.assign(app.$data.session, app.$data.sessionBeforeEdit);
                app.$data.sessionBeforeEdit=null;
            }
        },

        /** show edit session modal
        */
        showEditPeriod:function(){
            app.clearMainFormErrors();
            app.$data.cancelModal=true;
            app.$data.periodBeforeEdit = Object.assign({}, app.$data.session.parameter_set.periods[app.$data.current_period-1]);

            var myModal = new bootstrap.Modal(document.getElementById('editPeriodModal'), {
                keyboard: false
                })

            myModal.toggle();
        },

        /** hide edit session modal
        */
        hideEditPeriod:function(){
            if(app.$data.cancelModal)
            {
                Object.assign(app.$data.session.parameter_set.periods[app.$data.current_period-1], app.$data.periodBeforeEdit);
                app.$data.periodBeforeEdit=null;
            }
        },

        /** show edit session modal
        */
        showImportParameters:function(){
           
            var myModal = new bootstrap.Modal(document.getElementById('importParametersModal'), {
                keyboard: false
                })

            myModal.toggle();
        },

        /** hide edit session modal
        */
        hideImportParameters:function(){
            
        },
        
        /** clear form error messages
        */
        clearMainFormErrors:function(){
            
            for(var item in app.$data.session)
            {
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }

            s = app.$data.valuecost_form_ids;
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }

            s = app.$data.period_form_ids;
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }
        },

        /** display form error messages
        */
        displayErrors:function(errors){
            for(var e in errors)
            {
                $("#id_" + e).attr("class","form-control is-invalid")
                var str='<span id=id_errors_'+ e +' class="text-danger">';
                
                for(var i in errors[e])
                {
                    str +=errors[e][i] + '<br>';
                }

                str+='</span>';
                $("#div_id_" + e).append(str); 

                var elmnt = document.getElementById("div_id_" + e);
                elmnt.scrollIntoView(); 

            }
        }, 

    },

    mounted(){
        $('#editSessionModal').on("hidden.bs.modal", this.hideEditSession); 
        $('#valuecostModal').on("hidden.bs.modal", this.hideEditValuecost); 
        $('#editPeriodModal').on("hidden.bs.modal", this.hideEditPeriod); 
        $('importParametersModal').on("hidden.bs.modal", this.hideImportParameters); 
    },

}).mount('#app');

{%include "js/web_sockets.js"%}

  