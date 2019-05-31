$(document).ready(function() {
    $('.js-example-placeholder-multiple').select2({ theme: "bootstrap", width: "resolve", placeholder: "Genres" });
    $('#body-content').css('opacity', 1);
    window.catalogue = new catalogue();
    update_movies_grid();

    $('#filters-form').submit(function(event) {
        event.preventDefault();
        // window.catalogue.currentPage = 0;
        // update_movies_grid();
        window.catalogue.set_page(0);
    });

    $('#first-page-btn').click(function(event) {
        window.catalogue.set_page(0);
    });
    $('#last-page-btn').click(function(event) {
        window.catalogue.set_page(window.catalogue.numPages == 0 ? 0 : window.catalogue.numPages - 1);
    });
    $('#prev-page-btn').click(() => window.catalogue.prev_page());
    $('#next-page-btn').click(() => window.catalogue.next_page());
});

//Only one catalogue object should ever be created, and it should be attached to the window
function catalogue() {
    this.maxLoadedMovies = 40; //the maximum number of movies to load when querying the db
    this.numPages = 1;
    this.currentPage = 0; //the current 0-indexed "page" in the db (page is a group of n records, where n = maxLoadedMovies)
    this.moviesCache = []; //will possibly implement caching later

    this.prev_page = function() {
        if (this.currentPage > 0) {
            update_movies_grid(--this.currentPage);
        }
    }

    this.next_page = function() {
        if (this.currentPage < this.numPages - 1) {
            update_movies_grid(++this.currentPage);
        }
        else {
            console.log(this.currentPage, this.numPages)
        }
    }

    this.set_page = function(page) {
        this.currentPage = page;
        update_movies_grid();
    }
}

function update_movies_grid() {
    var form = $('#filters-form');
    var data = form.serialize() + "&page=" + window.catalogue.currentPage + "&amount=" + window.catalogue.maxLoadedMovies;
    $('#movies-container').css('opacity', 0);
    $.post(form.attr('action'), data, update_movies_grid_callback);
}

function update_movies_grid_callback(data) {
    if (data.success) {
        window.catalogue.numPages = data.numPages;

        $('#prev-page-btn').attr('disabled', window.catalogue.currentPage <= 0);
        $('#next-page-btn').attr('disabled', window.catalogue.currentPage >= window.catalogue.numPages - 1);

        $('#page-num-btn').text(window.catalogue.currentPage + 1);

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
                $.post('/do-delete-movie', { id: $(this).parent().parent().attr('id') }, update_movies_grid);
            }
        });

        $('.add-to-order-btn').click(function(event) {
            event.preventDefault();
            window.location.href = "/add-to-order" + $(this).parent().parent().attr('id');
        });
    }
    else {
        alert('An unexpected error has occurred while trying to refresh the movie catalogue: ' + data.message)
    }

    setTimeout(function() { $('#movies-container').css('opacity', 1); }, 250);
}
