import * as functions from "firebase-functions";

// Change the function name to something more descriptive
export const chatbotWebhook = functions.https.onRequest((request, response) => {
  // Get the user's query from the request's query parameter named "query"
  const query = request.query.query as string;

  // Create a response with the user's query
  const chatbotResponse = {
    fulfillmentText: `You said "${query}".`
  };

  // Send the response to the user
  response.json(chatbotResponse);
});

