// File: static/show_snippets.js
// Establish a WebSocket connection to the server
let socket = io.connect('http://127.0.0.1:5000');

// Function to display snippets
function displaySnippets(snippets) {
    console.log('displaySnippets called with:', snippets);
    
    const snippetsList = $("#snippets");
    console.log('snippetsList:', snippetsList);
    
    snippetsList.empty(); // Clear the current list of snippets
    console.log('snippetsList after empty():', snippetsList);
    
    snippets.forEach((snippet, index) => {
        console.log(`Processing snippet ${index}:`, snippet);
        const listItem = $("<li>").text(snippet.response);
        console.log(`Created list item for snippet ${index}:`, listItem);
        
        snippetsList.append(listItem);
        console.log(`snippetsList after appending snippet ${index}:`, snippetsList);
    });

    console.log('Display Snippets Function: Snippets have been displayed'); 
}

// Function to emit a search event to the server once connection is established
socket.on('connect', () => {
    socket.emit('search', {query: 'my query', num_results: 5});
});


// Function to handle 'snippets' event sent by the server
socket.on('snippets', (data) => {
    console.log('Received data from server:', data);
    displaySnippets(data.response);
});

function searchAndDisplaySnippets(query, num_results) {
    $.ajax({
        url: "/api/search",
        type: "POST",
        data: JSON.stringify({
            'query': query,
            'num_results': num_results
        }),
        contentType: 'application/json',
        dataType: "json",
        beforeSend: function() {
            console.log('AJAX Call: Request being prepared');
        },
        success: function (response) {
            console.log('AJAX Call: Successful response received');
            console.log('Full response from server: ', response);
            if (!response || !response.response) {
                console.error('Unexpected response format');
                return;
            }
            const snippets = response.response; // No need to parse JSON here as response is already JSON
            console.log('Snippets: ', snippets);
            displaySnippets(snippets);
        },
        error: function (error) {
            console.error('AJAX Call: Error occurred');
            console.error('Error: ', error);
        },
        complete: function() {
            console.log('AJAX Call: Request completed');
        }
    });
}

