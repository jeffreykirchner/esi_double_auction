
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

            app.chatSocket.send(JSON.stringify({
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
        app.chatSocket = new WebSocket(            
                               ws_scheme + '://' + window.location.host +
                               '/ws/subject/1/');        
    
        app.chatSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);                       
            app.takeMessage(data);
        };
    
        app.chatSocket.onclose = function(e) {
            // console.error('Socket closed unexpectedly.');
            // app.reconnecting=true;
            // window.setTimeout(doWebSockets(), app.randomNumber(500,1500));            
        }; 

        app.chatSocket.onopen = function(e) {
            console.log('Socket connected.');     
            // app.reconnecting=false;   
            // app.sendingMessage=false;
            // app.sendMessage("",-1,"setup");                        
        };                
};

doWebSockets();
