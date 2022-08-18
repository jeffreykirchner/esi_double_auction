
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {values:[],
                    helpText : "Loading ...",
                    values_prices:[],
                    values_profits:[],
                    buyer:{{buyer_json|safe}},
                    buyer_profit:"0.00",
                    costs:[],
                    costs_prices:[],
                    costs_profits:[],
                    seller:{{seller_json|safe}},
                    seller_profit:"0.00",
                }},
    methods: {
        //update buyer profit when price changes
        update_buyer(index){
            if  (app.values_prices[index] == "")
            {
                app.values_profits[index]="";
            }
            else
            {
                app.values_profits[index] = parseFloat(app.buyer.periods[0].value_list[index-1].value_cost) - app.values_prices[index];
                app.values_profits[index] = app.values_profits[index].toFixed(2);
                app.values_prices[index] = parseFloat(app.values_prices[index]).toFixed(2);
            }

            total=0;
            for(i=0;i<app.values_profits.length;i++)
            {
                value = parseFloat(app.values_profits[i]);
                
                if(value) total += value;
            }

            app.buyer_profit=total.toFixed(2);
            
        },  
        
        //update seller profit when price changes
        update_seller(index){
            if  (app.costs_prices[index] == "")
            {
                app.costs_profits[index]="";
            }
            else
            {
                app.costs_profits[index] =  app.costs_prices[index] - parseFloat(app.seller.periods[0].cost_list[index-1].value_cost);
                app.costs_profits[index] = app.costs_profits[index].toFixed(2);
                app.costs_prices[index] = parseFloat(app.costs_prices[index]).toFixed(2);
            }

            total=0;
            for(i=0;i<app.costs_profits.length;i++)
            {
                value = parseFloat(app.costs_profits[i]);
                
                if(value) total += value;
            }

            app.seller_profit=total.toFixed(2);
            
        }, 

        {%include "js/help_doc.js"%}
    },

    mounted(){
        
    },

}).mount('#app');

