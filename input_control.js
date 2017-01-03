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
				if(porn_list_val[current] > 30) {
					$('.porn__box__container > ul').append('<li class="porn__box danger" id="102' + porn_list[current] + '"><h2>' + porn_list[current] + '</h2><div class="section"><img src="data:img/png;base64,' + porn_list_img[current] + '" alt="nothing" id="100' + porn_list[current] + '" class="blur" onclick="showChart(' + porn_list[current] + ')"><h3 id="101' + porn_list[current] + '">色情率: ' + porn_list_val[current] + '%</h3></div></li>');
				}else{
					$('.porn__box__container > ul').append('<li class="porn__box safe" id="102' + porn_list[current] + '"><h2>' + porn_list[current] + '</h2><div class="section"><img src="data:img/png;base64,' + porn_list_img[current] + '" alt="nothing" id="100' + porn_list[current] + '" class="none" onclick="showChart(' + porn_list[current] + ')"><h3 id="101' + porn_list[current] + '">色情率: ' + porn_list_val[current] + '%</h3></div></li>');					
				}
				return false;
			}else{
				var id = '#' + address;
				$(id).remove();
				alert("error: " + request.status);
			}
		}
	}
	request.open("GET","http://140.113.89.234:8888/?MAC=" + address + "&PERIOD=0",true);
	request.send();
};

setInterval(update,5000);
function update(){
	for(var i = 0; i < porn_list.length; i++){
		(function (i) {
			var request = new XMLHttpRequest();
			request.onreadystatechange = function(){
			if(request.readyState == 4){
				if(request.status == 200){
					var data = JSON.parse(request.responseText);
					var currentImg = data.photo.substring(2,data.photo.length-1);
					var currentValue = Math.round(data.msg * 100);
					var id_img = '#100' + porn_list[i];
					var id_val = '#101' + porn_list[i];
					var id_class = '#102' + porn_list[i];
					console.log(i);
					if(currentValue > 30){
						$(id_img).attr( "class", "blur" );
						$(id_class).attr( "class", "porn__box danger" );
					}else{
						$(id_img).attr( "class", "none" );
						$(id_class).attr( "class", "porn__box safe" );
					}
					$(id_img).attr( "src", "data:img/png;base64," + currentImg );
					$(id_val).html('色情率: ' + currentValue + '%');
				}else{
					alert("error: " + request.status);
				}
			}	
			}
			request.open("GET","http://140.113.89.234:8888/?MAC=" + porn_list[i] + "&PERIOD=0",true);
			request.send();
		})(i);
	}
}

function showChart(id){
	var request = new XMLHttpRequest();
	var period_count;
	var period_date_yesterday;
	var period_date_today;
	var period_list_yesterday = [];
	var period_list_today = [];
	period_list_yesterday.push("0");
	period_list_today.push("0");
	var img_list_yesterday = [];
	var img_list_today = [];
	var total_time = 0;
			
	request.onreadystatechange = function(){
		if(request.readyState == 4){
			if(request.status == 200){
				var data = JSON.parse(request.responseText);
				period_count = data.periods.length;
				period_date_today = data.periods[period_count-1].start.toString();
				period_date_today = period_date_today.substring(0,8);
				period_date_yesterday = (parseInt(period_date_today)-1).toString();
				total_time = data.total;
				for(i = 0; i < period_count; i++){
					var temp_start;
					var temp_end;
					var temp_img;
					temp_start = data.periods[i].start.toString();
					temp_end = data.periods[i].end.toString();
					temp_img = data.periods[i].photo;
					if(temp_start.substring(0,8) == period_date_today){
						period_list_today.push(temp_start.substring(8,12));
						period_list_today.push(temp_end.substring(8,12));
						img_list_today.push(temp_img);
					}else if(temp_start.substring(0,8) == period_date_yesterday){
						period_list_yesterday.push(temp_start.substring(8,12));
						period_list_yesterday.push(temp_end.substring(8,12));
						img_list_yesterday.push(temp_img);
					}
				}
				$.colorbox({
					html:'<div id="chartContainer" style="height: 200px; width: 1200px;"></div>',
					onComplete:function () {
						var chart = new CanvasJS.Chart("chartContainer", {
							title: {
								text: "Today's porn period (total: " + total_time + "min)"
							},
							animationEnabled: true,
							axisX: {
								interval: 1,
								labelFontSize: 10,
								lineThickness: 0
							},
							axisY2: {
								valueFormatString: "00:00",
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
								color: "#FA8072",
								dataPoints: 
								[
									{ y: 0, label: period_date_yesterday },	
									{ y: 0, label: period_date_today }							
								]
								},
								{
								type: "stackedBar",
								showInLegend: true,
								name: "Safe",
								axisYType: "secondary",
								color: "#FFE1C7",
								dataPoints: 
								[
									{ y: 0, label: period_date_yesterday },	
									{ y: 0, label: period_date_today }	
								]
								}
							]
						});
						var porn_flag = 0;
						for(i = 1; i < period_list_yesterday.length; i++){
							if(porn_flag == 1){
								porn_flag = 0;
								chart.options.data.push(
									{
										type: "stackedBar",
										name: "Porn",
										axisYType: "secondary",
										color: "#FA8072",
										dataPoints: [
											{ x: 0, y: parseInt(period_list_yesterday[i]) - parseInt(period_list_yesterday[i-1]), label: period_date_yesterday }
										],
										click: function(e){
											for(j = 1; j < period_list_yesterday.length; j++){
												var p = parseInt(period_list_yesterday[j]) - parseInt(period_list_yesterday[j-1]);
												if(e.dataPoint.y == p){					
													periodImg(img_list_yesterday[j/2-1]);
													break;
												}
											}
										}
									}
								);
							}else{
								porn_flag = true;
								chart.options.data.push(
									{
										type: "stackedBar",
										name: "Safe",
										axisYType: "secondary",
										color: "#FFE1C7",
										dataPoints: [
											{ x: 0, y: parseInt(period_list_yesterday[i]) - parseInt(period_list_yesterday[i-1]), label: period_date_yesterday }
										]
									}
								);
							}
						}
						porn_flag = 0;
						for(i = 1; i < period_list_today.length; i++){
							if(porn_flag == 1){
								porn_flag = false;
								chart.options.data.push(
									{
										type: "stackedBar",
										name: "Porn",
										axisYType: "secondary",
										color: "#FA8072",
										dataPoints: [
											{ x: 1, y: parseInt(period_list_today[i]) - parseInt(period_list_today[i-1]), label: period_date_today }
										],
										click: function(e){
											for(j = 1; j < period_list_today.length; j++){
												var p = parseInt(period_list_today[j]) - parseInt(period_list_today[j-1]);
												if(e.dataPoint.y == p){
													periodImg(img_list_today[j/2-1]);
													break;
												}
											}
										}
									}
								);
							}else{
								porn_flag = true;
								chart.options.data.push(
									{
										type: "stackedBar",
										name: "Safe",
										axisYType: "secondary",
										color: "#FFE1C7",
										dataPoints: [
											{ x: 1, y: parseInt(period_list_today[i]) - parseInt(period_list_today[i-1]), label: period_date_today }
										]
									}
								);
							}
						}
						chart.render();
					}
				});
			}else{
				alert("error: " + request.status);
			}
		}
	}
	request.open("GET","http://140.113.89.234:8888/?MAC=" + id + "&PERIOD=1",true);
	request.send();
}

function periodImg(img_data){
	$(document).ready(function(){
		$.colorbox({
			html:'<img id="myImg" src="data:img/png;base64,' + img_data + '" width="800" height="500" class="blur">'
		});
	});
}