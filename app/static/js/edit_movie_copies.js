$(document).ready(function() {
    bind_buttons();
});

$('#add-copy-form').submit(function(event) {
    event.preventDefault();
    var form = $('#add-copy-form')
    $.post(form.attr('action'), form.serialize(), function(data) {
        if (data.success) {
            alert('Copy successfully added!');
            $('#add-copy-form')[0].reset();

            var newHtml = "";
            for (var i = 0; i < data.copies.length; i++) {
                newHtml += '<tr class="copy">\
                                <td>' + i + '</td>\
                                <td>' + data.copies[i].copy_information + '</td>\
                                <td>$' +  data.copies[i].price + '</td>\
                                <td>' + data.copies[i].sold + '</td>\
                                <td>\
                                    <button id="edit-btn" name="' + data.copies[i].id + '" class="btn btn-primary btn-sm copy-btn">\
                                        <i class="far fa-edit"></i>\
                                    </button>\
                                    <button id="delete-btn" name="' + data.copies[i].id + '" class="btn btn-danger btn-sm copy-btn">\
                                        <i class="far fa-trash-alt"></i>\
                                    </button>\
                                </td>\
                            </tr>'
            }

            $('#movie-copies-table-body').html(newHtml);

            bind_buttons();
        }
        else {
            alert("Failed to add the copy. Reason: ", data.reason);
        }
    });
});

function bind_buttons() {
    $('.edit-btn').click(function(event) {
        console.log("kill me");
    });

    $('.delete-btn').click(function(event) {
        event.preventDefault();

        if (confirm('Are you sure you wish to delete this movie copy? This action is irreversible.')) {
            $.post('/delete-movie-copy', { id: $(this).attr('name') }, function(data) {
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
