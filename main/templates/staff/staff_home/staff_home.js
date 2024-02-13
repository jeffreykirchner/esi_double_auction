
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {chatSocket : "",
                    helpText : "Loading ...",
                    reconnecting : true,
                    working : false,
                    sessions : [],
                    sessions_full_admin : [],
                    sessions_full_admin_visible : false,
                    user_id : {{request.user.id}},
                }},
    methods: {
        handleSocketConnected(){
            //fire when socket connects
            Vue.nextTick(() => {
                app.sendGetSessions();
                app.sendGetSessions();
            });
        },

        takeMessage(data) {
           //process socket message from server

           //console.log(data);

           messageType = data.message.messageType;
           messageData = data.message.messageData;

            switch(messageType) {
                case "help_doc":
                    app.takeLoadHelpDoc(messageData);
                    break;
                case "create_session":
                    app.takeCreateSession(messageData);
                    break;
                case "get_sessions":
                    app.takeGetSessions(messageData);
                    break;
                case "get_sessions_admin":
                    app.takeGetSessionsAdmin(messageData);
                    break;
    
            }

            app.working = false;
        },

        sendMessage(messageType,messageText) {
            //send socket message to server

            app.chatSocket.send(JSON.stringify({
                    'messageType': messageType,
                    'messageText': messageText,
                }));
        },

        sendGetSessions(){
            //get list of sessions
            app.sendMessage("get_sessions",{});
        },

        takeGetSessions(messageData){
            //process list of sessions created by user
            app.sessions = messageData.sessions;           

            if(app.sessions_full_admin_visible)
            {
                app.sendGetSessionsAdmin()
            }
        },

        sendDeleteSession(id){
            if (!confirm('Delete session? This is not reversible.')) {
                return;
            }

            //delete specified session
            app.working = true;
            app.sendMessage("delete_session",{"id" : id});
        },

        {%include "staff/staff_home/sessions_card_full_admin.js"%}
        {%include "staff/staff_home/sessions_card.js"%}
        {%include "js/help_doc.js"%}
        
    },

    mounted(){
        
    },

}).mount('#app');

{%include "js/web_sockets.js"%}
