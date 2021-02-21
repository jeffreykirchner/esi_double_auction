
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {chatSocket : "",
                    testMessage : "test",
                    reconnecting : true,
                    sessions : [],
                    createSessionButtonText : 'Create Session <i class="fas fa-plus"></i>',
                    dateSortButtonText: 'Date <i class="fas fa-sort"></i>',
                    titleSortButtonText: 'Title <i class="fas fa-sort"></i>',
                }},
    methods: {
        takeMessage(data) {
           //process socket message from server

           console.log(data);

           messageType = data.message.messageType;
           messageData = data.message.messageData;

           switch(messageType) {
            case "create_session":
                app.takeCreateSession(messageData);
                break;
            case "get_sessions":
                app.takeGetSessions(messageData);
                break;
            
          }
        },

        sendMessage(messageType,messageText) {
            //send socket message to server

            app.$data.chatSocket.send(JSON.stringify({
                    'messageType': messageType,
                    'messageText': messageText,
                }));
        },

        sendCreateSession(){
            //send create new session
            app.$data.createSessionButtonText ='<i class="fas fa-spinner fa-spin"></i>';
            app.sendMessage("create_session",{});
        },

        takeCreateSession(messageData){
            //take create new session
            app.$data.createSessionButtonText ='Create Session <i class="fas fa-plus"></i>';
            app.takeGetSessions(messageData);
        },

        sendGetSessions(){
            //get list of sessions
            app.sendMessage("get_sessions",{});
        },

        takeGetSessions(messageData){
            //process list of sessions

            app.sessions = messageData.sessions;
        },
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
                               '/ws/sessionList/{{parameters.channel_key}}/');        
    
        app.$data.chatSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);                       
            app.takeMessage(data);
        };
    
        app.$data.chatSocket.onclose = function(e) {
            console.error('Socket closed, trying to connect ... ');
            //app.$data.reconnecting=true;
            //window.setTimeout(doWebSockets(), app.randomNumber(500,1500));            
        }; 

        app.$data.chatSocket.onopen = function(e) {
            console.log('Socket connected.');     
            app.$data.reconnecting=false;   
            // app.$data.sendingMessage=false;
            app.sendGetSessions();                        
        };                
};

doWebSockets();
