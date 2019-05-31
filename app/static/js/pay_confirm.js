$(document).ready(function(){
    $('#payconf-form').submit(function(event) {
        event.preventDefault();
     
        
  });

    // The delete account button handler - removes
    // the account and redirects.
    $('#delete-btn').click(() => {
        $.ajax({
          type: "DELETE",
          url: "/delete-payment",
          success: (data) => { window.location.href = "/" },
          fail: (error) => { $("#error-message").text(JSON.parse(error.responseText).message) },
            }); 
        });
    });


