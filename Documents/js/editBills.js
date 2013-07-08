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
					'</tr>';
					$('#currentBills').append(row);
				});
			});
			var tbl = $('#currentBills');
			var obj = $.paramquery.tableToArray(tbl);
			var newObj = {
				editModel: { clicksToEdit: 2 },
				width: 900,
				flexHeight: true,
				title: "Current Bills"
			};

			newObj.dataModel = { data: obj.data, sortIndx: 2, rPP:20, paging: "local" };
			newObj.colModel = obj.colModel;
			$.extend(newObj.colModel[0], {flexWidth: 200});
			$.extend(newObj.colModel[1], {width: 100});
			var $grid = $('#currentBills').pqGrid(newObj);
			

		}



	});








});
