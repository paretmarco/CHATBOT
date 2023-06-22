// Function for handling form submission with streaming

async function handleFormSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const query = formData.get("query");
  const max_tokens = parseInt(formData.get("max_tokens"));
  const num_results = parseInt(formData.get("num_results"));
  const user_personality = formData.get("user_personality");
  const task = formData.get("task");
  const format = formData.get("format");
  const additional_context = task + " " + format;
  const user_id = formData.get("user_id");

  const model = $("#model").val();

  $.ajax({
    url: "/api/search",
    type: "POST",
    data: {
      query: query,
      num_results: num_results,
    },
    dataType: "json",
    success: function (response) {
      const snippets = response.snippets;
      displaySnippets(snippets);
    },
  });

  const controller = new AbortController();

  await fetch(`http://${window.location.hostname}:5001/api/chatbot_streaming`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    signal: controller.signal,
    body: JSON.stringify({
      user_input: query,
      user_id: user_id,
      max_tokens: max_tokens,
      user_personality: user_personality,
      additional_context: additional_context,
      model: model,
    }),
  }).then(async (response) => {
    if (response.status === 200) {
      const reader = response.body.getReader();
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const text = new TextDecoder().decode(value);
          const message = JSON.parse(text);
          $("#chatbot_response").html(message);
          $("#edited_answer").val(message);
        }
      } catch (err) {
        console.error("Error in streaming:", err);
      } finally {
        reader.releaseLock();
      }
    } else {
      console.error("Error in chatbot streaming API:", response.status);
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
    // $("form").submit(handleFormSubmit); // Use this for non-streaming
    $("form").submit(handleFormSubmitStreaming); // Use this for streaming

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
