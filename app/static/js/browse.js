$(document).ready(function() {
    $('.js-example-placeholder-multiple').select2({ theme: "bootstrap", width: "resolve", placeholder: "Genres" });
    $('#body-content').css('opacity', 1);
    window.catalogue = new catalogue();
    update_movies_grid();

    $('#filters-form').submit(function(event) {
        event.preventDefault();
        update_movies_grid();
    });
});

//Only one catalogue object should ever be created, and it should be attached to the window
function catalogue() {
    this.maxLoadedMovies = 40; //the maximum number of movies to load when querying the db
    this.currentPage = 0; //the current "page" in the db (page is a group of n records, where n = maxLoadedMovies)
    this.moviesCache = []; //will possibly implement caching later
}

function update_movies_grid() {
    var form = $('#filters-form');
    var data = form.serialize() + "&page=" + window.catalogue.currentPage + "&amount=" + window.catalogue.maxLoadedMovies;
    $.post(form.attr('action'), data, update_movies_grid_callback);
    $('#movies-container').css('opacity', 0);
}

function update_movies_grid_callback(data) {
    if (data.success) {
        $('#movies-container').html(data.gridHtml);

        $('[data-toggle="tooltip"]').tooltip({ trigger: 'hover' });

        $('.edit-movie-btn').click(function(event) {
            event.preventDefault();
            window.location.href = "/edit-movie/" + $(this).parent().parent().attr('id');
        });

        $('.edit-movie-copies-btn').click(function(event) {
            event.preventDefault();
            window.location.href = "/edit-movie-copies/" + $(this).parent().parent().attr('id');
        });

        $('.delete-movie-btn').click(function(event) {
            event.preventDefault();
            if (confirm('Are you sure you wish to delete this movie? This cannot be undone.')) {
                $.post('/delete-movie', { id: $(this).parent().parent().attr('id') }, update_movies_grid);
            }
        });
    }
    else {
        alert('An unexpected error has occurred while trying to refresh the movie catalogue: ' + data.message)
    }

    setTimeout(function() { $('#movies-container').css('opacity', 1); }, 250);
}
