dTableAnalytics = null;
dTableMonth = null;
dTableMonths = null;

month = 0;
billName = '';

function calcDaysInMonth(month)
{
	if( month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12)
		return 31
	else if( month == 2 )
		return 28
	else
		return 30  
}

function calcWeek(firstDay, month, year)
{
	var daysInMonth = calcDaysInMonth(month);
	var week = parseInt(firstDay)+6;
	var newYear = parseInt(year);
	if(week > daysInMonth)
	{
		week = week - daysInMonth;
		month = parseInt(month) + 1;
		if(month > 12)
		{
			month = parseInt(month) - 12;
			newYear = newYear + 1;
		}
		return [week, month, newYear];
	}
	else
		return [week, month, newYear];
}
function getBills()
{
      parameters = JSON.stringify({request:'queryAll'});
      $.ajax({
	url: 'cgi-bin/command.py',
	type: 'POST',
	data: parameters,
	dataType: 'text',
	error: function(jqXHR, error, errorThrown){
	    alert("ERROR:" + jqXHR.responseText);
	},
	success: function(data){ //data is in custom JSON object.  See database_transactions.py for definition
		data = $.parseJSON(data);
		var eventArray = new Array();
		var index = 0; 
		$.each(data, function(table, tableObject) {		
			$.each(tableObject, function(key, value){

				//current month events
				var newEvent = new Object();
				newEvent.title = value['currentTitle'];
				newEvent.start = value['currentDate'];
				if(value['currentStatus'] == 'Due' && value['status'] == 'Automatic')
				{
					newEvent.color = 'orange';
					newEvent.title += " [" + value['account'] + "]";
				}
				else if(value['currentStatus'] == 'Due' && value['status'] == 'Manual')
				{
					newEvent.color = 'red';
				}
				else if(value['currentStatus'] == 'Paid')
				{
					newEvent.color = 'blue';
				}
				else if(value['currentStatus'] == 'Skip')
				{
					newEvent.color = 'green';
				}
				$('#calendar').fullCalendar( 'renderEvent', newEvent );

			});
		});
	}
      });
}
function tables()
{
	//Calculate the 6 weeks shown on all the calendars
	var startDate = $.fullCalendar.formatDate($('#calendar').fullCalendar('getView').visStart, 'M dd yyyy');
	var calArray = new Array(parseInt(startDate.split(" ")[0]), parseInt(startDate.split(" ")[1]), parseInt(startDate.split(" ")[2]));

	for(var i=0; i<6; i++)
	{
		//debugger;
		dates = calcWeek(calArray[calArray.length-2], calArray[calArray.length - 3], calArray[calArray.length - 1]);
		calArray.push(dates[1]); //month
		calArray.push(dates[0]); //day
		calArray.push(dates[2]); //year
		if(i != 5)
		{
			if((dates[0] + 1) > calcDaysInMonth(dates[1]))
			{
				if(dates[1] == 12)
					calArray.push(1);
				else
					calArray.push(dates[1] + 1);
				calArray.push(1);
				if(dates[1] == 12)
					calArray.push(dates[2] + 1);
				else
					calArray.push(dates[2]);
			}
			else
			{
				calArray.push(dates[1]);
				calArray.push(dates[0] + 1);
				calArray.push(dates[2]);
			}
		}
	}
	parameters = JSON.stringify({request:'getMonths', startMonth:startDate.split(" ")[0], year:$('#calendar').fullCalendar('getView').title.split(" ")[1]});
	$.ajax({
		url: 'cgi-bin/command.py',
		type: 'POST',
		data: parameters,
		dataType: 'text',
		error: function(jqXHR, error, errorThrown){
		    alert("ERROR:" + jqXHR.responseText);
		},
		success: function(data){
			data = $.parseJSON(data);
			if(dTableMonths != null)
				dTableMonths.fnClearTable();
			else
			{
				dTableMonths = $('#months').dataTable( {
					"bPaginate": false,
					"bSort": false,
					"bFilter": false,
					"bInfo": false,
					"bAutoWidth":true
				});
			}
			dTableMonths.fnAddData( [
				[ data['month1'], data['month1Total'] ],
				[ data['month2'], data['month2Total'] ],
				[ data['month3'], data['month3Total'] ]
			]);
		}
	});

	parameters = JSON.stringify({request:'6weeks', weeksArray:calArray});
	$.ajax({
		url: 'cgi-bin/command.py',
		type: 'POST',
		data: parameters,
		dataType: 'text',
		error: function(jqXHR, error, errorThrown){
		    alert("ERROR:" + jqXHR.responseText);
		},
		success: function(data){
			data = $.parseJSON(data);
			if(dTableAnalytics != null){
				dTableAnalytics.fnClearTable();
			}
			else
			{
				dTableAnalytics = $('#analytics').dataTable( {
					"bPaginate": false,
					"bSort": false,
					"bFilter": false,
					"bInfo": false,
					"bAutoWidth": true
				});
			}
			dTableAnalytics.fnAddData( [ 
				[ data['Date1'], data['week1'], data['week1Due'] ],
				[ data['Date2'], data['week2'], data['week2Due'] ],
				[ data['Date3'], data['week3'], data['week3Due'] ],
				[ data['Date4'], data['week4'], data['week4Due'] ],
				[ data['Date5'], data['week5'], data['week5Due'] ],
				[ data['Date6'], data['week6'], data['week6Due'] ]
			]);
			if(dTableMonth != null)
				dTableMonth.fnClearTable();
			else
			{
				dTableMonth = $('#month').dataTable( {
					"bPaginate": false,
					"bSort": false,
					"bFilter": false,
					"bInfo": false
				});
			}
			dTableMonth.fnAddData( [ data['calendarCost'], data['calendarDue'] ] );
		}
	});

}
$(document).ready(function() {
	$('#calendar').fullCalendar({
		height: 700,
		windowResize: false,
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month, basicWeek'
		},
		editable: true,
		viewDisplay: function() {
			$('#calendar').fullCalendar( 'removeEvents' );
			getBills();
			tables();
		},
		eventDrop: function(event,dayDelta,minuteDelta,allDay,revertFunc) {

			var monthToChange = $.fullCalendar.formatDate( event.start, "M");
			var dayToChange = $.fullCalendar.formatDate( event.start, "d");

			parameters = JSON.stringify({"request":"changeDay", "dayToChange":dayToChange, "month":monthToChange,"title":event.title}); 
			$.ajax({
				url: 'cgi-bin/command.py',
				type: 'POST',
				data: parameters,
				dataType: 'text',
				error: function(jqXHR, error, errorThrown){
				    alert("ERROR:" + jqXHR.responseText);
				},
				success: function(){ 
					tables();
				}
	
		    	});
		},
		eventClick: function(calEvent, jsEvent, view) {

			month = $.fullCalendar.formatDate( calEvent.start, "M");
			billName = calEvent.title.split(':')[0]
			$.fancybox({
			    'width': '40%',
			    'height': '40%',
			    'autoScale': true,
			    'transitionIn': 'fade',
			    'transitionOut': 'fade',
			    'type': 'iframe',
			   // 'href': 'changeBill.php?bill=' + calEvent.title.split(':')[0] + '&date=' + date + ''
			    'href': 'changeBill.html'
			});
		}
	});
});
