
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

           console.log(data);

           messageType = data.message.messageType;
           messageData = data.message.messageData;

            switch(messageType) {
                case "upload_parameters":
                    app.takeUploadParameters(messageData);
                    break;
                case "":
                    
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

        sendUploadParameters(){
            app.$data.parameter_upload_status="";
            //app.$data.working=true;

            app.sendMessage("upload_parameters",{ini_text : app.$data.parameters_text});
            
        },

        takeUploadParameters(messageData){
   
        },

       
        
    },

    mounted(){
        
    },

}).mount('#app');

{%include "js/web_sockets.js"%}
