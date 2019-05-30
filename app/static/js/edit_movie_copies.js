$(document).ready(function() {
    bind_buttons();
});

$('#add-copy-form').submit(function(event) {
    event.preventDefault();
    var form = $('#add-copy-form');
    $.post(form.attr('action'), form.serialize(), function(data) {
        if (data.success) {
            alert('Copy successfully added!');
            $('#add-copy-form')[0].reset();

            update_table(data.copies);
            bind_buttons();
        }
        else {
            alert("Failed to add the copy. Reason: ", data.reason);
        }
    });
});

$('#edit-copy-form').submit(function(event) {
    event.preventDefault();
    var form = $('#edit-copy-form');
    $.post(form.attr('action'), form.serialize(), function(data) {
        if (data.success) {
            $.get('/do-get-movie-copies/' + $('#new-btn').attr('name'), function(data) {
                if (data.success) {
                    update_table(data.copies);
                    bind_buttons();
                    $('#edit-copy-modal').modal('hide');

                    $('[name=' + $('#copy-id-input').val() + ']').parent().parent().addClass('highlight');
                    setTimeout(function() {
                        $('[name=' + $('#copy-id-input').val() + ']').parent().parent().removeClass('highlight');
                    }, 2000);
                }
                else {
                    alert("Failed to refresh copies table. Reason: " + data.reason);
                }
            });
        }
        else {
            alert("Failed to edit movie copy. Reason: " + data.reason);
        }
    });
});

function bind_buttons() {
    console.log('prick');
    $('.edit-btn').click(function(event) {
        //set copy id input to id
        console.log("fuck you");
        $('#copy-id-input').val($(this).attr('name'));
        $('#copy-price-input').val($(this).parent().parent().children('td')[2].textContent.slice(1))
        $('#copy-description-input').text($(this).parent().parent().children('td')[1].textContent);
        $('#edit-copy-modal').modal('show');
    });

    $('.delete-btn').click(function(event) {
        if (confirm('Are you sure you wish to delete this movie copy? This action is irreversible.')) {
            $.post('/do-delete-movie-copy', { id: $(this).attr('name') }, function(data) {
                if (data.success) {
                    console.log($('[name=' + data.id + ']').parent().parent());
                    $('[name=' + data.id + ']').parent().parent().fadeOut('slow', function() {$(this).remove(); });
                }
                else {
                    alert('Failed to delete the movie copy. Reason: ' + data.reason);
                }
            });
        }
    });
}

function update_table(copies) {
    var newHtml = "";
    for (var i = 0; i < copies.length; i++) {
        newHtml += '<tr class="copy">\
                        <td>' + i + '</td>\
                        <td>' + copies[i].copy_information + '</td>\
                        <td>$' +  copies[i].price + '</td>\
                        <td>' + copies[i].sold + '</td>\
                        <td>\
                            <button name="' + copies[i].id + '" class="btn btn-primary btn-sm copy-btn edit-btn">\
                                <i class="far fa-edit"></i>\
                            </button>\
                            <button name="' + copies[i].id + '" class="btn btn-danger btn-sm copy-btn delete-btn">\
                                <i class="far fa-trash-alt"></i>\
                            </button>\
                        </td>\
                    </tr>'
    }

    $('#movie-copies-table-body').html(newHtml);
}
