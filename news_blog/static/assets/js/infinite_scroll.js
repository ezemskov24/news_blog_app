// infinite_scroll.js

var loading = false;
var page = 2;
var reachedEnd = false;

function loadMoreNews() {
    if (!loading && !reachedEnd) {
        loading = true;
        $.ajax({
            url: window.location.href,
            type: 'GET',
            data: {
                'page': page,
            },
            success: function(data) {
                if (data.news_html) {
                    $('#news-container').append(data.news_html);
                    loading = false;
                    if (data.has_next) {
                        page += 1;
                    } else {
                        reachedEnd = true;
                    }
                } else {
                    console.log('No data received.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
}

$(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
        loadMoreNews();
    }
});


