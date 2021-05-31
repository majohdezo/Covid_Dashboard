/*
*PRIMER CHART
*/

var margin ={top: 20, right: 100, bottom: 30, left: 50},
    width = 800 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom,
    radius = Math.min(width, height) / 2;

var svg = d3.select("#chart-area").append("svg")
	.attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);
var g = svg.append("g")
    .attr("transform", 
    	"translate(" + width / 2 + "," + height / 2 + ")");

g.append("text")
    .attr("class", "x axis-label")
    .attr("x",  width2 / 2 )
    .attr("y", height2)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("transform","translate(0,200)")
    .style("fill","#414042")
    .text("Tipo de Paciente por Sexo");

var color = d3.scaleOrdinal(d3.schemeSet2);

// TODO: create the arc generator for a donut chart.
// var arc = ...
var arc = d3.arc()
	.outerRadius(radius - 20)
	.innerRadius(radius - 80);

// TODO: create the pie layout generator.
// var pie = ...
var pie = d3.pie()
	.value((d) => { return d.COUNT; })
	.sort(null);


d3.json("data/covid/paciente_sexo.json").then((data)=> {
        data.forEach((d)=>{
            d.COUNT = +d.COUNT;
        });
    console.log(data);


    var peopleBySex =  d3.nest()
	    .key((d) => { return d.SEXO; })
	    .entries(data);

    

       

    var label = d3.select("form").selectAll("label")
        .data(peopleBySex)
        .enter().append("label");

   
    label.append("input")
        	.attr("type", "radio")
        	.attr("name", "sexo")
        	.attr("value", (d) => { return d.key; })
        	.on("change", update)
        .filter((d, i) => { return !i; })
        	.each(update)
        	.property("checked", true);

    label.append("span")
        .attr("fill", "red")
        .text((d) => { return d.key; });

}).catch((error) => {
    console.log(error);
});

function update(TIPO_PACIENTE) {

    var tip = d3.tip().attr('class', 'd3-tip')
        .html((d) => { 
            var text = "<strong>Tipo de paciente:</strong>";
            text += "<span style='color:red'> " + d.data.TIPO_PACIENTE + "</span><br>";  
            text += "<strong> Cantidad:</strong>";       
            text +=  d.data.COUNT;     
            return text;            
        });

    g.call(tip);		
    var path = g.selectAll("path");

    var data0 = path.data(),
        data1 = pie(TIPO_PACIENTE.values);

    // JOIN elements with new data.
    path = path.data(data1, key);

    // EXIT old elements from the screen.
    path.exit()
        .datum((d, i) => { 
        	return findNeighborArc(i, data1, data0, key) || d; 
        })
        .transition()
        .duration(750)
        .attrTween("d", arcTween)
        .remove();
    
    // UPDATE elements still on the screen.
    path.transition()
        .duration(750)
        .attrTween("d", arcTween);

    // ENTER new elements in the array.
    path.enter()
        .append("path")
        .each((d, i) => { 
        	this._current = 
        		findNeighborArc(i, data0, data1, key) || d; 
        }) 
        .attr("fill", (d) => {  
        	return color(d.data.TIPO_PACIENTE) 
        })
        .on("mouseover", tip.show)
		.on("mouseout", tip.hide)
        .transition()
        .duration(750)
            .attrTween("d", arcTween);
}

function key(d) {
    return d.data.TIPO_PACIENTE;
}

function findNeighborArc(i, data0, data1, key) {
    var d;
    return (d = findPreceding(i, data0, data1, key)) ? {startAngle: d.endAngle, endAngle: d.endAngle}
        : (d = findFollowing(i, data0, data1, key)) ? {startAngle: d.startAngle, endAngle: d.startAngle}
        : null;
}

// Find the element in data0 that joins the highest preceding element in data1.
function findPreceding(i, data0, data1, key) {
    var m = data0.length;
    while (--i >= 0) {
        var k = key(data1[i]);
        for (var j = 0; j < m; ++j) {
            if (key(data0[j]) === k) return data0[j];
        }
    }
}

// Find the element in data0 that joins the lowest following element in data1.
function findFollowing(i, data0, data1, key) {
    var n = data1.length, m = data0.length;
    while (++i < n) {
        var k = key(data1[i]);
        for (var j = 0; j < m; ++j) {
            if (key(data0[j]) === k) return data0[j];
        }
    }
}

function arcTween(d) {
    var i = d3.interpolate(this._current, d);
    this._current = i(1)
    return (t) => { return arc(i(t)); };
}

//////////////////////////////////////////////////////////////////////////////////////////////
/*
*    SEGUNDO CHART
*/

var margin2 = { left:80, right:100, top:50, bottom:100 },
    height2 = 600 - margin2.top - margin2.bottom, 
    width2 = 1000 - margin2.left - margin2.right;

var svg2 = d3.select("#chart-area2").append("svg")
    .attr("width", width2 + margin2.left + margin2.right)
    .attr("height", height2 + margin2.top + margin2.bottom);

var g2 = svg2.append("g")
    .attr("transform", "translate(" + margin2.left + 
        ", " + margin2.top + ")");

// Time parser for x-scale
var parseTime = d3.timeParse("%Y");
// For tooltip
var bisectDate = d3.bisector((d) => { return d.MES; }).left;

// Scales
var x2 = d3.scaleTime().range([0, width2]);
var y2 = d3.scaleLinear().range([height2, 0]);


// Axis groups
var xAxis = g2.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height2 + ")");
var yAxis = g2.append("g")
    .attr("class", "y axis")
    
// Y-Axis label
yAxis.append("text")
    .attr("class", "axis-title")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .attr("fill", "#414042")
    .text("Muertes");

xAxis.append("text")
    .attr("class", "axis-title")
    .attr("x", width2+30)
    .attr("y", -10)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .attr("fill", "##414042")
    .text("Meses");

// Line path generator
// TODO: Implement the line generator
var line = d3.line()

	.x((d) => { return x2(d.MES); })

	.y((d) => { return y2(d.COUNT); });

d3.json("data/covid/muertes_2020.json").then((data2) => {
    // Data cleaning
    data2.forEach((d) => {
        d.MES = +d.MES;
        d.COUNT = +d.COUNT;
    });

    

    // Set scale domains
    // TODO: set domain of axes
    x2.domain([d3.min(data2, (d) => { return d.MES; }), d3.max(data2, (d) => { return d.MES; })]);
    y2.domain([d3.min(data2, (d) => { return d.COUNT; }), d3.max(data2, (d) => { return d.COUNT; })]);
    
    

    // Add line to chart
    // TODO: add line path
    g2.append("path")
        .attr("class", "line")
    	.attr("fill", "none")
        .attr("stroke", "grey")
        .attr("stroke-with", "3px")
        .attr("d", line(data2))
    
    // Axis generators
    var names=data2.map((d)=>{return d.MES_NOMBRE;});
    
    var x_n = d3.scaleBand()
	    .domain(names)
	    .range(([-30,width2+30]));

    var bottomAxis=d3.axisBottom(x_n);

    g2.append("g")
        .attr("class", "bottom axis")
        .attr("transform", "translate(0, " + height2+ ")")
	    .call(bottomAxis).selectAll("text")
	        .attr("y", "15")
	        .attr("x", "10")
	        .attr("text-anchor", "end")
	        .attr("transform", "rotate(-25)");

    g2.append("text")
        .attr("class", "x axis-label")
        .attr("x",  width2 / 2)
        .attr("y", height2+140)
        .attr("font-size", "20px")
        .attr("text-anchor", "middle")
        .attr("transform","translate(0,-55)")
        .style("fill","#414042")
        .text("Muertes por Covid en México en 2020");


    
    
    var yAxisCall = d3.axisLeft()
        .ticks(6)
        .tickFormat((d) => { console.log(d); return parseInt(d / 1000) + "k"; });

    
    yAxis.call(yAxisCall.scale(y2))

    /******************************** Tooltip Code ********************************/

    var focus = g2.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("line")
        .attr("class", "x-hover-line hover-line")
        .attr("y1", 0)
        .attr("y2", height2);

    focus.append("line")
        .attr("class", "y-hover-line hover-line")
        .attr("x1", 0)
        .attr("x2", width2);

    focus.append("circle")
        .attr("r", 7.5);

    focus.append("text")
        .attr("x", 15)
        .attr("dy", ".31em");

    g2.append("rect")
        .attr("class", "overlay")
        .attr("width", width2)
        .attr("height", height2)
        .on("mouseover", () => { focus.style("display", null); })
        .on("mouseout", () => { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
        var x0 = x2.invert(d3.mouse(this)[0]),
            i = bisectDate(data2, x0, 1),
            d0 = data2[i - 1],
            d1 = data2[i],
            d = x0 - d0.MES > d1.MES - x0 ? d1 : d0;
        focus.attr("transform", "translate(" + x2(d.MES) + "," + y2(d.COUNT) + ")");
        focus.select("text").text(d.COUNT);
        focus.select(".x-hover-line").attr("y2", height2 - y2(d.COUNT));
        focus.select(".y-hover-line").attr("x2", -x2(d.MES));
    }

});




////////////////////////////////////////////////////////////////////////////////////


/*
*    TERCER CHART
*/

var margin3={left:100,right:10,top:100,bottom:100};
var width=1000;
var height=600;

var svg3 = d3.select("#chart-area3").append("svg")
	.attr("width", width + margin3.left + margin3.right)
    .attr("height", height + margin3.top + margin3.bottom);
var g3 = svg3.append("g")
    .attr("transform","translate("+margin3.left+", "+margin3.top+")");



d3.json("data/covid/casos_entidad.json").then((data3)=> { 
    console.log(data3);
    data3.forEach((d)=>{
  		d.COUNT = +d.COUNT;
  	});
    
    var names=data3.map((d)=>{return d.ENTIDAD_RES;});
    
    var x = d3.scaleBand()
	    .domain(names)
	    .range(([0,width]))
	    .paddingInner(0.3)
	    .paddingOuter(0.2);

    var y = d3.scaleLinear()
        .domain([57471,0])
        .range([0,height]);

    var color = d3.scaleOrdinal()
      .domain(names)
      .range(d3.schemeSet3);

      var tip = d3.tip().attr('class', 'd3-tip')
      .offset([-10, 0])
      .html((d) => { 
          var text = "<strong> " + d.ENTIDAD_RES + ":</strong><br>";             
          text +=  d.COUNT;     
          text += " casos";  
          return text;            
    });


    g3.call(tip);	

    

    var buildings = g3.selectAll("rect")
        .data(data3)

    buildings.enter()
        .append("rect")
        .attr("x", (d, i) =>{return x(d.ENTIDAD_RES)})
        .attr("y", (d)=>{return y(d.COUNT)})
        .attr("width", x.bandwidth())
        .attr("height", (d)=>{return height-y(d.COUNT);})
        .attr("stroke","#6d6e71")
        .attr("fill",(d)=>{return color(d.COUNT)})
        .on("mouseover", tip.show)
		.on("mouseout", tip.hide);

    var bottomAxis=d3.axisBottom(x);
    
    g3.append("g")
        .attr("class", "bottom axis")
        .attr("transform", "translate(0, " + height+ ")")
	    .call(bottomAxis).selectAll("text")
	        .attr("y", "10")
	        .attr("x", "-5")
	        .attr("text-anchor", "end")
	        .attr("transform", "rotate(-25)");
    
    var leftAxis = d3.axisLeft(y)
        .ticks(5)
        .tickFormat((d)=>{return d;});

    g3.append("g")
	    .attr("class", "left axis")
	    .call(leftAxis);

    g3.append("text")
        .attr("class", "x axis-label")
        .attr("x",  width / 2)
        .attr("y", height+140)
        .attr("font-size", "20px")
        .attr("text-anchor", "middle")
        .attr("transform","translate(0,-55)")
        .style("fill","#414042")
        .text("Casos de Covid en Mexico por estado en 2020");

    g3.append("text")
        .attr("class", "y axis-label")
        .attr("x",  -(height / 2))
        .attr("y", -60)
        .attr("font-size", "20px")
        .attr("text-anchor", "middle")
        .attr("transform", "rotate(-90)")
        .style("fill","#414042")
        .text("Número de casos");

    

}).catch((error)=>{
    console.log(error)
});

/*
*    Cuarto Chart
*/

var margin4={left:100,right:10,top:10,bottom:100};
width=800;
height=500; 
var flag=true;
var t=d3.transition().duration(750);

var g4=d3.select("#chart-area4").append("svg")
    .attr("width",width+margin4.right+margin4.left)
    .attr("height",height+margin4.bottom+margin4.top)
    .append("g")
    .attr("transform","translate("+margin4.left+", "+margin4.top+")");

var x= d3.scaleBand()    
    .range([0,width])
    .padding(0.2)
    ;    
 
var y=d3.scaleLinear().range([0,height]);    

var xAxisGroup=g4.append("g")
    .attr("class","x axis")
    .attr("transform","translate(0, "+height+")");

var yAxisGroup = g4.append("g")
    .attr("class", "y-axis");   

g4.append("text")
    .attr("class","x axis-label")
    .attr("x",width/2)
    .attr("y",height+160)
    .attr("font-size","20px")
    .attr("text-anchor","middle")
    .attr("fill","#414042")
    .attr("transform","translate(0,-70)")
    .text("Casos de Diabetes y Neumonia en personas con Covid por estado en 2020");    
    
var yLabel=g4.append("text")
    .attr("class","y axis-label")
    .attr("x",-(height/2))
    .attr("y",-60)
    .attr("font-size","20px")
    .attr("text-anchor","middle")
    .attr("transform","rotate(-90)")
    .attr("fill","#414042");    

d3.json("data/covid/diab_neu.json").then((data4)=>{
    console.log(data4);
    data4.forEach(d => {
        d.CASOS_DIABETES = +d.CASOS_DIABETES;
        d.CASOS_NEUMONIA = +d.CASOS_NEUMONIA;
    });

    d3.interval(()=>{
        console.log("Hello world");
        var newData = flag ? data4 : data4;
        update2(newData);
        flag=!flag;
    },1000);
    update2(data4);

}).catch((error)=>{
    console.log(error);
});

function update2(data4){
    var value = flag ? "CASOS_DIABETES" : "CASOS_NEUMONIA";

    x.domain(data4.map((d)=>{return d.ENTIDAD_RES;}));
    y.domain([d3.max(data4,(d)=>{return 5000;}),0]);

    var bars=g4.selectAll("rect").data(data4,(d)=>{return d.ENTIDAD_RES;});

  
    bars.transition(t)
        .attr("x",(d)=>{return x(d.ENTIDAD_RES);})
        .attr("y",(d)=>{return y(d[value]);})
        .attr("width",x.bandwidth)
        .attr("height",(d)=>{return height-y(d[value]);})
        .attr("fill",(d)=>{return value=="CASOS_DIABETES"? '#42daf5':'#65c96a';});
          

    bars.enter()
        .append("rect")
        .attr("y", y(0))
        .attr("height", 0)
        .attr("x", (d) =>{return x(d.ENTIDAD_RES)})
        .attr("width", x.bandwidth)
        .attr("fill","#42daf5")
        .merge(bars)
        .transition(t)
            .attr("y",(d)=>{return y(d[value]);})
            .attr("height",(d)=>{return height-y(d[value]);});
       
    var bottomAxis=d3.axisBottom(x);

    xAxisGroup.transition(t)
        .call(bottomAxis)
        .attr("fill","#414042")
        .selectAll("text")
            .attr("y","5")
            .attr("x","0")
            .attr("text-anchor","end")
            .attr("fill","#414042")
            .attr("transform", "rotate(-40)");

    var leftAxis=d3.axisLeft(y)
        .ticks(10)
        .tickFormat((d)=>{return +d/1000+"K";});
    
    yAxisGroup.call(leftAxis)
        .attr("fill","#d4d8d9")
        .selectAll("text")
        .attr("fill","#414042");

    var label = flag ? "Diabetes" : "Neumonia";
    yLabel.text(label);
}






