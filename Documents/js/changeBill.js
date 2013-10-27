$(document).ready(function() {
	
	$('#currentMonthButton').click(function(sub){
		sub.preventDefault();
		parameters = JSON.stringify({stat : $("input:radio[name='billStatus']:checked").val(), request : 'changeBill', bill : $('#bill').val(), amount : $('#amount').val(), month : billDate});

		$.ajax({
			url: 'cgi-bin/command.py',
			type: 'POST',
			data: parameters,
			dataType: 'text',
			error: function(jqXHR, error, errorThrown){
				alert("Error submitting change bill: " + error + errorThrown + jqXHR );
			},
			success: function(){
				parent.$('#calendar').fullCalendar( 'removeEvents' );
				parent.$.fancybox.close();
				parent.getBills();
				parent.tables();
			}
		});

	});
	$('#futureMonthButton').click(function(sub){
		sub.preventDefault();
		pars = JSON.stringify({oldBillName: billName, stat : $("input:radio[name='billStatus']:checked").val(), pay_type : $("input:radio[name='status']:checked").val(), request : 'changeAllBill', bill : $('#bill').val(),  pay_method : $('#pay_method').val(), amount : $('#billAmount').val(), month : billDate, day : $('#day').val()});
		$.ajax({
			url: 'cgi-bin/command.py',
			type: 'POST',
			data: pars,
			dataType: 'text',
			error: function(jqXHR, error, errorThrown){
				alert("Error submitting future change bill: " + errorThrown);
			},
			success: function(){
				parent.$('#calendar').fullCalendar( 'removeEvents' );
				parent.$.fancybox.close();
				parent.getBills();
				parent.tables();
			}
		})
	});
	/*$('#editBill').submit(function(sub){
	});*/
	$('#button').button();
	parameters = JSON.stringify({request:'getAccounts'});
	$.ajax({
		url: 'cgi-bin/command.py',
		type: 'POST',
		data: parameters,
		dataType: 'text',
		error: function(jqXHR, error, errorThrown){
			alert("Error getting accounts: changebill");
		},
		success: function(data){
			data = $.parseJSON(data); 
			$.each(data, function(key, value){
				$('#pay_method').append(
					$('<option></option>')
						.attr("value", value)
						.text(value));
			});
		}
	});

	var billName = parent.billName;
	var billDate = parent.month;;
	parameters = JSON.stringify({request:'getBill', bill:billName, date:billDate});
	$.ajax({
		url: 'cgi-bin/command.py',
		type: 'POST',
		data: parameters,
		dataType: 'text',
		error: function(jqXHR, error, errorThrown){
			alert("Error loading page: changebill");
		},
		success: function(data){
			$('#bill').val(billName);
			data = $.parseJSON(data);
			$('#amount').val(data['amount']);
			$('#billAmount').val(data['amount']);
			$('#day').val(data['day'])
			//Set the payment type
			if(data['pay_type'] == 'Automatic')
			{
				$('#r_Auto').attr("checked", "checked");
				$('#pay_method').val(data['account']);
			}
			else if(data['pay_type'] == 'Manual')
			{
				$('#r_Manual').attr("checked", "checked");
				$('#pay_method').val('None');
			}		

			//Set the bill status
			if(data['status'] == 'Paid')
				$('#r_Paid').attr("checked", "checked");
			else if(data['status'] == 'Due')
				$('#r_Due').attr("checked", "checked");
			else if(data['status'] == 'Skip')
				$('#r_Skip').attr("checked", "checked");

		}
	});	

});
