// main.js

$(document).ready(function () {
    // Load search options
    loadSearchOptions();

    // Load previous conversations on page load
    loadPreviousConversations();
});

// Function to load previous conversations
function loadPreviousConversations() {
    $.ajax({
        url: "/load_previous_conversations",
        type: "GET",
        dataType: "json",
        success: function(response) {
            const previousConversations = response.previous_conversations;
            $("#previous_conversations").html(previousConversations);
        }
    });
}

// Function to save to google sheet
function saveEditedAnswerToSheet(editedAnswer) {
    $.ajax({
        url: "/save_edited_answer",
        type: "POST",
        data: {
            edited_answer: editedAnswer
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

    console.log(`About to send AJAX request with query: ${query}, max_tokens: ${max_tokens}, num_results: ${num_results}`);

    // Call the searchAndDisplaySnippets function
    searchAndDisplaySnippets(query, num_results);

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


