// File: static/save_edits.js

function saveEditedAnswerToSheet(editedAnswer) {
    const user_id = $("#user_id").val() || "OWNER";

    // Construct the base URL dynamically
    const protocol = window.location.protocol;
    const host = window.location.hostname;

    // Choose the port based on the hostname
    let port;
    if (host === 'localhost' || host === '127.0.0.1') {
        port = 5002;  // The port your Flask app runs on in your personal computer
    } else {
        port = 5002;  // The port your Flask app runs on in your Digital Ocean instance
    }

    const flask_app_url = `http://${host}:${port}`;

    // Log the constructed URL
    console.log("Constructed URL: ", flask_app_url);

    $.ajax({
        url: flask_app_url + "/save_edited_answer",
        type: "POST",
        data: {
            'edited_answer': editedAnswer,
            'user_id': user_id  // Include user_id in the request
        },
        success: function(response) {
            console.log('Success:', response);
            alert(response.message);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('Error:', textStatus, errorThrown);
            alert("An error occurred while saving the edited answer.");
        }
    });
}

