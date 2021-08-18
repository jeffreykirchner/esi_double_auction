
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

//vue app
var app = Vue.createApp({
    delimiters: ["[[", "]]"],

    data() {return {values:[],
                    values_prices:[],
                    values_profits:[],
                    buyer:{{buyer_json|safe}},
                    costs:[],
                    costs_prices:[],
                    costs_profits:[],
                    seller:{{seller_json|safe}},
                }},
    methods: {
        //update buyer profit when price changes
        update_buyer(index){
            if  (app.$data.values_prices[index] == "")
            {
                app.$data.values_profits[index]="";
            }
            else
            {
                app.$data.values_profits[index] = parseFloat(app.$data.buyer.periods[0].value_list[index-1].value_cost) - app.$data.values_prices[index];
                app.$data.values_profits[index] = app.$data.values_profits[index].toFixed(2);
                app.$data.values_prices[index] = parseFloat(app.$data.values_prices[index]).toFixed(2);
            }
            
        },  
        
        //update seller profit when price changes
        update_seller(index){
            if  (app.$data.costs_prices[index] == "")
            {
                app.$data.costs_profits[index]="";
            }
            else
            {
                app.$data.costs_profits[index] = parseFloat(app.$data.seller.periods[0].cost_list[index-1].value_cost) - app.$data.costs_prices[index];
                app.$data.costs_profits[index] = app.$data.costs_profits[index].toFixed(2);
                app.$data.costs_prices[index] = parseFloat(app.$data.costs_prices[index]).toFixed(2);
            }
            
        }, 
    },

    mounted(){
        
    },

}).mount('#app');

