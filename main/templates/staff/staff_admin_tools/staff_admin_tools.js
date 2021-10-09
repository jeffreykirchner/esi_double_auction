
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {chatSocket : "",
                    reconnecting : true,
                    working : false,
                    parameter_upload_status : "",
                    datafile_upload_status : "",
                    parameters_text : "",
                    datafile_text : "",
                }},
    methods: {
        handleSocketConnected(){
            //fire when socket connects
           
        },

        takeMessage(data) {
           //process socket message from server

           //console.log(data);

           messageType = data.message.messageType;
           messageData = data.message.messageData;

            switch(messageType) {
                case "upload_parameters":
                    app.takeUploadParameters(messageData);
                    break;
                case "upload_datafile":
                    app.takeUploadDatafile(messageData);
                    break;
    
            }

            app.working = false;
        },

        sendMessage(messageType,messageText) {
            //send socket message to server

            app.$data.chatSocket.send(JSON.stringify({
                    'messageType': messageType,
                    'messageText': messageText,
                }));
        },

        /**upload legacy parameter file
        */
        sendUploadParameters(){
            app.$data.parameter_upload_status="";
            app.$data.working=true;

            app.sendMessage("upload_parameters",{ini_text : app.$data.parameters_text});
            
        },

        /**take result of parameter file upload
        */
        takeUploadParameters(messageData){

            result = messageData.result;
            
            if(result.status == "success")
            {
                app.$data.parameter_upload_status="Parameters have been uploaded: <a href='/staff-session/" + result.message.session + "/'>View Session</a>";
                app.$data.parameters_text = "";
            }
            else
            {
                app.$data.parameter_upload_status="Invalid parameter file"
            }            
        }, 

        /**upload legacy parameter file
        */
        sendUploadDatafile(){
            app.$data.datafile_upload_status="";
            app.$data.working=true;

            app.sendMessage("upload_datafile", {ini_text : app.$data.datafile_text});
            
        },

        /**take result of parameter file upload
        */
        takeUploadDatafile(messageData){

            result = messageData.result;
            
            if(result.status == "success")
            {
                app.$data.datafile_upload_status="Datafile has been uploaded: <a href='/staff-session/" + result.message.session + "/'>View Session</a>";
                app.$data.datafile_text = "";
            }
            else
            {
                app.$data.datafile_upload_status="Invalid data file"
            }            
        },
    },

    mounted(){
        
    },

}).mount('#app');

{%include "js/web_sockets.js"%}
