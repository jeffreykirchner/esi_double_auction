/**start the experiment
*/
start_experiment:function(){
    app.$data.working = true;
    app.sendMessage("start_experiment", {"sessionID" : app.$data.sessionID});
},

/** take start experiment response
 * @param messageData {json}
*/
takeStartExperiment(messageData){
    app.takeGetSession(messageData);
},

/**reset experiment, remove all bids, asks and trades
*/
reset_experiment:function(){
    app.$data.working = true;
    app.sendMessage("reset_experiment", {"sessionID" : app.$data.sessionID});
},

/** take reset experiment response
 * @param messageData {json}
*/
takeResetExperiment(messageData){
    app.takeGetSession(messageData);
},

/**advance to next period
*/
next_period:function(){
    app.$data.working = true;
    app.sendMessage("next_period", {"sessionID" : app.$data.sessionID});
},

/** take next period response
 * @param messageData {json}
*/
takeNextExperiment(messageData){
     
},