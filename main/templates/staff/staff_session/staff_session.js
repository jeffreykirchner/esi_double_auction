
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
                        current_period : 1,
                        started : false,
                        session_periods : [{trade_list : []},
                                          ],
                        parameter_set : {
                            number_of_buyers : 0,
                            number_of_sellers : 0,
                            number_of_periods : 0,
                            periods : [ {
                                period_number : 1,
                                price_cap : "0.00",
                                y_scale_max: "",
                                x_scale_max: "",
                                price_cap_enabled : "False",
                                sellers : [],
                                buyers : [],
                                demand : [],
                                supply : [],
                             }]
                         },
                     },
                    current_visible_period : 1,                //period visible on screen
                    downloadParametersetButtonText:'Download <i class="fas fa-download"></i>',
                    valuecost_modal_label:'Edit Value or Cost',
                    current_valuecost:{                       //json attached to value/cost edit modal
                        id:0,
                        valuecost:0,
                        enabled:false,
                    },
                    valuecost_form_ids: {{valuecost_form_ids|safe}},
                    period_form_ids: {{period_form_ids|safe}},
                    upload_file: null,
                    upload_file_name:'Choose File',
                    uploadParametersetButtonText:'Upload  <i class="fas fa-upload"></i>',
                    uploadParametersetMessaage:'',
                    show_parameters:false,
                    bid_offer_id:"",
                    bid_offer_amount:"",
                    bid_offer_message:"",              //message shown in input card under bid/offer input
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
                case "download_parameters":
                    app.takeDownloadParameters(messageData);
                    break;
                case "start_experiment":
                    app.takeStartExperiment(messageData);
                    break;
                case "reset_experiment":
                    app.takeResetExperiment(messageData);
                    break;
                case "next_period":
                    app.takeNextExperiment(messageData);
                    break;   
                case "submit_bid_offer":
                    app.take_submit_bid_offer(messageData); 
                    break;       
                case "undo_bid_offer":
                    app.take_undo_bid_offer(messageData);
                    break;
            }

            app.working = false;
            Vue.nextTick(app.update_sdgraph_canvas());
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
            
            app.$data.session = messageData.session;

            if(app.$data.session.started)
            {
                app.$data.show_parameters = false;
            }
            else
            {
                app.$data.show_parameters = true;
            }
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
            app.$data.working = true;
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

        {%include "staff/staff_session/parameters_card.js"%}
        {%include "staff/staff_session/graph_card.js"%}
        {%include "staff/staff_session/control_card.js"%}
        {%include "staff/staff_session/input_card.js"%}
        
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
        $('#importParametersModal').on("hidden.bs.modal", this.hideImportParameters); 
        $('#parameterSetModal').on("hidden.bs.modal", this.hideUploadParameters);
    },

}).mount('#app');

{%include "js/web_sockets.js"%}

  