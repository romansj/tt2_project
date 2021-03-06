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

        //console.log(request_parameters);

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


    const searchBarModal = $("#search_bar_modal");
    let ajax_call2 = function (endpoint, request_parameters) {
        refs.modalEdicion.open();
        searchBarModal.focus();
        searchBarModal.val(enteredWord);
        searchBarModal.on('keyup', function () {
            //console.log("keyup big search");
            enteredWord = $(this).val();
            request_parameters = {
                q: enteredWord
            };
            if (scheduled_function) clearTimeout(scheduled_function);
            scheduled_function = setTimeout(ajax_call2, delay_by_in_ms, endpoint, request_parameters)
        });

        var pathname = window.location.pathname;
        //console.log("path " + pathname);
        if (pathname)

        //ja mes jau esam search lapa, tad html tur jau ir (kurā mes atrodam elementu un aizvietojam ar renderotiem rezultatiem no views.py)
        //savukart ja mes vel neesam search lapa, tad html vel nav, mes ieladejam content blokos tieši

        //console.log(request_parameters);

        $.getJSON(endpoint, request_parameters)
            .done(response => {
                $("#div_content_replace").html(response['html_from_view']);

            });
    };


    var selectedCategory;
    var enteredWord;
    var clickedCategoryID;
    user_input.on('keyup', function () {
        //console.log("keyup");
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


    const searchBar = $('#search_bar');


    searchBar.on('keyup', function () {
        enteredWord = $(this).val();
        request_parameters = {
            q: enteredWord
        };


        if (scheduled_function) clearTimeout(scheduled_function);
        scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)


    });


    function removeCategory() {

    }


    const categorySelectionDiv = $("#search_selected_categories");

    function doSearch(elem,) {
        clickedCategoryID = elem.dataset.categoryId;
        //console.log(elem.dataset.categoryId);//sanity check

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
            //console.log(request_parameters);

            $.getJSON(endpoint, request_parameters)
                .done(response => {
                    $("#div_content_replace").html();
                    artists_div.html(response['html_from_view']);


                });
        };
        ajax_call(endpoint, request_parameters);
    }

    $('a.a_category').click(function () {
        document.getElementById("myDropdown").classList.toggle("show");

        if (selectedCategory) {
            selectedCategory.classList.remove("selected_category");
        }

        selectedCategory = this;
        categorySelectionDiv.html("<span class='tag is-primary is-medium'>" + $(this).text() + "<button id='remove_category_bttn' class='delete is-small'></button></span><br><br>");

        selectedCategory.classList.add("selected_category");

        $('#remove_category_bttn').click(function () {
            //console.log('click');
            if (selectedCategory) {
                //console.log('in remove');
                selectedCategory.classList.remove("selected_category");
                categorySelectionDiv.html('');
                clickedCategoryID = '';

                doSearch(this);
            }
        });


        doSearch(this);
    });


// using jQuery
    $("#modal_bg").click(function () {
        refs.modalEdicion.close();
    });
    $("#close_button_modal").click(function () {
        refs.modalEdicion.close();
    });
    var refs = {
        modalEdicion: {
            open: function () {
                document.getElementById('my_modal').classList.add('is-active');
            },
            close: function () {
                document.getElementById('my_modal').classList.remove('is-active');
                searchBar.focus();
            }
        }
    };


    $('#post-form').on('submit', function (event) {
        event.preventDefault();
        //console.log("form submitted!");  // sanity check
        create_post();
    });


    function create_post() {
        //console.log("create post is working!"); // sanity check
        $.ajax({
            url: "rate/", // the endpoint
            type: "POST", // http method
            data: {the_post: $('#ingredient-name').val(), the_stars: $('#post-stars').val()}, // data sent with the post request

            // handle a successful response
            success: function (html) {
                $('#post-text').val(''); // remove the value from the input
                //console.log(html); // log the returned json to the console
                $("#results").prepend(html);
                $("#no_ratings_div").html('');


                //console.log("success"); // another sanity check
            },


            // handle a non-successful response
            error: function (data) {
                //xhr, errmsg, err

                if (data) {
                    alert(data.status + ". " + data.responseJSON.error); // the message
                }


                // $('#results').html("<div class='alert-box alert radius'>Oops! We have encountered an error: " + errmsg +
                //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }


    $('#button_delete_comment').click(function (event) {
        //console.log("clicked delete");
        event.preventDefault();

        var doDelete = true;
        if (confirm('Are you sure you want to delete your comment?')) {
            doDelete = true;
            //console.log("sure")
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


