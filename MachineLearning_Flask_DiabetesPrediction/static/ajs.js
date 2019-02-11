
function check(e){
		 $.ajax({
            url: '/diabetesPredictionApi',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
               if (response=='yes') {
                $('#btnGreen1').prop('disabled', true);
              $('#btnRed').prop('disabled', false);
 
               //alert("You have the possibility of diabetes. Consult your doctor immediately")

            }else{
            $('#btnGreen1').prop('disabled', false);
               $('#btnRed').prop('disabled', true);
			  
             // alert("No Diabetes. Keep the good healthy habit")
            }
            },
            error: function(error) {
                console.log(error);
            }
        });
		  e.preventDefault();
      e.stopPropagation();
	}
