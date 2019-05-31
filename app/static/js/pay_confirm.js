$(document).ready(function(){
  bind_buttons();
});
$('#update-payment-form').submit(function(event) {
  event.preventDefault();
  var form = $('#update-payment-form');
  $.post(form.attr('action'), form.serialize(), function(data) {
                  update_table(data.copies, data.isStaff);
                  bind_buttons();
                  $('#edit-copy-modal').modal('hide');
                  //console.log($('#copy-id-input').val());
                  $('[name=' + $('#copy-id-input').val() + ']').parent().parent().addClass('highlight');
                  setTimeout(function() {
                      $('[name=' + $('#copy-id-input').val() + ']').parent().parent().removeClass('highlight');
                  }, 2000);
              }
              );
});




