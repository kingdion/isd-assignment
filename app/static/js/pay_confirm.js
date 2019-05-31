$(document).ready(function(){
    $('#payconf-form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: $('#payconf-form').attr('action'),
            data: {dfirst : $("[name=dfirst]").val(), dlast : $("[name=dlast]").val(), daddress : $("[name=daddress]").val(), dpostcode : $("[name=dpostcode]").val(), cname : $("[name=cname]").val(), creditno : $("[name=creditno]").val(), cvc : $("[name=cvc]").val(), month : $("[name=month]").val(), year : $("[name=year]").val(), bfirst : $("[name=bfirst]").val(), blast : $("[name=blast]").val(), baddress : $("[name=baddress]").val(), bpostcode : $("[name=bpostcode]").val()},
            success: (data) => 
            { 
                if (data.success) 
                { 
                    window.location.href = "/browse" 
                    var myObj = { firsname : "John", lastname : "Doe" };
                    console.log(myObj);
                } 
                else 
                { 
                    window.location.href = "/login"
                    var myObj = { firsname : "No", lastname : "work" };
                    console.log(myObj);
                }
            },
          });

        if (validate_form()) {
            
            $.post($(this).attr('action'), $(this).serialize());
        }
        
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


