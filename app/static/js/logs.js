$(document).ready(function()
{
    $('.delete-log').click(function(event) 
    {
        event.preventDefault();

        var ids = $(this).attr("id");

        $.ajax({
            type: "DELETE",
            url: "/delete-log",
            data: {log_id : ids},
            success: (data) => { $(this).parent().parent().fadeOut('slow') },
            error: (error) => { $(".error-message").text(JSON.parse(error.responseText).message) },
          });
    });

    $("#date-time-picker-button").click(function(event)
    {
        var dateToFilterBy = $("#date-time-picker").val();

        $('.log > .timestamp > .inner-date').each(function(i, obj) 
        {
            var rowParent = $(this).parent().parent().parent();
            if (!$(this).text().includes(dateToFilterBy))
            {
                rowParent.fadeOut();
            }
            else 
            {
                rowParent.fadeIn();
            }
        });
    });
});