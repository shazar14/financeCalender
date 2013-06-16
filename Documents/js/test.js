jQuery(document).ready(function(){
	jQuery.ajax({
		url: 'cgi-bin/database_interact.rb',
		type: 'POST',
		data: 'function2',
		dataType: 'text',
		success: function(response)
		{
			$('#test').hide();
			$('#test').html(response);
			$('#test').show();
		},
		error: function()
		{
			alert("error");
		}
	});
});
