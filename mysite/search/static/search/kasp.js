$(document).ready(function () {
    console.log("kaspready!");
    $('#button_copy').click(function () {
        clickedRecipeID = this.dataset.identifikators;
        console.log(clickedRecipeID);
        request_parameters = {
            recid: clickedRecipeID
        };
        const endpoint = '/post-create/';


        let ajax_call = function (endpoint, request_parameters) {

            //console.log(request_parameters);

            $.getJSON(endpoint, request_parameters)
                .done(response => {


                    $("#div_content_replace").html();
                    artists_div.html(response['html_from_view']);

                });
        };
    })
});
