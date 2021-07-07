
/**submit bid or offer
*/
submit_bid_offer:function(){
    app.$data.working = true;
    app.sendMessage("submit_bid_offer",{"bid_offer_id" : app.$data.bid_offer_id,
                                        "bid_offer_amount" : app.$data.bid_offer_amount,
                                        "sessionID" : app.$data.sessionID});
},

/**take result of submiting bid or offer
 * @param messageData {json} result of bid or offer
*/
take_submit_bid_offer:function(messageData){
    
    if(messageData.result.status == "success")
    {

        if (messageData.result.bid_list != null)
        {
            app.$data.session.session_periods[app.$data.session.current_period-1].bid_list = messageData.result.bid_list;
            app.$data.session.session_periods[app.$data.session.current_period-1].current_best_bid = messageData.result.current_best_bid;
        }
        else if(messageData.result.offer_list != null)
        {
            app.$data.session.session_periods[app.$data.session.current_period-1].offer_list = messageData.result.offer_list;
            app.$data.session.session_periods[app.$data.session.current_period-1].current_best_offer = messageData.result.current_best_offer;
        }

        app.$data.bid_offer_id = "";
        app.$data.bid_offer_amount = "";

        app.$refs.bid_offer_id.focus();
    }
    else
    {

    }

    app.$data.bid_offer_message = messageData.result.message;
},
