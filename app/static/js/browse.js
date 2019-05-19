$(document).ready(function() {
    $('.js-example-basic-multiple').select2({ theme: "bootstrap", width: "resolve" });
    $('#filters-container').css('opacity', 1);
    $('#movies-container').css('opacity', 1);
});

function catalogue() {
    this.maxLoadedMovies = 40; //the maximum number of movies to load when querying the db
    this.currentDbIndex = 0; //the current position in the result of the current movie query
    this.loadedMovies = [];
    this.moviesCache = []; //will possibly implement caching later

    this.get_movies = function(startIndex, length, filter) {
        var form = $('#filters-form');
        var data = form.serialize() + "&index=" + startIndex + "&amount=" + length;
        $.post(form.attr('action'), data, this.get_movies_callback);
    }

    this.get_movies_callback = function(data) {
        if (data.success) {
            this.loadedMovies = data.movies;
        }
        else {
            alert("An unexpected error has occurred while trying to refresh the movie catalogue: " + data.reason);
        }
    }
}
