$(document).ready(function()
{
    $('#login-form').submit(function(event) 
    {
        event.preventDefault();

        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: {email : $("[name=email]").val(), password : $("[name=password]").val()},
            success: (data) => { window.location.href = '/dashboard'; },
            error: (error) => { $(".error-message").text(JSON.parse(error.responseText).message) },
          });
    });
});