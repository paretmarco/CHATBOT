$(document).ready(function () {
    $("form").submit(function (event) {
        event.preventDefault();

        const query = $("#query").val();
        const num_results = $("#num_results").val();
        const max_tokens = $("#max_tokens").val();
        const chatbot_max_tokens = $("#chatbot_max_tokens").val();

        // Add your logic here to handle the form submission
        // This may include making an API call to your server and displaying the results

        // Example:
        $.ajax({
            url: "/api/search",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                query: query,
                num_results: num_results,
            }),
            success: function (data) {
                // Clear the snippets list
                $("#snippets").empty();

                // Add the retrieved snippets to the list
                data.response.forEach(function (snippet) {
                    $("#snippets").append("<li>" + snippet.response + "</li>");
                });

                // Display the chatbot response
                $("#chatbot_response").html(data.response[0].response.slice(0, chatbot_max_tokens));
            },
        });
    });
});
