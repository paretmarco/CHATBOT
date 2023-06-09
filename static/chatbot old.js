// Function for handling form submission
function handleFormSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const query = formData.get("query");
    const max_tokens = parseInt(formData.get("max_tokens"));
    const num_results = parseInt(formData.get("num_results"));
    const user_id = $("#user_id").val() || "OWNER"; 
    const user_personality = formData.get("user_personality");
    const task = formData.get("task");
    const format = formData.get("format");
    const additional_context = task + " " + format;
    const temperature = parseFloat(formData.get("temperature"));
    const frequency_penalty = parseFloat(formData.get("frequency_penalty"));
    console.log('Frequency penalty:', frequency_penalty);
    console.log('Query chatbot:', query);
    console.log('Num results chatbot:', num_results);
    console.log('User id chtabot:', user_id);

    // Get the selected model from the dropdown
    const model = $("#model").val();


    // Fetch a video to display while waiting for the chatbot's response
    fetch('http://localhost:5003/api/video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: query  // send the query as request body
        })
    })

    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // extract the video URL from the response
        const video_url = data.video_url;

        // display the video in the iframe
        document.getElementById('youtube-video').src = video_url;
    })
    .catch(error => {
        console.error('Fetch Error:', error);
    });



    // Call the searchAndDisplaySnippets function
    searchAndDisplaySnippets(query, num_results);

    // Search for relevant snippets
    $("#progress-bar").removeClass("hidden");
    $.ajax({
        url: "/api/search",
        type: "POST",
        data: {
            'query': query,
            'num_results': num_results 
        },
        dataType: "json",
        success: function (response) {
            const snippets = response.snippets;
            displaySnippets(snippets); 
        }
    });

    // Get the chatbot's response
    $.ajax({
        url: `http://${window.location.hostname}:5001/api/chatbot`,
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            user_input: query,
            user_id: user_id, 
            max_tokens: max_tokens,
            user_personality: user_personality,
            additional_context: additional_context,
            model: model,
            temperature: temperature,
            frequency_penalty: frequency_penalty
        }),
        beforeSend: function() {
            showProgressBar();
        },
        success: function (response) {
            $("#chatbot_response").html(response.response);
            $("#edited_answer").val(response.response);
            hideProgressBar();
        },
        error: function() {
            hideProgressBar();
        }
    });
}

// Function to save edited answer
function saveEditedAnswer() {
    const editedAnswer = $("#edited_answer").val();
    $("#final_answer").html(editedAnswer);
    saveEditedAnswerToSheet(editedAnswer);
}


// Function to show the progress bar
function showProgressBar() {
    $("#progress").width('100%');
    showVideo(); // Show the video
}

// Function to hide the progress bar
function hideProgressBar() {
    $("#progress").width(0);
    hideVideo(); // Hide the video
}

// Document ready function
$(document).ready(function () {
    // Form submit event handler
    $("form").submit(handleFormSubmit);

    // Save edited answer event handler
    $("#save_edited_answer").click(saveEditedAnswer);
});