$(document).ready(function()
{
    // When you click on the individual row
    // to delete a log, send a DELETE request
    // to the server to remove the row.
    // The ID of the log is injected into the
    // html of the user row so we can pull it
    // out here and use it as an argument.

    $('.delete-account').click(function(event)
    {
        event.preventDefault();

        var ids = $(this).attr("id");

        $.ajax({
            type: "DELETE",
            url: "/delete-user",
            data: {account_id : ids},
            success: (data) => { $(this).parent().parent().fadeOut('slow') },
            fail: (error) => { $("#error-message").text(JSON.parse(error.responseText).message) },
          });
    });

    $("#modify-user-btn").click(function()
    {
        event.preventDefault();
        window.location.href = "/modify_user/" + $(this).parent().parent().attr('id');
    });

    $("#user-filter-button").click(function(event)
    {
        // Gets the value for the inputted data
        var dataToFilterBy = $("#user-filter").val();

        // For each account , check if the name of the input
        // is equal to a user's name. Fade out the row if
        // it is not equal to the filter.
        $('.account > .user > .name').each(function(i, obj)
        {
            var rowParent = $(this).parent().parent();

            if ($(this).text().includes(dataToFilterBy))
            {
                rowParent.fadeIn();
            }
            else
            {
                rowParent.fadeOut();
            }
        });
    });
});
