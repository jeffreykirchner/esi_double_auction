/**start the experiment
*/
start_experiment(){
    app.working = true;
    app.sendMessage("start_experiment", {"sessionID" : app.sessionID});
},

/** take start experiment response
 * @param messageData {json}
*/
takeStartExperiment(messageData){
    app.takeGetSession(messageData);
    app.current_visible_period = 1;
    app.show_bids_offers_graph = true;
    app.show_supply_demand_graph = false;
    app.show_equilibrium_price_graph = false;
    app.show_trade_line_graph = false;
    app.show_gains_from_trade_graph = false;
},

/**reset experiment, remove all bids, asks and trades
*/
reset_experiment(){
    if (!confirm('Reset session? All bids and offers will be removed.')) {
        return;
    }

    app.working = true;
    app.sendMessage("reset_experiment", {"sessionID" : app.sessionID});
},

/** take reset experiment response
 * @param messageData {json}
*/
takeResetExperiment(messageData){
    app.takeGetSession(messageData);
    app.current_visible_period = 1;
    app.bid_offer_message = "";
},

/**advance to next period
*/
next_period(){
    if (app.session.current_period == app.session.parameter_set.number_of_periods)
    {
        if (!confirm('Complete experiment?')) {
            return;
        }
    }
    else
    {
        if (!confirm('Advance to next period?')) {
            return;
        }
    }

    app.working = true;
    app.sendMessage("next_period", {"sessionID" : app.sessionID});
},

/** take next period response
 * @param messageData {json}
*/
takeNextPeriod(messageData){
    
    app.session.current_period = messageData.data.current_period;
    app.session.finished = messageData.data.finished;
    
    app.current_visible_period = app.session.current_period;
    app.bid_offer_message = "";

    app.updateMoveOnButtonText();

    if(app.session.finished)
    {
        app.current_visible_period = 1;
        app.session.current_period = 1;
    }
},