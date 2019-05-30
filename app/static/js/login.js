$(document).ready(function()
{
    $('#login-form').submit(function(event) 
    {
        event.preventDefault();

        // When the login button is pressed, submit a post 
        // request with the username/password fields. 
        // Redirect on success, show errors on error.

        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: {username : $("[name=username]").val(), password : $("[name=password]").val()},
            success: (data) => 
            { 
                if (data.success) 
                { 
                    window.location.href = "/browse" 
                } 
                else 
                { 
                    $(".error-message").text(data.message);
                }
            },
            error: (error) => { $(".error-message").text(JSON.parse(error.responseText).message) },
          });
    });
});