$(document).ready(function() {
    $('.js-example-basic-multiple').select2({ theme: "bootstrap", width: "resolve" });
    $('#body-content').css('opacity', 1);
    window.catalogue = new catalogue();
    window.catalogue.update_movies_grid();
});

function catalogue() {
    this.maxLoadedMovies = 40; //the maximum number of movies to load when querying the db
    this.currentPage = 0; //the current "page" in the db (page is a group of n records, where n = maxLoadedMovies)
    this.moviesCache = []; //will possibly implement caching later

    this.update_movies_grid = function() {
        var form = $('#filters-form');
        var data = form.serialize() + "&page=" + this.currentPage + "&amount=" + this.maxLoadedMovies;
        $.post(form.attr('action'), data, this.update_movies_grid_callback);
        $('#movies-container').css('opacity', 0);
    }

    this.update_movies_grid_callback = function(data) {
        console.log(data);
        if (data.success) {
            $('#movies-container').html(data.gridHtml);

            $('[data-toggle="tooltip"]').tooltip()

            $('.edit-movie-btn').click(function(event) {
                event.preventDefault();
                window.location.href = "/edit-movie/" + $(this).parent().parent().attr('id');
            });

            $('.edit-movie-copies-btn').click(function(event) {
                event.preventDefault();
                window.location.href = "/edit-movie-copies/" + $(this).parent().parent().attr('id');
            });
        }
        else {
            alert("An unexpected error has occurred while trying to refresh the movie catalogue: " + data.message)
        }

        setTimeout(function() { $('#movies-container').css('opacity', 1); }, 250);
    }
}
