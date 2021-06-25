
/**submit bid or offer
*/
submit_bid_offer:function(){
    app.$data.working = true;
    app.sendMessage("submit_bid_offer",{"bid_offer_id" : app.$data.bid_offer_id,
                                        "bid_offer_amount" : app.$data.bid_offer_amount,
                                        "sessionID" : app.$data.sessionID});
},

/**take result of submiting bid or offer
*/
take_submit_bid_offer:function(messageData){
    
    if(messageData.result.status == "success")
    {
        app.$data.bid_offer_id = "";
        app.$data.bid_offer_amount = "";

        app.$refs.bid_offer_id.focus();
    }
    else
    {

    }

    app.$data.bid_offer_message = messageData.result.message;
},
