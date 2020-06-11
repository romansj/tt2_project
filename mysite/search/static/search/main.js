$(document).ready(function () {
    console.log("ready!");


    //setup
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    //end setup


    const user_input = $("#user-input");
    const search_icon = $('#search-icon');
    const artists_div = $('#replaceable-content');

    const endpoint = '/search/results/';
    const delay_by_in_ms = 700;
    let scheduled_function = false;

    let ajax_call = function (endpoint, request_parameters) {

        console.log(request_parameters);

        $.getJSON(endpoint, request_parameters)
            .done(response => {
                // fade out the artists_div, then:
                // artists_div.fadeTo('slow', 0).promise().then(() => {
                // replace the HTML contents

                $("#div_content_replace").html();
                artists_div.html(response['html_from_view']);
                // fade-in the div with new contents
                // artists_div.fadeTo('slow', 1);
                // stop animating search icon
                // search_icon.removeClass('blink');
                // });
            });
    };

    var selectedCategory;
    var enteredWord;
    var clickedCategoryID;
    user_input.on('keyup', function () {
        console.log("keyup");
        enteredWord = $(this).val();
        request_parameters = {
            q: enteredWord // value of user_input: the HTML element with ID user-input
        };


        if (clickedCategoryID) {
            request_parameters = {
                q: enteredWord, cat: clickedCategoryID
            };
        }


        if (scheduled_function) { // if scheduled_function is NOT false, cancel the execution of the function
            clearTimeout(scheduled_function)
        }

        // setTimeout returns the ID of the function to be executed
        scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
    });


    const categorySelectionDiv = $("#search_selected_categories");

    $('a.a_category').click(function () {
        if (selectedCategory) {
            selectedCategory.classList.remove("selected_category");

        }

        selectedCategory = this;
        categorySelectionDiv.html("<p>" + $(this).text() + "</p>");
        selectedCategory.classList.add("selected_category");


        clickedCategoryID = this.dataset.categoryId;
        console.log(this.dataset.categoryId);//sanity check

        request_parameters = {
            cat: clickedCategoryID
        };

        if (enteredWord) {
            request_parameters = {
                q: enteredWord, cat: clickedCategoryID
            };
        }

        const endpoint = '/search/results/';


        let ajax_call = function (endpoint, request_parameters) {

            console.log(request_parameters);

            $.getJSON(endpoint, request_parameters)
                .done(response => {


                    $("#div_content_replace").html();
                    artists_div.html(response['html_from_view']);

                });
        };


        ajax_call(endpoint, request_parameters);

    });


// using jQuery


    $('#post-form').on('submit', function (event) {
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        create_post();
    });


    function create_post() {
        console.log("create post is working!"); // sanity check
        $.ajax({
            url: "rate/", // the endpoint
            type: "POST", // http method
            data: {the_post: $('#ingredient-name').val(), the_stars: $('#post-stars').val()}, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                $("#talk").prepend(
                    "<li style='background: #006400'> <p>Author: " + json.author + "</p> <p>Stars: " + json.stars + "</p> <p>Comment: " + json.comment + "</p> </li>"
                );


                console.log("success"); // another sanity check
            },


            // handle a non-successful response
            error: function (data) {
                //xhr, errmsg, err


                alert(data.status + ". " + data.responseJSON.error); // the message

                // $('#results').html("<div class='alert-box alert radius'>Oops! We have encountered an error: " + errmsg +
                //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }


    $('#button_delete_comment').click(function (event) {
        console.log("clicked delete");
        event.preventDefault();

        var doDelete = true;
        if (confirm('Are you sure you want to delete your comment?')) {
            doDelete = true;
            console.log("sure")
        }

        $.ajax({
            url: "rating_delete/", // the endpoint
            method: "get", // http method

            data: {the_delete: doDelete}, // data sent with the post request


            success: function (json) {
                // $('#post-text').val(''); // remove the value from the input
                // console.log(json); // log the returned json to the console
                // $("#talk").prepend(
                //     "<li style='background: darkgreen'> <p>Author: " + json.author + "</p> <p>Stars: " + json.stars + "</p> <p>Comment: " + json.comment + "</p> </li>"
                // );

                // console.log("success"); // another sanity check

                //location.reload();
            },


            error: function (data) {
                alert(data.status + ". " + data.responseJSON.error);
            }
        });
        return false;
    });


});


