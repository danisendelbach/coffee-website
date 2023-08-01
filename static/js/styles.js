function toggleState(cafeId) {
    // Send an HTTP request to your Flask server to update the boolean state
    // You can use Fetch API, Axios, or other libraries to make the request.
    // Here, we'll use Fetch API as an example:
  const checkbox = document.getElementById(cafeId);
  const label = document.getElementById('label_' + cafeId);
  const state = checkbox.checked ? 'unchecked' : 'checked';

    fetch(`/update_state/${cafeId}/${state}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    })
    .then(response => response.json())
    .then(data => {
      // The response from the server can be processed here if needed
      console.log('Updated state:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }