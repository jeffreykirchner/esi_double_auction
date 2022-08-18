/**change the period being shown during replay
*/
updateCurrentPeriodReplay(adjustment){
    
    if(adjustment == 1)
    {
        if(app.current_visible_period < app.session.parameter_set.number_of_periods)
        {
            app.current_visible_period += 1;
        }
    }
    else
    {
        if(app.current_visible_period > 1)
        {
            app.current_visible_period -= 1;
        }
    }

    app.show_bids_offers_graph = true;
    app.show_supply_demand_graph = false;
    app.show_equilibrium_price_graph = false;
    app.show_trade_line_graph = false;
    app.show_gains_from_trade_graph = false;

    app.session.current_period =  app.current_visible_period;

    Vue.nextTick(app.update_sdgraph_canvas());
},

/** start playback
 **/
playback_start(){

    app.playback_enabled=true;
    app.playback_trade=0;

    app.show_bids_offers_graph = false;
    app.show_supply_demand_graph = true;
    app.show_equilibrium_price_graph = false;
    app.show_trade_line_graph = false;
    app.show_gains_from_trade_graph = false;

    Vue.nextTick(app.update_sdgraph_canvas());
},

/** advance playback period in direction specified
 **/
playback_advance(direction){
    current_visible_period=app.current_visible_period-1;
    session_period = app.session.session_periods[current_visible_period];
    parameter_set_period = app.session.parameter_set.periods[current_visible_period]

    if(direction == 1 && 
       app.playback_trade < session_period.trade_list.length)
    {
        app.playback_trade++;
    }
    else if (direction == -1 && app.playback_trade > 0)
    {
        app.playback_trade--;
    }

    // hide used bids and offers
    for(let i=0;i<app.playback_trade;i++)
    {
        app.set_demand_visible(session_period.trade_list[i].buyer_value__id, false);
        app.set_supply_visible(session_period.trade_list[i].seller_cost__id, false);
    }

    //show remaining bids and offers
    for(i = app.playback_trade; i < session_period.trade_list.length; i++)
    {
        app.set_demand_visible(session_period.trade_list[i].buyer_value__id, true);
        app.set_supply_visible(session_period.trade_list[i].seller_cost__id, true);
    }

    Vue.nextTick(app.update_sdgraph_canvas());
},

/**set demand step visibility based on id number
 */
set_demand_visible(id, value){
    session = app.session;
    parameter_set = session.parameter_set;

    for(let i=0; i<parameter_set.periods.length;i++)
    {
        demand = parameter_set.periods[i].demand;
        for(let j=0; j<demand.length;j++)
        {
            if(demand[j].id == id)
            {
                demand[j].visible=value;
                return;
            }
        }
    }
 
},

/**return index in demand array that value holds
 */
 get_demand_index(id){
    var session = app.session;
    var parameter_set = session.parameter_set;

    for(let i=0; i<parameter_set.periods.length;i++)
    {
        var demand = parameter_set.periods[i].demand;
        var counter=0;

        for(let j=0; j<demand.length;j++)
        {
            if(demand[j].id == id)
            {
                return {index:counter, value:demand[j].value_cost};
            }

            if(demand[j].visible) counter++;
        }
    }
 
},

/**set cost step visibility based on id number
 */
 set_supply_visible(id, value){
    var session = app.session;
    var parameter_set = session.parameter_set;

    for(let i=0; i<parameter_set.periods.length;i++)
    {
        var supply = parameter_set.periods[i].supply;
        for(let j=0; j<supply.length;j++)
        {
            if(supply[j].id == id)
            {
                supply[j].visible=value;
                return;
            }
        }
    }
 
},

/**return index in supply array cost holds
 */
get_supply_index(id){
    var session = app.session;
    var parameter_set = session.parameter_set;

    for(let i=0; i<parameter_set.periods.length;i++)
    {
        var supply = parameter_set.periods[i].supply;
        var counter=0;

        for(let j=0; j<supply.length;j++)
        {
            if(supply[j].id == id)
            {
                return {index:counter, cost:supply[j].value_cost};
            }

            if(supply[j].visible) counter++;
        }
    } 
},

/** start playback
 * */
 playback_stop(){
    app.playback_enabled=false;

    app.show_supply_demand_graph = false;
    app.show_bids_offers_graph = true;

    var session = app.session;
    var parameter_set = session.parameter_set;

    //reset visibility
    for(i=0; i<parameter_set.periods.length;i++)
    {
        demand = parameter_set.periods[i].demand;
        for(j=0; j<demand.length;j++)
        {
            demand[j].visible=true;
        }
    }

    for(let i=0; i<parameter_set.periods.length;i++)
    {
        supply = parameter_set.periods[i].supply;
        for(let j=0; j<supply.length;j++)
        {
            supply[j].visible=true;
        }
    }

    Vue.nextTick(app.update_sdgraph_canvas());
},

/** send request to download parameters to a file 
*/
sendDownloadDataset(){
    
    app.working = true;
    app.sendMessage("download_dataset", {"sessionID" : app.sessionID,});
},

/** download parameter set into a file 
 @param messageData {json} result of file request, either sucess or fail with errors
*/
takeDownloadDataset(messageData){
    

    if(messageData.status == "success")
    {                  
        console.log(messageData.parameter_set);

        var downloadLink = document.createElement("a");
        var jsonse = JSON.stringify(messageData.dataset);
        var blob = new Blob([jsonse], {type: "application/json"})
        var url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = "Double_Auction_Session_" + app.session.id + "_Dataset.json";

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);                     
    } 

    app.working = false;
},


