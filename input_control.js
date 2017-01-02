$(".mat-input").focus(function(){
  $(this).parent().addClass("is-active is-completed");
});

$(".mat-input").focusout(function(){
  if($(this).val() === "")
    $(this).parent().removeClass("is-completed");
  $(this).parent().removeClass("is-active");
});


var porn_list = [];
var porn_list_img = [];
var porn_list_val = [];

function addMachine(e) {
    if (e.keyCode == 13) {
		var tb = document.getElementById('first-name');
		if(tb.value){
			porn_list.push(tb.value);
			document.getElementById('first-name').value = "";
			$('.porn__tabs > ul').remove();
			$('.porn__tabs').append('<ul></ul>');
			for(i = 0; i < porn_list.length; i++){
				$('.porn__tabs > ul').append('<li class="porn__tab" id="' + porn_list[i] + '">' + porn_list[i] + '</li>');
			}
			listGet();
			return false;
		}
    }
};

function listGet(){
	$('.porn__box__container > ul').remove();
	$('.porn__box__container').append('<ul></ul>');
	for(i = 0; i < porn_list.length; i++){
		getScreenshots(porn_list[i],i);
	}
};

function getScreenshots(address,current) {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(request.readyState == 4){
			if(request.status == 200){
				var data = JSON.parse(request.responseText);
				var currentImg = data.photo.substring(2,data.photo.length-1);
				var currentValue = data.msg;
				if(currentValue==='Unknown MAC'){
					alert(currentValue);
					var id = '#' + address;
					$(id).remove();
					return false;
				}
				porn_list_img[current] = currentImg;
				porn_list_val[current] = Math.round(currentValue * 100);
				if(porn_list_val[current] > 80) {
					$('.porn__box__container > ul').append('<li class="porn__box danger" id="102' + porn_list[current] + '"><h2>' + porn_list[current] + '</h2><div class="section"><img src="data:img/png;base64,' + porn_list_img[current] + '" alt="nothing" id="100' + porn_list[current] + '" class="blur" onclick="showChart(' + porn_list[current] + ')"><h3 id="101' + porn_list[current] + '">色情率: ' + porn_list_val[current] + '%</h3></div></li>');
				}else{
					$('.porn__box__container > ul').append('<li class="porn__box safe" id="102' + porn_list[current] + '"><h2>' + porn_list[current] + '</h2><div class="section"><img src="data:img/png;base64,' + porn_list_img[current] + '" alt="nothing" id="100' + porn_list[current] + '" class="none" onclick="showChart(' + porn_list[current] + ')"><h3 id="101' + porn_list[current] + '">色情率: ' + porn_list_val[current] + '%</h3></div></li>');					
				}
				return false;
			}else{
				alert("error: " + request.status);
			}
		}
	}
	//alert(address);
	request.open("GET","http://140.113.89.234:8888/?MAC=" + address + "&PERIOD=0",true);
	request.send();
};

setInterval(update,3000);
function update(){
	for(i = 0; i < porn_list.length; i++){
		var request = new XMLHttpRequest();
		request.onreadystatechange = function(){
			if(request.readyState == 4){
				if(request.status == 200){
					var data = JSON.parse(request.responseText);
					var currentImg = data.photo.substring(2,data.photo.length-1);
					var currentValue = Math.round(data.msg * 100);
					var id_img = '#100' + porn_list[i-1];
					var id_val = '#101' + porn_list[i-1];
					var id_class = '#102' + porn_list[i-1];
					if(currentValue > 80){
						$(id_img).attr( "class", "blur" );
						$(id_class).attr( "class", "porn__box danger" );
					}else{
						$(id_img).attr( "class", "none" );
						$(id_class).attr( "class", "porn__box safe" );
					}
					$(id_img).attr( "src", "data:img/png;base64," + currentImg );
					$(id_val).html('色情率: ' + currentValue + '%');
					return false;
				}else{
					alert("error: " + request.status);
				}
			}
		}
		//alert(address);
		request.open("GET","http://140.113.89.234:8888/?MAC=" + porn_list[i] + "&PERIOD=0",true);
		request.send();
	}
}

function showChart(id){
	var request = new XMLHttpRequest();
	var period_count;
	var period_date;
	var start_point = [];
	var period_list = [];
			
	request.onreadystatechange = function(){
		if(request.readyState == 4){
			if(request.status == 200){
				var data = JSON.parse(request.responseText);
				period_count = data.total;
				period_date = data.periods[0].start.toString();
				period_date = period_date.substring(0,8);
				for(i = 0; i < (period_count/2); i++){
					var temp;
					temp = data.periods[i].start.toString();
					period_list.push(temp.substring(8,12));
					temp = data.periods[i].end.toString();
					period_list.push(temp.substring(8,12));
				}
				start_point.push(period_list[0].substring(0,2));
				start_point.push(period_list[0].substring(2,4));
				return false;
			}else{
				alert("error: " + request.status);
			}
		}
	}
	request.open("GET","http://140.113.89.234:8888/?MAC=" + id + "&PERIOD=1",true);
	request.send();
	
	$.colorbox({
		html:'<div id="chartContainer" style="height: 200px; width: 600px;"></div>',
		onComplete:function () {
			
			var chart = new CanvasJS.Chart("chartContainer", {
				title: {
					text: "Today's porn period"
				},
				animationEnabled: true,
				axisX: {
					interval: 1,
					labelFontSize: 10,
					lineThickness: 0
				},
				axisY2: {
					//valueFormatString: start_point[0] + ":" + start_point[1],
					//valueFormatString: "hh:mm",
					labelFormatter: function (e) {
						return CanvasJS.formatDate( e.value, "hh:mm");
					},
					lineThickness: 0
				},
				toolTip: {
					shared: false
				},
				legend: {
					verticalAlign: "top",
					horizontalAlign: "center"
				},
			
				data: [
					{
					type: "stackedBar",
					showInLegend: true,
					name: "Porn",
					axisYType: "secondary",
					color: "#F0E6A7",
					dataPoints: [{ y: 0, label: period_date }]
					},
					{
					type: "stackedBar",
					showInLegend: true,
					name: "Safe",
					axisYType: "secondary",
					color: "#7E8F74",
					dataPoints: [{ y: 0, label: period_date }]
					}
				]
			});
			var porn_flag = true;
			for(i = 1; i < period_count; i++){
				if(porn_flag == true){
					porn_flag = false;
					chart.options.data.push(
						{
							type: "stackedBar",
							name: "Porn",
							axisYType: "secondary",
							color: "#F0E6A7",
							dataPoints: [
								{ y: parseInt(period_list[i]) - parseInt(period_list[i-1]), label: period_date }
							]
						}
					);
				}else{
					porn_flag = true;
					chart.options.data.push(
						{
							type: "stackedBar",
							name: "Safe",
							axisYType: "secondary",
							color: "#7E8F74",
							dataPoints: [
								{ y: parseInt(period_list[i]) - parseInt(period_list[i-1]), label: period_date }
							]
						}
					);
				}
			}
			chart.render();
		}
	});
}