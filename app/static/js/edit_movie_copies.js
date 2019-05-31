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
            update_table(data.copies, data.isStaff);
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
                    update_table(data.copies, data.isStaff);
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
    $('.edit-btn').click(function(event) {
        $('#copy-id-input').val($(this).attr('name'));
        $('#copy-price-input').val($(this).parent().parent().children('td')[2].textContent.slice(1))
        $('#copy-description-input').val($(this).parent().parent().children('td')[1].textContent);
        $('#edit-copy-modal').modal('show');
    });

    $('.delete-btn').click(function(event) {
        if (confirm('Are you sure you wish to delete this movie copy? This action is irreversible.')) {
            $.post('/do-delete-movie-copy', { id: $(this).attr('name') }, function(data) {
                if (data.success) {
                    $('[name=' + data.id + ']').parent().parent().fadeOut('slow', function() {$(this).remove(); });
                }
                else {
                    alert('Failed to delete the movie copy. Reason: ' + data.reason);
                }
            });
        }
    });

    $('.add-to-order-btn').click(function(event) {
        //@Amara, fill in code here
        //It should make a post request (using $.post()) to '/do-add-to-order'
          var orders = JSON.parse(localStorage.getItem('orders')) || [];
          if (orders.indexOf($(this).attr('name')) == -1) {
            orders.push($(this).attr('name'));
            localStorage.setItem('orders', JSON.stringify(orders))
        }
        else {
          alert('This movie has already been added to your order.');
        }

    });

    $('[data-toggle="tooltip"]').tooltip({ trigger: 'hover' });
}

function update_table(copies, staffUser) {
    var newHtml = "";
    for (var i = 0; i < copies.length; i++) {
        newHtml += '<tr class="copy">\
                        <td>' + i + '</td>\
                        <td>' + copies[i].copy_information + '</td>\
                        <td>$' +  copies[i].price + '</td>\
                        <td>' + copies[i].sold + '</td>\
                        <td>'

        if (!copies[i].sold) {
            if (staffUser) {
                newHtml += '<button name="' + copies[i].id + '" class="btn btn-primary btn-sm copy-btn edit-btn" data-toggle="tooltip" data-placement="top" title="Edit copy details">\
                                <i class="far fa-edit"></i>\
                            </button>\
                            <button name="' + copies[i].id + '" class="btn btn-danger btn-sm copy-btn delete-btn" data-toggle="tooltip" data-placement="top" title="Delete copy">\
                                <i class="far fa-trash-alt"></i>\
                            </button>'
            }
            else {
                newHtml += '<button name="' + copies[i].id + '" class="btn btn-success btn-sm copy-btn add-to-order-btn" data-toggle="tooltip" data-placement="top" title="Add copy to order">\
                                <i class="far fa-plus-square"></i>\
                            </button>'
            }
        }

        newHtml += '</td></tr>';
    }

    $('#movie-copies-table-body').html(newHtml);
}
