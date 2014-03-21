$(function(){
  var rawdata = ' [{"Statement": "Balance", "ItemName": "Total Assets", "Period": "1995Q0", "Value": "1232321", "CompanyID": "K TRON INTERNATIONAL INC 20"},{"Statement": "Balance", "ItemName": "Total Assets", "Period": "1995Q1", "Value": "2343242", "CompanyID": "K TRON INTERNATIONAL INC 20"},{"Statement": "Balance", "ItemName": "Total Assets", "Period": "1995Q2", "Value": "32432243", "CompanyID": "K TRON INTERNATIONAL INC 20"}' //placeholder
  // ??? I'm still unsure how we actually get either the data itself, or the commands into the html file. Can htmls be called with arguments from code written in a different language?
  var parsed = []; // the array of parsed data
  var labels = []; // an array where each index contains three things: The company, the field, and the class of the field.
  var datas = []; // an array of arrays, containing the raw data to be put into each series
  var series = [];

  // converts dates in the form YYYYQq into a JavaScript time.
  convertDate = function (date){
    var q = date[5]; // get the quarters
    q = 3*q; // convert to the appropriate month
    var y = date.substr(0,4);
    result = new Date(y, q, 0, 0, 0, 0, 0);
    return result;
  }

  // obtain the data, format "[{"Statement": "Balance", "ItemName": "Total Assets", "Period": "1995Q0", "Value": null, "CompanyID": "K TRON INTERNATIONAL INC 20"}, ... ]"

  /* I HAVE NO IDEA HOW I DO THIS */
  
  // parse the data input
  
  rawdata.replace("\"","").replace("]","").replace("CompanyID:","").replace("Value:","").replace("Period:","").replace("ItemName:","").replace("Statement:","").replace("[",""); // strip string of unwanted parts. There's probably a much better way of doing this.
  var raw1 = rawdata.split("}, {"); // parse into rows
  for(var i = 0; i<raw1.length; i+=1){ // parse into two dimensional array of strings.
    parsed.push(raw1[i].split(", "));
  }

  // convert the parsed data into a set of labels, and a set of x and y values to plot

  for(var i = 0; i<parsed.length; i+=1){
    var label = parsed[i][4]+": "+parsed[i][1]; // gets the three labels
	var value = parsed[i][3];
    if(parsed[i][0] == "Cash"){value = "-" + value;}	// I think the cash label means its an expenditure? If so, it sets the value to negative.
    var data = [value, convertDate(parsed[i][2])]; // gets y (time) and x (money) to plot
    var index = labels.indexOf(label); // find if label matches an existing series
    if(index<0){
      labels.push(label); // adds these labels to the array, updates index.
	  index = datas.push([]); // create a new series
    }
    datas[index].push(data); // adds the data to the correct series // this does not work, unsure why
  }

  // convert the labels and x,y data into an array of series?

  for(var i = 0; i<labels.length; i+=1){
    series.push( {
      data: datas[i],
	  label: labels[i],
    } )
  }

  // default options for all series	

  var options = {
    series: {
  	lines: { show: true }, // plot is a line graph
 	points: { show: true } // plot displays points
  },
  grid: {
	hoverable: true, // for use with interactivity
	clickable: true // for use with interactivity
  },
  xaxis: {
       mode: "time", // axis is in time mode
       timeformat: "%YQ%q", //axis displays time in quarters
	minTickSize: [3, "month"] // axis grid-lines are at quarters
     }
  }

  var plot = $.plot("#placeholder", series, options);
  
  $("<div id='tooltip'></div>").css({
	position: "absolute",
	display: "none",
	border: "1px solid #fdd",
	padding: "2px",
	"background-color": "#fee",
	opacity: 0.80
  }).appendTo("body");
			

  // event for clicking; displays a tooltip and highlights until next click
  $("#placeholder").bind("plotclick", function (event, pos, item) {
	if (item) {
	  var x = item.datapoint[0],
	  y = item.datapoint[1];
	  plot.unhighlight();
	$("#tooltip").html(item.series.label + " (" + x + "," + y + ")")
						.css({top: item.pageY+5, left: item.pageX+5})
						.fadeIn(200);
					plot.highlight(item.series, item.datapoint);
				}
			});
});