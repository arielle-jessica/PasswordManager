document.getElementById('btnRetrieve').addEventListener('click', retrievePassword);
document.getElementById('btnBack').addEventListener('click', () => {
  window.location.href = 'popup.html';  
});

function retrievePassword() {
  const website = document.getElementById('website').value;

  if (!website) {
    alert('Please enter the website name.');
    return;
  }

  fetch('http://127.0.0.1:5000/retrieve-password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ website })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    if (data.success) {
      // Display the decrypted password
      document.getElementById('result').innerText = `Password for ${website}: ${data.password}`;
    } else {
      document.getElementById('result').innerText = `Error: ${data.message}`;
    }
  })
  .catch(error => {
    console.error('Fetch Error:', error);
    document.getElementById('result').innerText = 'An error occurred while retrieving the password. Try Again!';
  });
}
