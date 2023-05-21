// Function for handling form submission
function handleFormSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const query = formData.get("query");
    const max_tokens = parseInt(formData.get("max_tokens"));
    const num_results = parseInt(formData.get("num_results")); // Add this line
    const user_personality = formData.get("user_personality");
    const task = formData.get("task");
    const format = formData.get("format");
    const additional_context = task + " " + format;
    const user_id = formData.get("user_id");  // Add this line
    console.log(`User ID in chatbot.js: ${user_id}`); // Add this line

    // Get the selected model from the dropdown
    const model = $("#model").val();

    // Search for relevant snippets
    $.ajax({
        url: `http://${window.location.hostname}:5001/api/chatbot`, // dont modify the port as the chatbot is at 5001
        type: "POST",
        data: {
            'query': query,
            'num_results': num_results  // Update this line
        },
        dataType: "json",
        success: function (response) {
            const snippets = response.snippets;
            displaySnippets(snippets); // Call the function to display snippets on the search page.
        }
    });

    // Get the chatbot's response
    $.ajax({
        url: `/api/chatbot`,
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            user_input: query,
            user_id: user_id,  // Use the user_id from the form
            max_tokens: max_tokens,
            user_personality: user_personality,
            additional_context: additional_context,
            model: model
        }),
        success: function (response) {
            $("#chatbot_response").html(response.response);
            $("#edited_answer").val(response.response);
        }
    });
}

// Function to save edited answer
function saveEditedAnswer() {
    const editedAnswer = $("#edited_answer").val();
    $("#final_answer").html(editedAnswer);
    saveEditedAnswerToSheet(editedAnswer);
}

// Document ready function
$(document).ready(function () {
    // Form submit event handler
    $("form").submit(handleFormSubmit);

    // Save edited answer event handler
    $("#save_edited_answer").click(saveEditedAnswer);
});

// Function to display snippets
function displaySnippets(snippets) {
    const snippetsList = $("#snippets");
    snippetsList.empty(); // Clear the current list of snippets

    snippets.forEach(snippet => {
        const listItem = $("<li>").text(snippet.response);
        snippetsList.append(listItem);
    });
}
