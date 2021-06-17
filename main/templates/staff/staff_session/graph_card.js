/**refresh the supply and demand canvas
*/


update_sdgraph_canvas:function(){

    var el = $('#sd_graph');
    el.attr('width', parseInt(el.css('width')));
    el.attr('height', parseInt(el.css('height')));

    period = app.$data.session.parameter_set.periods[app.$data.current_period-1];
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

convertToX:function(tempValue,maxValue,minValue,tempWidth, markerWidth){
    tempT = tempWidth / (maxValue-minValue);

    tempValue-=minValue;

    if(tempValue>maxValue) tempValue=maxValue;

    return (tempT * tempValue - markerWidth/2);
},

convertToY:function(tempValue,maxValue,minValue,tempHeight, markerHeight){
    tempT = tempHeight / (maxValue-minValue);

    if(tempValue > maxValue) tempValue=maxValue;
    if(tempValue < minValue) tempValue=minValue;

    tempValue-=minValue;

    if(tempValue>maxValue) tempValue=maxValue;

    return(-1 * tempT * tempValue - markerHeight/2)
},