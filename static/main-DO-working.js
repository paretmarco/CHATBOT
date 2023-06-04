File: static/main.js
// main.js

$(document).ready(function () {

    // Load previous conversations on page load
    loadPreviousConversations();
});

// Function to load previous conversations
function loadPreviousConversations() {
    const user_id = $("#user_id").val() || "OWNER";
    console.log('user_id:', user_id); // Add this line for debugging
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
