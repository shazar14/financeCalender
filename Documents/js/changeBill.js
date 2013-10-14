$(document).ready(function() {

	$('#button').click(function(sub){
		submit = true;
		//perform some error checking
		if(!submit)
			sub.preventDefault();
		else
		{
			sub.preventDefault();
			parameters = JSON.stringify({stat : $("input:radio[name='billStatus']:checked").val(), pay_type : $("input:radio[name='status']:checked").val(), request : 'changeBill', bill : $('#bill').val(),  pay_method : $('#pay_method').val(), amount : $('#amount').val(), month : billDate});

			$.ajax({
				url: 'cgi-bin/command.py',
				type: 'POST',
				data: parameters,
				dataType: 'text',
				error: function(jqXHR, error, errorThrown){
					alert("Error submitting change bill");
				},
				success: function(){
					parent.$('#calendar').fullCalendar( 'removeEvents' );
					parent.$.fancybox.close();
					parent.getBills();
					parent.tables();
				}
			});
		}

	});
	$('#button2').click(function(sub){
		submit = true;

		if(!submit)
			sub.preventDefault();
		else
			parameters = JSON.stringify({stat : $("input:radio[name='billStatus']:checked").val(), pay_type : $("input:radio[name='status']:checked").val(), request : 'changeAllBill', bill : $('#bill').val(),  pay_method : $('#pay_method').val(), amount : $('#amount').val(), month : billDate});
			url: 'cgi-bin/command.py',
			type: 'POST',
			data: parameters,
			dataType: 'text',
			error: function(jqXHR, error, errorThrown){
				alert("Error submitting change bill");
			},
			success: function(){
				parent.$('#calendar').fullCalendar( 'removeEvents' );
				parent.$.fancybox.close();
				parent.getBills();
				parent.tables();
			}
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
			alert("Error getting accounts");
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

	var billName = $('#billName').val();
	var billDate = $('#billDate').val();
	parameters = JSON.stringify({request:'getBill', bill:billName, date:billDate});
	$.ajax({
		url: 'cgi-bin/command.py',
		type: 'POST',
		data: parameters,
		dataType: 'text',
		error: function(jqXHR, error, errorThrown){
			alert("Error loading page");
		},
		success: function(data){
			$('#bill').val(billName);
			data = $.parseJSON(data);
			$('#amount').val(data['amount']);

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
