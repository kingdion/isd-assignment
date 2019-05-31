$(document).ready(function()
{

    $('.delete-movie-order').click(function(event)
    {
        event.preventDefault();

        var ids = $(this).attr("id");

        $.ajax({
            type: "DELETE",
            url: "/do-delete-movie-order",
            data: {movie_id : ids},
            success: (data) => { $(this).parent().parent().fadeOut('slow') },
            error: (error) => { $(".error-message").text(JSON.parse(error.responseText).message) },
          });
    });

});
