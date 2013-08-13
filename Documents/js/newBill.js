$(document).ready(function() {
      	$("#pay_accounts").hide();

	$('#newBillButton').click(function(sub){
		sub.preventDefault();

		parameters = JSON.stringify({request:'addBill', name:$('#name').val(), amount:$('#amount').val(), dueDay:$('#dayOfMonth').val(), pay_type:$("input:radio[name='status']:checked").val(), pay_account:$('#pay_accounts').val()});
		$.ajax({
			url: 'cgi-bin/command.py',
			type: 'POST',
			data: parameters,
			dataType: 'text',
			error: function(jqXHR, error, errorThrown){
				alert("Error submitting new account");
			},
			success: function(){ alert('yo');}
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
			success: function(){}
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
                                $('#pay_accounts').append(
                                        $('<option></option>')
                                                .attr("value", value)
                                                .text(value));
                        });
                }
        });
	$("#r_Auto, #r_Manual").change(function(){
    		if($(this).val() == 'Manual'){
      			$("#pay_accounts").hide();
    		}
		else
      			$("#pay_accounts").show();
			
	});
});
