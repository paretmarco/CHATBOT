  $(document).ready(function () {
    $("#search-form").on("submit", function (event) {
      event.preventDefault();
      const query = $("#query").val();
      const num_results = $("#num_results").val() || "{{ default_num_results }}";
      $.ajax({
        url: "/api/search",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ query: query, num_results: num_results }),
        dataType: "json",
        success: function (response) {
          displaySnippets(response.response);
        },
        error: function (error) {
          console.error("Error:", error);
        },
      });
    });

function displaySnippets(snippets) {
  const snippetsList = $("#snippets-list");
  snippetsList.empty();
  snippets.forEach((snippet) => {
    const listItem = $("<li>").text(snippet.response);
    snippetsList.append(listItem);
  });
}

 });
