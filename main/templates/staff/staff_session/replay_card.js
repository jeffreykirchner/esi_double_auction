/**change the period being shown during replay
*/
updateCurrentPeriodReplay(adjustment){
    
    if(adjustment == 1)
    {
        if(app.$data.current_visible_period < app.$data.session.parameter_set.number_of_periods)
        {
            app.$data.current_visible_period += 1;
        }
    }
    else
    {
        if(app.$data.current_visible_period > 1)
        {
            app.$data.current_visible_period -= 1;
        }
    }

    app.$data.session.current_period =  app.$data.current_visible_period;

    Vue.nextTick(app.update_sdgraph_canvas());
},

/** start playback
 **/
playback_start(){

    app.$data.playback_enabled=true;
    app.$data.playback_trade=0;

    app.$data.show_bids_offers_graph = false;
    app.$data.show_supply_demand_graph = true;
    app.$data.show_equilibrium_price_graph = false;
    app.$data.show_trade_line_graph = false;
    app.$data.show_gains_from_trade_graph = false;

    Vue.nextTick(app.update_sdgraph_canvas());
},

/** advance playback period in direction specified
 **/
playback_advance(direction){
    current_visible_period=app.$data.current_visible_period-1;
    session_period = app.$data.session.session_periods[current_visible_period];
    parameter_set_period = app.$data.session.parameter_set.periods[current_visible_period]

    if(direction == 1 && 
       app.$data.playback_trade < session_period.trade_list.length)
    {
        app.$data.playback_trade++;
    }
    else if (direction == -1 && app.$data.playback_trade > 0)
    {
        app.$data.playback_trade--;
    }

    // hide used bids and offers
    for(let i=0;i<app.$data.playback_trade;i++)
    {
        app.set_demand_visible(session_period.trade_list[i].buyer_value__id, false);
        app.set_supply_visible(session_period.trade_list[i].seller_cost__id, false);
    }

    //show remaining bids and offers
    for(i = app.$data.playback_trade; i < session_period.trade_list.length; i++)
    {
        app.set_demand_visible(session_period.trade_list[i].buyer_value__id, true);
        app.set_supply_visible(session_period.trade_list[i].seller_cost__id, true);
    }

    Vue.nextTick(app.update_sdgraph_canvas());
},

/**set demand step visibility based on id number
 */
set_demand_visible(id, value){
    session = app.$data.session;
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
    var session = app.$data.session;
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
    var session = app.$data.session;
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
    var session = app.$data.session;
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
    app.$data.playback_enabled=false;

    app.$data.show_supply_demand_graph = false;
    app.$data.show_bids_offers_graph = true;

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

