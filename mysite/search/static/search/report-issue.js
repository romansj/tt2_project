$(document).ready(function () {
    $('#report-issue-from').on('submit', function (event) {
        event.preventDefault();
        console.log("aaaaa");  // sanity check
        send_information();
    });

    function send_information() {
        console.log("The report is being sent"); // sanity check
        $.ajax({
            url: "", // the endpoint
            type: "POST", // http method
            data: {the_message: $('#reporting-message').val()}, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#reporting-message').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console


                console.log("success"); // another sanity check
            },


            // handle a non-successful response
            error: function (data) {
                //xhr, errmsg, err

                if (data) {
                    // alert(data.status + ". " + data.responseJSON.error); // the message
                }
                // $('#results').html("<div class='alert-box alert radius'>Oops! We have encountered an error: " + errmsg +
                //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

});