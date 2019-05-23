$(document).ready(function() {
    $('.js-example-basic-multiple').select2({ theme: "bootstrap", width: "resolve" });
    $('#filters-container').css('opacity', 1);
    $('#movies-container').css('opacity', 1);
    window.catalogue = new catalogue();
    window.catalogue.update_loaded_movies();
});

function catalogue() {
    this.maxLoadedMovies = 40; //the maximum number of movies to load when querying the db
    this.currentPage = 0; //the current "page" in the db (page is a group of n records, where n = maxLoadedMovies)
    this.loadedMovies = [];
    this.moviesCache = []; //will possibly implement caching later

    this.update_loaded_movies = function() {
        var form = $('#filters-form');
        var data = form.serialize() + "&page=" + this.currentPage + "&amount=" + this.maxLoadedMovies;
        $.post(form.attr('action'), data, this.update_loaded_movies_callback);
    }

    this.update_loaded_movies_callback = function(data) {
        console.log(data);
        if (data.success) {
            this.loadedMovies = data.movies;

            moviesContainer = $('#movies-container');
            newMovies = ""
            for (var i = 0; i < this.loadedMovies.length; i++) {
                movie = this.loadedMovies[i]
                newMovies += '<div class="movie-cell"><img src="' + movie.thumbnailSrc + '" alt="' + movie.title + '"><div class="movie-description">' + movie.title + '<br>(' + movie.release_year + ')</div></div>'
            }

            moviesContainer.html(newMovies);
        }
        else {
            alert("An unexpected error has occurred while trying to refresh the movie catalogue: " + data.reason);
        }
    }
}
