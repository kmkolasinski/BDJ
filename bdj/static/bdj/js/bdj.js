$(document).ready(function () {

    $('#search').keyup(function () {
        $('.card').removeClass('d-none');
        let filter = slugify($(this).val().toLowerCase()); // get the value of the input, which we filter on
        let words = filter.split(" ");

        $('.card-deck div.card-text div.active').each(function( key, value ) {
            let text = slugify($(this).text().toLowerCase())
            words.forEach(function (word, index) {
              if ( !text.includes(word) ){
                    $(value).parents("div.card").addClass('d-none');
              }
            });
        });
    })

    $('#btnSort').click(function () {
        $('.card-deck .card').sort(function (a, b) {
            return $(a).find(".card-title").text() > $(b).find(".card-title").text() ? 1 : -1;
        }).appendTo(".card-deck");
    })

});

function loadFoodPlacePosts(url, cardElement, foodPlaceId) {
    $(cardElement).fadeTo("fast", 0.5)
    $.ajax({
        url: url,
        data: {
            foodPlaceId: foodPlaceId,
            csrfmiddlewaretoken: Cookies.get('csrftoken')
        },
        type: 'post',
        dataType: 'json',
        success: function (data) {
            $(cardElement).html(data.html)
            $(cardElement).fadeTo("fast", 1.0)
            $(".zoomable-image").zoom({ on:'click' , magnify: 0.75});
        }
    });
}


function slugify (str) {
    const map = {
        '-': ' ',
        'a': 'á|à|ã|â|ą|À|Á|Ã|Â|Ą',
        'e': 'é|è|ê|ę|É|È|Ê|Ę',
        'i': 'í|ì|î|Í|Ì|Î',
        'o': 'ó|ò|ô|õ|Ó|Ò|Ô|Õ',
        'u': 'ú|ù|û|ü|Ú|Ù|Û|Ü',
        'c': 'ç|ć|Ç',
        'n': 'ñ|Ñ|ń',
        'l': 'ł|Ł',
        's': 'ś|Ś',
        'z': 'ż|ź|Ż|Ź',
    };

    for (let pattern in map) {
        str = str.replace(new RegExp(map[pattern], 'g'), pattern);
    }
    return str;
}