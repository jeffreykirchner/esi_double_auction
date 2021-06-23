/**refresh the supply and demand canvas
*/
update_sdgraph_canvas:function(){

    var el = $('#sd_graph');
    el.attr('width', parseInt(el.css('width')));
    el.attr('height', parseInt(el.css('height')));

    period = app.$data.session.parameter_set.periods[app.$data.current_visible_period-1];
    value_list = period.demand;
    cost_list = period.supply;

    y_max = period.y_scale_max;
    x_max = period.x_scale_max;

    var marginY=45;    //margin between left side of canvas and Y axis
    var marginX=40;    //margin between bottom of canvas and X axis
    var marginTopAndRight=10;    // margin between top and right sides of canvas and graph

    app.draw_axis("sd_graph", marginY, marginX, marginTopAndRight, 0, y_max, y_max, 0, x_max, x_max, "Price", "Units Traded");

    //supply
    app.draw_sd_line("sd_graph", marginY, marginX, marginTopAndRight, 0, y_max, 0, x_max, 3, value_list, "blue");

    //demand
    app.draw_sd_line("sd_graph", marginY, marginX, marginTopAndRight, 0, y_max, 0, x_max, 3, cost_list, "red");

    //equilibrium
    app.draw_eq_lines("sd_graph", marginY, marginX, marginTopAndRight, 0, y_max, 0, x_max, period)
},

/**draw an x-y axis on a canvas
 * @param chartID {string} dom ID name of canvas
 * @param marginY {int} margin between Y axis and vertial edge of graph
 * @param marginX {int} margin between X axis and horizontal edge of graph
 * @param marginTopAndRight {int} margin between top and rights side of canvas and graph
 * @param yMin {int} starting value on Y axis
 * @param yMax {int} ending value on Y axis
 * @param yTickCount {int} number of ticks along Y axis
 * @param xMin {int} starting value on X axis
 * @param xMax {int} ending value on X axis
 * @param xTickCount {int} number of ticks along X axis
 * @param yLabel {string} label on Y axis
 * @param XLabel {string} label on X axis
*/
draw_axis: function (chartID, marginY, marginX, marginTopAndRight, yMin, yMax, yTickCount, xMin, xMax, xTickCount, yLabel, xLabel){
    
    if(document.getElementById(chartID) == null)
    {
        return;
    }

    var canvas = document.getElementById(chartID),
        ctx = canvas.getContext('2d');    

    ctx.save();

    var xScale = xMax-xMin;
    var yScale = yMax-yMin;

    var w = ctx.canvas.width;
    var h = ctx.canvas.height;

    var tickLength=3;
    
    var xTickValue=xScale/parseFloat(xTickCount);
    var yTickValue=yScale/parseFloat(yTickCount);

    ctx.moveTo(0,0);

    //clear screen
    // ctx.fillStyle = "white";
    // ctx.fillRect(0,0,w,h);
    ctx.clearRect(0,0,w,h);
    ctx.strokeStyle="black";
    ctx.lineWidth=3;

    //axis
    ctx.beginPath();
    ctx.moveTo(marginY, marginTopAndRight);
    ctx.lineTo(marginY, h-marginX);
    ctx.lineTo(w-marginTopAndRight, h-marginX);
    ctx.lineWidth = 3;
    ctx.lineCap = "round";
    ctx.stroke();

    //y ticks
    ctx.beginPath();                                                               
    ctx.font="12px Georgia";
    ctx.fillStyle = "black";
    ctx.textAlign = "right";

    var tempY = h-marginX;     
    var tempYValue = yMin;

    for(var i=0;i<=yTickCount;i++)
    {                                       
        ctx.moveTo(marginY, tempY);                                   
        ctx.lineTo(marginY-5, tempY);
        ctx.fillText(tempYValue,marginY-8,tempY+4);

        tempY -= ((h-marginX-marginTopAndRight)/ (yTickCount));
        tempYValue += yTickValue;
    }

    ctx.stroke();

    //x ticks
    ctx.beginPath();                                                               
    ctx.textAlign = "center";

    var tempX = marginY;
    var tempXValue=xMin;                                
    for(var i=0;i<=xTickCount;i++)
    {                                       
        ctx.moveTo(tempX, h-marginX);                                   
        ctx.lineTo(tempX,  h-marginX+5);
        ctx.fillText(Math.round(tempXValue).toString(),tempX,h-marginX+18);

        tempX += ((w-marginY-marginTopAndRight)/ (xTickCount));
        tempXValue += xTickValue;
    }

    ctx.stroke();

    ctx.restore();

    //labels
    ctx.save();
    ctx.textAlign = "center";
    ctx.fillStyle = "DimGray";
    ctx.font="bold 14px Arial"; 

    ctx.translate(14, h/2);
    ctx.rotate(-Math.PI/2);                                                              
    ctx.fillText(yLabel,0,0);
    ctx.restore();

    ctx.save();
    ctx.textAlign = "center";
    ctx.fillStyle = "DimGray";
    ctx.font="bold 14px Georgia";
    ctx.fillText(xLabel,w/2,h-4);
    ctx.restore();                       
},

/** draw either the supply or demand line
 * @param chartID {string} dom ID name of canvas
 * @param marginY {int} margin between Y axis and vertial edge of graph
 * @param marginX {int} margin between X axis and horizontal edge of graph
 * @param marginTopAndRight {int} margin between top and rights side of canvas and grap
 * @param yMin {int} starting value on Y axis
 * @param yMax {int} ending value on Y axis
 * @param xMin {int} starting value on X axis
 * @param xMax {int} ending value on X axis
 * @param lineWidth {int} width of the line
 * @param valueList[] {int} sorted values of line
 * @param lineColor {string, hex} color of line
*/
draw_sd_line: function(chartID, marginY, marginX, marginTopAndRight, yMin, yMax, xMin, xMax, lineWidth, valueList, lineColor){
    var canvas = document.getElementById(chartID),
        ctx = canvas.getContext('2d');

    var w =  ctx.canvas.width;
    var h = ctx.canvas.height;
    
    ctx.save();

    ctx.strokeStyle = lineColor;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = "round";
    ctx.font="12px Arial";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";

    ctx.translate(marginY, h-marginX);

    for(i=0; i<valueList.length; i++)
    {
        xStart = app.convertToX(i, xMax, xMin, w-marginY-marginTopAndRight, lineWidth);
        xEnd = app.convertToX(i+1, xMax, xMin, w-marginY-marginTopAndRight, lineWidth);
        y1 = app.convertToY(parseFloat(valueList[i].value_cost), yMax, yMin, h-marginX-marginTopAndRight, lineWidth);

        //horizontal line
        ctx.beginPath();
        ctx.moveTo(xStart, y1);
        ctx.lineTo(xEnd, y1);        

        //vertical line
        if(i<valueList.length-1)
        {
            y2 = app.convertToY(parseFloat(valueList[i+1].value_cost), yMax, yMin, h-marginX-marginTopAndRight, lineWidth);
            ctx.lineTo(xEnd, y2);
        }

        ctx.stroke();

        //label
        ctx.fillText(valueList[i].label,(xEnd-xStart)/2 + xStart, y1-3);

    }

    ctx.restore(); 
},

/**draw the equilibrium price and quantity lines
*/
draw_eq_lines: function(chartID, marginY, marginX, marginTopAndRight, yMin, yMax, xMin, xMax, period){

    if(period.eq_price == null) return;

    var canvas = document.getElementById(chartID),
        ctx = canvas.getContext('2d');

    var w =  ctx.canvas.width;
    var h = ctx.canvas.height;
    
    ctx.save();

    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.lineCap = "round";
    ctx.setLineDash([5, 5]);
    ctx.font="14px Arial";
    ctx.fillStyle = "black";
    ctx.textAlign = "left";

    ctx.translate(marginY, h-marginX);

    ctx.beginPath();

    y1 = app.convertToY(period.eq_price, yMax, yMin, h-marginX-marginTopAndRight, 1);
    x1 = app.convertToX(0, xMax, xMin, w-marginY-marginTopAndRight, 1);

    y2 = app.convertToY(0, yMax, yMin, h-marginX-marginTopAndRight, 1);
    x2 = app.convertToX(period.eq_quantity, xMax, xMin, w-marginY-marginTopAndRight, 1);

    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y1); 
    ctx.lineTo(x2, y2); 

    ctx.stroke();

    ctx.fillText(period.eq_price, x1+5, y1-5);

    ctx.restore(); 
},

/**convert value to X cordinate on the graph
 * @param value {float} value to be converted to X cordinate
 * @param maxValue {float} ceiling of value on graph
 * @param minValue {float} floor of value to be shown on graph
 * @param canvasWidth {int} width of the canvas in pixels
 * @param markerWidth {int} width of the marker or line in pixels
 */
convertToX:function(value, maxValue, minValue, canvasWidth, markerWidth){
    markerWidth=0;

    tempT = canvasWidth / (maxValue-minValue);

    value-=minValue;

    if(value>maxValue) value=maxValue;

    return (tempT * value - markerWidth/2);
},

/**convert value to Y cordinate on the graph
 * @param value {float} value to be converted to Y cordinate
 * @param maxValue {float} ceiling of value on graph
 * @param minValue {float} floor of value to be shown on graph
 * @param canvasHeight {int} height of the canvas in pixels
 * @param markerHeight {int} height of the marker or line in pixels
 */
convertToY:function(value, maxValue, minValue, canvasHeight, markerHeight){
    markerHeight=0;
    
    tempT = canvasHeight / (maxValue-minValue);

    if(value > maxValue) value=maxValue;
    if(value < minValue) value=minValue;

    value-=minValue;

    if(value>maxValue) value=maxValue;

    return(-1 * tempT * value - markerHeight/2)
},