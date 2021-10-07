sendCreateSession(){
    //send create new session
    app.$data.working = true;
    app.$data.createSessionButtonText ='<i class="fas fa-spinner fa-spin"></i>';
    app.sendMessage("create_session",{});
},

takeCreateSession(messageData){
    //take create new session
    app.$data.working = false;
    app.$data.createSessionButtonText ='Create Session <i class="fas fa-plus"></i>';
    app.takeGetSessions(messageData);
},

//sort by title
sortByTitle:function(){

    app.$data.working = true;

    app.$data.sessions.sort(function(a, b) {
        a=a.title.trim().toLowerCase();
        b=b.title.trim().toLowerCase();
        return a < b ? -1 : a > b ? 1 : 0;
    });

    app.$data.working = false;
},

sortByDate:function(){

    app.$data.working = true;

    app.$data.sessions.sort(function(a, b) {
        return new Date(b.start_date) - new Date(a.start_date);

    });

    app.$data.working = false;
},