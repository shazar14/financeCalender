$(document).ready(function() {
	parameters = JSON.stringify({request:'queryAll'});
	$('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month, basicWeek'
			},
			editable: true,
			viewDisplay: function() {
				$('#calendar').fullCalendar( 'removeEvents' );
				getBills();
    			}
		});

	function getBills()
	{
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
});
