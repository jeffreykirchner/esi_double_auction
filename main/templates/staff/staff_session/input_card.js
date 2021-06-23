
/**submit bid or offer
*/
submit_bid_offer:function(){
    app.$data.working = true;
    app.sendMessage("submit_bid_offer",{"formData" : $("#bidOfferForm").serializeArray(),
                                        "sessionID" : app.$data.sessionID});
},

/**take result of submiting bid or offer
*/
take_submit_bid_offer:function(){

},
