


$(document).ready(function(){
	$('#submit').off('click').on('click', function () {
		var img = $("#blah").attr("src");
		if (img){
			var img_name = $("#imgInp")[0].files[0].name;
			$.ajax({
				data: {
					img_name: img_name
				},
				type: 'POST',
				url : '/predict',
				success: function(response){
					$('#display').text("Prediction expression: "+response.expression).show();
					$('#result').text("Result: "+response.result).show();
				},
				error: function(errormessage){
					alert("Invalid expression or an error occurred!")
				}
			});
		}
		else
			alert("You have not selected a photo!");
	});
});
