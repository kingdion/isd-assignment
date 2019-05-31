$(document).ready(function()
{
    // When updating the data, we use a PUT
    // request so the server knows
    // we are merely updating records. Send in
    // all of the inputs to change, redirect
    // on sucess or show error.
    $('#modify-update-form').submit(function(event)
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
            success: (data) =>
            {
                if (data.success)
                {
                    window.location.href = "/modify_user/"
                }
                else
                {
                    $(".error-message").text(data.message);
                }
            },
            error: (error) => { $("#error-message").text(JSON.parse(error.responseText).message) },
          });
    });

    // The delete account button handler - removes
    // the account and redirects.
    $('#delete-btn').click(() => {
        $.ajax({
          type: "DELETE",
          url: "/delete-user",
          success: (data) => { window.location.href = "/" },
          fail: (error) => { $("#error-message").text(JSON.parse(error.responseText).message) },
        });
    });
});
