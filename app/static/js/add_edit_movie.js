$(document).ready(function() {
    $('select').select2({ theme: "bootstrap", width: "resolve" });
    $('[name="genres[]"]').select2({ placeholder: "Genres", theme: "bootstrap", width: "resolve" });
    $('#body-content').css('opacity', 1);

    $('[name="title"]').focusout(function(){ validate_not_empty($(this)); });
    $('[name="release-date"]').focusout(function(){ validate_not_empty($(this)); });
    $('[name="runtime"]').focusout(function(){ validate_not_empty($(this)); });

    fileInput = $('#image-file');
    fileInput.on('dragenter', function(event) {
        $('#file-name-container').addClass('dragover');
    });

    fileInput.on('dragleave', function(event) {
        $('#file-name-container').removeClass('dragover');
    });

    fileInput.on('change', function(event) {
        $('#file-name').text(fileInput.val().split('\\').pop());
        $('#file-name-container').removeClass('dragover');
        $('#file-name-container').css('border', 'none');
        $('#image-preview').attr('src', window.URL.createObjectURL(document.getElementById('image-file').files[0]));
        $('#image-preview').css('display', 'block');
        $('#file-name').css('background-color', 'rgba(0, 0, 0, 0.8)');
        $('#file-name').css('color', 'white');
    });
});

$('#movie-form').submit(function(event) {
    event.preventDefault();
    $.ajax({
        url: $('#movie-form').attr('action'),
        type: 'POST',
        data: new FormData($('#movie-form')[0]),
        cache: false,
        contentType: false,
        processData: false,
        success: add_edit_movie_callback
    });
});

function add_edit_movie_callback(data) {
    if (data.success) {
        alert("Save successful!");
        location.reload();
    }
    else {
        if (data.reason == 'movie exists') {
            set_warning($('[name="title"]'), "A movie with that title and release date already exists");
        }
        else if (data.reason == 'incomplete form') {
            alert("The save failed due to the form being incomplete. Please fill all fields.");
        }
        else {
            alert("Undefined server error: " + data.reason);
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
