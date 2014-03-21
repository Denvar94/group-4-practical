$(function(){
  var rawdata = '[{"Statement": "Balance", "ItemName": "Total Assets", "Period": "1995Q0", "Value": "", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1995Q1", "Value": "0", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Current Assets", "Period": "1999Q3", "Value": "36066", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1996Q0", "Value": "69296", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1996Q1", "Value": "65438", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1996Q2", "Value": "61142", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1996Q3", "Value": "59275", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1997Q0", "Value": "55330", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1997Q1", "Value": "530370", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1997Q2", "Value": "53434", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1997Q3", "Value": "53768", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1998Q0", "Value": "54249", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1998Q1", "Value": "52802", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1998Q2", "Value": "54978", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1998Q3", "Value": "58154", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1999Q0", "Value": "56617", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1999Q1", "Value": "54019", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1999Q2", "Value": "55143", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Assets", "Period": "1999Q3", "Value": "56227", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total Current Liabilities", "Period": "1999Q3", "Value": "21804", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Balance", "ItemName": "Total shareholders\' equity", "Period": "1999Q3", "Value": "24679", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Income", "ItemName": "Revenues", "Period": "1999Q3", "Value": "21688", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Income", "ItemName": "Gross Profit", "Period": "1999Q3", "Value": "9925", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Income", "ItemName": "Opertaing", "Period": "1999Q3", "Value": "2393", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Income", "ItemName": "Net income", "Period": "1999Q3", "Value": "1670", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Income", "ItemName": "Retained Earnings", "Period": "1999Q3", "Value": "26688", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Income", "ItemName": """, "Period": "1999Q3", "Value": "1670", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Cash", "ItemName": "Net cash provided by operating activities", "Period": "1999Q3", "Value": "2457", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Cash", "ItemName": "Net cash used in investing activities", "Period": "1999Q3", "Value": "2239", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Cash", "ItemName": "Net cash used in financing activities", "Period": "1999Q3", "Value": "1628", "CompanyID": "K TRON INTERNATIONAL INC 20"}, {"Statement": "Cash", "ItemName": "CASH AND CASH EQUIVALENTS", "Period": "1999Q3", "Value": "1750", "CompanyID": "K TRON INTERNATIONAL INC 20"}]' //placeholder
  // ??? I'm still unsure how we actually get either the data itself, or the commands into the html file. Can htmls be called with arguments from code written in a different language?
  var parsed = []; // the array of parsed data
  var labels = []; // an array where each index contains three things: The company, the field, and the class of the field.
  var datas = []; // an array of arrays, containing the raw data to be put into each series
  var series = [];

  // converts dates in the form YYYYQq into a JavaScript time.
  convertDate = function (date){
    var d = String(date)
    var q = d[5]; // get the quarters
    q = 3*q; // convert to the appropriate month
    var y = d.substr(0,4);
    result = new Date(y, q, 1, 0, 0, 0, 0);
    return result;
  }
  
  // removes all instances of " from inside a string
  unquote = function (string){
    var res = "";
	for(var i = 0; i<string.length; i+=1){
	  var c = string[i];
	  if(c!='"'){
		res = res + string[i];
	  }
	}
	return res
  }

  // obtain the data in format: "[{"Statement": "Balance", "ItemName": "Total Assets", "Period": "1995Q0", "Value": null, "CompanyID": "K TRON INTERNATIONAL INC 20"}, ... ]"
  /* I HAVE NO IDEA HOW I DO THIS */
  
  // parse the data input
  rawdata = unquote(rawdata.substring(2,rawdata.length-3)); // strip data of ", and remove outside [{}]
  var rawdata = rawdata.split("}, {"); // parse into rows
  for(var i = 0; i<rawdata.length; i+=1){ // parse into two dimensional array of strings.
    var temp = rawdata[i].replace("CompanyID: ","").replace("Value: ","").replace("Period: ","").replace("ItemName: ","").replace("Statement: ","").split(", ") // remove tokens from each part
	parsed.push([]);
	parsed[i].push(temp[0]);
	parsed[i].push(temp[1]);
	parsed[i].push(temp[2]);
	parsed[i].push(temp[3]);
	parsed[i].push(temp[4]);
  }
  
  // convert the parsed data into a set of labels, and a set of x and y values to plot
  for(var i = 0; i<parsed.length; i+=1){
    var label = parsed[i][4]+": "+parsed[i][1]; // gets the three labels
	var value = parsed[i][3];
    if(parsed[i][0] == "Cash"){value = "-" + value;}	// I think the cash label means its an expenditure? If so, it sets the value to negative.
    var data = [convertDate(parsed[i][2]),value]; // gets y (time) and x (money) to plot
    var index = labels.indexOf(label); // find if label matches an existing series
    if(index<0){
      labels.push(label); // adds these labels to the array, updates index.
	  index = datas.push([]) -1; // create a new series
    }
    datas[index].push(data); // adds the data to the correct series
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