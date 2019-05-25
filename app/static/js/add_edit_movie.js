$(document).ready(function() {
    $('select').select2({ theme: "bootstrap", width: "resolve" });
    $('[name="genres[]"]').select2({ placeholder: "Genres", theme: "bootstrap", width: "resolve" });
    $('#body-content').css('opacity', 1);

    $('[name="title"]').focusout(function(){ validate_not_empty($(this)); });
    $('[name="release-date"]').focusout(function(){ validate_not_empty($(this)); });
    $('[name="runtime"]').focusout(function(){ validate_not_empty($(this)); });
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
    else {
        if (data.reason == 'movie exists') {
            set_warning($('[name="title"]'), "A movie with that title and release date already exists");
        }
    }
}

function set_warning(el, warning) {
    el.tooltip('hide')
      .css('border', '1px solid red')
      .prop('title', warning)
      .attr('data-original-title', warning)
      .tooltip('show');
}

function clear_warning(el) {
    el.css('border', '1px solid #ced4da')
      .prop('title', '')
      .attr('data-original-title', '')
      .tooltip('hide');
}

function validate_not_empty(el) {
    if (el.val().length == 0) {
        set_warning(el, 'Required field.');
        return false;
    }
    else {
        clear_warning(el);
        return true;
    }
}
