$(document).ready(function() {
    $('select').select2({ theme: "bootstrap", width: "resolve" });
    $('[name="genres[]"]').select2({ placeholder: "Genres", theme: "bootstrap", width: "resolve" });
    $('[data-toggle="tooltip"]').tooltip({ trigger: 'hover' });
    $('#body-content').css('opacity', 1);
});

$('#movie-form').submit(function(event) {
    event.preventDefault();
    $.post($(this).attr('action'), $(this).serialize(), add_edit_movie_callback);
});

function add_edit_movie_callback(data) {
    if (data.success) {
        alert("Movie successfully added!");
        $('#movie-form')[0].reset();
        $('select').trigger('change');
    }
}
