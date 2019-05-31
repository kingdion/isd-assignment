$(document).ready(function()
{
$.post('/do-add-to-order'. {'copiesIDs[]': JSON.parse(localStorage.getItem('orders'))}, function(data){
  if (data.success) {
    update_order_tables(data.orders);
  }
  else {
    alert('Failed to update orders. Reason:' + data.reason);
  }


}));
  });


function update_order_tables(orders){
    var newHtml = ""
    for (var i = 0; i < orders.length; i++) {
      newHtml += '<tr>\
                      <td>' + i + '</td>\
                      <td>' + orders[i].title + '</td>\
                      <td>$' +  copies[i].price + '</td>\
                      <td><button id="{{order.id}}" class="delete-movie-order btn btn-danger btn-sm">Remove Movie</button></td></tr>';\

    }
    $('#order-body').html(newHtml)
}




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
