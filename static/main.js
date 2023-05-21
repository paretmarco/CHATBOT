// main.js

$(document).ready(function () {
    // Load search options
    loadSearchOptions();

    // Load previous conversations on page load
    loadPreviousConversations();
});

// Function to load previous conversations
function loadPreviousConversations() {
    const user_id = $("#user_id").val() || "OWNER";
    $.ajax({
        url: "/load_previous_conversations",
        type: "GET",
        data: {
            'user_id': user_id
        },
        dataType: "json",
        success: function(response) {
            const previousConversations = response.previous_conversations;
            $("#previous_conversations").html(previousConversations);
        }
    });
}

function saveEditedAnswerToSheet(editedAnswer) {
    const user_id = $("#user_id").val() || "OWNER";
    $.ajax({
        url: "/save_edited_answer",
        type: "POST",
        data: {
            'edited_answer': editedAnswer,
            'user_id': user_id  // Include user_id in the request
        },
        success: function(response) {
            alert(response.message);
        },
        error: function() {
            alert("An error occurred while saving the edited answer.");
        }
    });
}

// Function to load search options
function loadSearchOptions() {
    fetch("templates/search_options.html")
        .then((response) => response.text())
        .then((html) => {
            $("#search_page_options").html(html);
        });
}

function handleFormSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const query = formData.get("query");
    const max_tokens = parseInt(formData.get("max_tokens"));
    const num_results = parseInt(formData.get("num_results"));

    // Call the searchAndDisplaySnippets function
    searchAndDisplaySnippets(query, num_results);
}

function searchAndDisplaySnippets(query, num_results) {
    $.ajax({
        url: "/api/search",
        type: "POST",
        data: {
            'query': query,
            'num_results': num_results
        },
        dataType: "json",
        success: function (response) {
            const snippets = response.response;
            displaySnippets(snippets);
        }
    });
}
