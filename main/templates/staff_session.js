
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {chatSocket : "",
                    reconnecting : true,
                    working : false,
                    sessionID : {{session.id}},
                    session : {},
                    downloadParametersetButtonText:'Download <i class="fas fa-download"></i>',
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
                app.displayErrors(response.data.errors);
            } 
        },

        /** show edit session modal
        */
        showEditSession:function(){
            app.clearMainFormErrors();
            app.$data.cancelModal=true;
            app.$data.sessionBeforeEdit = Object.assign({}, app.$data.session);
            $('#editSessionModal').modal('show');                   
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

        /** clear form error messages
        */
        clearMainFormErrors:function(){
            
            for(var item in app.$data.session.parameterset)
            {
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }

            for(var item in app.$data.session)
            {
                $("#id_" + item).attr("class","form-control");
                $("#id_errors_" + item).remove();
            }

            s = app.$data.subject_form_ids;
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
    },

}).mount('#app');

{%include "js/web_sockets.js"%}

  