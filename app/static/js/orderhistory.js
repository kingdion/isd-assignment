$("#date-time-picker-button").click(function(event)
{
    // Get the datepicker value
    var dateToFilterBy = $("#date-time-picker").val();

    // For each log's timestamp, check if the date of the row
    // is equal to our filter date. Fade out the row if
    // it is not equal to the filter.
    $('.log > .timestamp > .inner-date').each(function(i, obj)
    {
        var rowParent = $(this).parent().parent();

        if ($(this).text().includes(dateToFilterBy))
        {
            rowParent.fadeIn();
        }
        else
        {
            rowParent.fadeOut();
        }
    });
});

$("#searchnumber").click(function(event)
{
  var idFilter = $("searchnumber").val();



  var rowParent = $(this).parent().parent();

  if ($(this).text().include(idFilter))
  {
    rowParent.fadeIn();
  }
  else {
    {
      rowParent.fadeOut();
    }
  });

});
