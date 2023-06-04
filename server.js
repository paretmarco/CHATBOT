const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

// Serve your snippets.html file
app.use(express.static('templates'));

// Define a route to retrieve snippets from the Python script
app.get('/api/snippets', async (req, res) => {
  try {
    console.log('Received request for snippets');
    const response = await axios.post('http://localhost:3000/api/search', {});
    const snippets = response.data.response;
    console.log('Retrieved snippets:', snippets);
    res.json(snippets);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

