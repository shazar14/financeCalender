$(document).ready(function() {
      	$("#pay_accounts").hide();
      	$("#months").hide();

	$('#newBillButton').click(function(sub){
		sub.preventDefault();
		var month_array = new Array();
		if($("#r_jan").is(':checked'))
			month_array.push('January');
		if($("#r_feb").is(':checked'))
			month_array.push('February');
		if($("#r_march").is(':checked'))
			month_array.push('March');
		if($("#r_april").is(':checked'))
			month_array.push('April');
		if($("#r_may").is(':checked'))
			month_array.push('May');
		if($("#r_jun").is(':checked'))
			month_array.push('June');
		if($("#r_jul").is(':checked'))
			month_array.push('July');
		if($("#r_aug").is(':checked'))
			month_array.push('August');
		if($("#r_sept").is(':checked'))
			month_array.push('September');
		if($("#r_oct").is(':checked'))
			month_array.push('October');
		if($("#r_nov").is(':checked'))
			month_array.push('November');
		if($("#r_dec").is(':checked'))
			month_array.push('December');
		

		parameters = JSON.stringify({request:'addBill', name:$('#name').val(), amount:$('#amount').val(), dueDay:$('#dayOfMonth').val(), pay_type:$("input:radio[name='status']:checked").val(), pay_account:$('#pay_accounts').val(), months:month_array, repeat:$("input:radio[name='repeating']:checked").val()});
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
	$("#r_monthly, #r_custom").change(function(){
    		if($(this).val() == 'monthly'){
      			$("#months").hide();
    		}
		else
      			$("#months").show();
			
	});
});
