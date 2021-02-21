
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {chatSocket:"",
                    testMessage:"test"}},
    methods: {
        takeMessage(data) {
           console.log(data);
        },

        sendMessage(messageType,messageText) {

            app.$data.chatSocket.send(JSON.stringify({
                    'messageType': messageType,
                    'messageText': messageText,
                }));
        }
    },

    mounted(){
        
    },

}).mount('#app');

//web sockets
doWebSockets = function()
{
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        app.$data.chatSocket = new WebSocket(            
                               ws_scheme + '://' + window.location.host +
                               '/ws/subject/1/');        
    
        app.$data.chatSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);                       
            app.takeMessage(data);
        };
    
        app.$data.chatSocket.onclose = function(e) {
            // console.error('Socket closed unexpectedly.');
            // app.$data.reconnecting=true;
            // window.setTimeout(doWebSockets(), app.randomNumber(500,1500));            
        }; 

        app.$data.chatSocket.onopen = function(e) {
            console.log('Socket connected.');     
            // app.$data.reconnecting=false;   
            // app.$data.sendingMessage=false;
            // app.sendMessage("",-1,"setup");                        
        };                
};

doWebSockets();
