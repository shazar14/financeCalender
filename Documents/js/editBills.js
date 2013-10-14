dTableBills = null;

$(document).ready(function (){
	parameters = JSON.stringify({request:'billInfo'});
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
			var head = '<thead>' + 
			'<tr>' +
				'<th>Bill</th>' +
				'<th>Due</th>' + 
				'<th>Due Date</th>' + 
				'<th>Payment Type</th>' + 
				'<th>Payment Account</th>' + 
				'<th>Delete</th>' +
			'</tr>' +
			'</thead>' +
			'<tbody></tbody>';
			$('#currentBills').append(head);
			$.each(data, function(table, tableObject) {
				$.each(tableObject, function(key, value){
					row = '<tr>';
					row += '<td>' + value['name'] + '</td>' +
					'<td>' + value['amount'] + '</td>' +
					'<td>' + value['dayofmonth'] + '</td>' +
					'<td>' + value['paymentType'] + '</td>' +
					'<td>' + value['account'] + '</td>' +
					'<td><button class="buttonSQ" value="' +  value['id'] + '">Delete</button></td>'
					'</tr>';
					$('#currentBills').append(row);
				});
			});
			$('#currentBills').delegate('.buttonSQ', 'click', function(){
				submitVariable = $(this).val()
				parameters = JSON.stringify({request: "checkDelete", data:submitVariable});
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
						if(confirm("Delete " + data['name'] + "\nAmount:" + data['amount'] ))
						{
							parameters = JSON.stringify({request: "delete", data:submitVariable});
							$.ajax({
								url: 'cgi-bin/command.py',
								type: 'POST',
								data: parameters,
								dataType: 'text',
								error: function(jqXHR, error, errorThrown){
									alert("ERROR:" + jqXHR.responseText);
								},
								success: function(data){
									location.reload();
								}
							});
						}
					}
				});
			});
			dTableBills = $('#currentBills').dataTable({
				"bPaginate": false,
				"bFilter": false,
				"aaSorting":[[ 2, "asc"]]
			});
			

		}
	});
});
