$(document).ready(function () {
    $('#report-form').on('submit', function (event) {
        event.preventDefault();
        console.log("Report");  // sanity check
        send_report();
    });

    function send_report() {
        console.log("The report is being sent"); // sanity check
        $.ajax({
            url: "report/", // the endpoint
            type: "POST", // http method
            data: {the_report: $('#report_message').val()}, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#report-text').val(''); // remove the value from the input
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