$(document).ready(function() {
	alert("Loading...");
	parameter = JSON.stringify({request:'queryAll'});
	$.ajax({
		url: 'cgi-bin/command.py',
	      	type: 'POST',
	      	data: parameter,
	      	dataType: 'text',
	      	error: function(jqXHR, error, errorThrown){
		  	alert("ERROR:" + jqXHR.responseText);
	      	},
	      	success: function() {
			alert("Hello World");
		}
	});



}
