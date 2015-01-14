
jQuery(document).ready(function($) {
    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });


    $('.mark').click(function() {
        var answer = $(this).closest('.answer');

        if (answer)
        {
            $.ajax({
              type: "POST",
              url: "/mark/",
              data: {
                  id: answer.data('id')
              }
            })
            .done(function( msg )
            {
                if(msg['status'] == "ok")
                {
                    var mark = answer.find('.mark');

                    if(mark.text() != "Right!")
                        mark.text("Right!");
                    else
                        mark.text("Mark as right");
                }
                else
                    alert(msg['status']);
            })
            .fail(function( msg ) {
                alert(msg);
            });
        }

        return false;
    });


    //set rating handlers
    $('.ratingArrow').click(function() {
        var entry = $(this).closest('.thumbnail');
        var type = "";

        if(entry.hasClass("question"))
            type = "q";
        else if(entry.hasClass("answer"))
            type = "a";

        var direction = "";

        if ($(this).hasClass('rating_up'))
            direction = "up";
        else if ($(this).hasClass('rating_down'))
            direction = "down";

        if (direction != "" && type != "" && entry != null)
        {
            $.ajax({
              type: "POST",
              url: "/rating/",
              data: {
                  type: type,
                  id: entry.data('id'),
                  direction: direction
              }
            })
              .done(function( msg ) {

                    if(msg['status'] == "ok")
                        entry.find('.rating_value').text(msg['rating']);
                    else
                        alert(msg['status']);
              })
              .fail(function( msg ) {
                    alert(msg);
              });
        }

        return false;
    });
});