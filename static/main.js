// main.js

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

// Function to load search options
function loadSearchOptions() {
  fetch("templates/search_options.html")
    .then((response) => response.text())
    .then((html) => {
      $("#search_page_options").html(html);
    });
}

// Document ready function
$(document).ready(function() {
  // Load search options
  loadSearchOptions();

  // Load previous conversations on page load
  loadPreviousConversations();

  // Form submit event handler
  $("form").submit(function(event) {
    event.preventDefault();
        const formData = new FormData(this);
        const query = formData.get("query");
        const max_tokens = parseInt(formData.get("max_tokens"));
        const user_personality = formData.get("user_personality");
        const task = formData.get("task");
        const format = formData.get("format");
        const additional_context = task + " " + format;

        // Search for relevant snippets
        $.ajax({
            url: "/search",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function(response) {
                const snippets = response.snippets;
                let resultsHTML = '<ol>';
                snippets.forEach(snippet => {
                    resultsHTML += `<li>${snippet.response}</li>`;
                });
                resultsHTML += '</ol>';
                $("#results").html(resultsHTML);
            }
        });

        // Get the chatbot's response
        $.ajax({
            url: "http://localhost:5001/api/chatbot",
            type: "POST",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                user_input: query,
                max_tokens: max_tokens,
                user_personality: user_personality,
                additional_context: additional_context
            }),
            success: function(response) {
                $("#chatbot_response").html(response.response);
            }
        });
    });
});
