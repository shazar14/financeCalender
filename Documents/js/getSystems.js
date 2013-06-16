$(function(){
	$.ajax({
		url: 'cgi-bin/database_interact.rb',
		dataType: 'text',
		type: 'POST',
		error: function(){
			alert("ERROR");
		},
		success: function(data){
			alert(data);
		}
	});




});
