$(document).ready(function(){
  bind_buttons();
});
$('#update-payment-form').submit(function(event) {
  event.preventDefault();
  var form = $('#update-payment-form');
  $.post(form.attr('action'), form.serialize(), function(data) {
    bind_buttons();
    $('#edit-copy-modal').modal('hide');}
  );
});

function bind_buttons() {
  $('.edit-btn').click(function(event) {
      $('#payment-id-input').val($(this).attr('name'));
      $('#update-payment-modal').modal('show');
  });

  $('.delete-btn').click(function(event) {
          $.post('/do-delete-payment', { id: $(this).attr('name') }, function(data) {
              if (data.success) {
                  $('[name=' + data.id + ']').parent().parent().fadeOut('slow', function() {$(this).remove(); });
              }
              else {
                  alert('Failed to delete the movie copy. Reason: ' + data.reason);
              }
          });
      }
  );
}



