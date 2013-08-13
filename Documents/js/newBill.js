$(document).ready(function() {
      	$("#pay_accounts").hide();

	$('#newBill').submit(function(sub){
		sub.preventDefault();
		alert("Not Working yet, fill out submit bill stuff");
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
