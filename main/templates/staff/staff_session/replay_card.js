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