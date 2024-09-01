document.getElementById('btnGenerate').addEventListener('click', generatePassword);
document.getElementById('btnBack').addEventListener('click', () => {
  window.location.href = 'popup.html';
});

function generatePassword() {
  const length = parseInt(document.getElementById('length').value);
  const website = document.getElementById('website').value;
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const desiredChars = document.getElementById('desiredChars').value;

  if (!length || !website || !username || !email) {
    alert('Please fill out all required fields.');
    return;
  }

  fetch('http://127.0.0.1:5000/generate-password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ length, website, username, email, desiredChars })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      document.getElementById('result').innerText = `Generated password for ${website}: ${data.password}`;
    } else {
      document.getElementById('result').innerText = `Error: ${data.message}`;
    }
  })
  .catch(error => {
    console.error('Error:', error);
    document.getElementById('result').innerText = 'An error occurred while generating the password.';
  });
}
