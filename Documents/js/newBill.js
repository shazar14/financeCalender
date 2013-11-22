$(document).ready(function() {
      	$("#pay_accounts").hide();
      	$("#monthly").hide();

	$('#newBillButton').click(function(sub){
		sub.preventDefault();
		var month_array = new Array();
		if($("#r_jan").is(':checked'))
			month_array.push('1');
		if($("#r_feb").is(':checked'))
			month_array.push('2');
		if($("#r_march").is(':checked'))
			month_array.push('3');
		if($("#r_april").is(':checked'))
			month_array.push('4');
		if($("#r_may").is(':checked'))
			month_array.push('5');
		if($("#r_jun").is(':checked'))
			month_array.push('6');
		if($("#r_jul").is(':checked'))
			month_array.push('7');
		if($("#r_aug").is(':checked'))
			month_array.push('8');
		if($("#r_sept").is(':checked'))
			month_array.push('9');
		if($("#r_oct").is(':checked'))
			month_array.push('10');
		if($("#r_nov").is(':checked'))
			month_array.push('11');
		if($("#r_dec").is(':checked'))
			month_array.push('12');

		var payHow = $("input:radio[name='status']:checked").val();
		var account = '';
		if( payHow == 'Manual')
			account = 'None';
		else
			account = $('#pay_accounts').val();
		debugger;		
		parameters = JSON.stringify({request:'addBill', name:$('#name').val(), amount:$('#amount').val(), dueDay:$('#dayOfMonth').val(), pay_type:payHow, pay_account:account, months:month_array, repeat:$("input:radio[name='repeating']:checked").val()});
		$.ajax({
			url: 'cgi-bin/command.py',
			type: 'POST',
			data: parameters,
			dataType: 'text',
			error: function(jqXHR, error, errorThrown){
				alert("Error submitting new account");
			},
			success: function(){
				location.reload();	
			}
		});
	});	

	$('#newAccountButton').click(function(sub1){
		sub1.preventDefault();
		parameters = JSON.stringify({request:'addAccount', account:$('#account').val()});

		$.ajax({
			url: 'cgi-bin/command.py',
			type: 'POST',
			data: parameters,
			dataType: 'text',
			error: function(jqXHR, error, errorThrown){
				alert("Error submitting new account");
			},
			success: function(){
				location.reload();
			}
		});
	});

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
				if(value != 'None')
				{
					$('#pay_accounts').append(
						$('<option></option>')
							.attr("value", value)
							.text(value));
				}
                        });
                }
        });
	$("#r_Auto, #r_Manual").change(function(){
    		if($(this).val() == 'Manual')
      			$("#pay_accounts").hide();
		else
      			$("#pay_accounts").show();
			
	});
	$("#r_monthly, #r_custom").change(function(){
    		if($(this).val() == 'monthly')
      			$("#monthly").hide();
		else
      			$("#monthly").show();
			
	});
});
