$(document).ready(function()
{
    $('#registration-update-form').submit(function(event) 
    {
        event.preventDefault();

        $.ajax({
            type: "PUT",
            url: $(this).attr('action'),
            data: 
            {
                first_name : $("[name=first-name]").val(),
                last_name : $("[name=last-name]").val(),
                street_address : $("[name=street-address]").val(),
                postcode : $("[name=postcode]").val(),
                phone_number : $("[name=phone-number]").val(),
            },
            success: (data) => { window.location.href = "/profile" },
            error: (error) => { $("#error-message").text(JSON.parse(error.responseText).message) },
          });
    });

    $('#delete-btn').click(() => {
        $.ajax({
          type: "DELETE",
          url: "/delete-account",
          success: (data) => { window.location.href = "/" }, 
          fail: (error) => { $("#error-message").text(JSON.parse(error.responseText).message) },
        }); 
    });
});