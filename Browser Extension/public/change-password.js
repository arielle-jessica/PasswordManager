document.getElementById('btnSubmitChange').addEventListener('click', changeMasterPassword);
document.getElementById('btnBack').addEventListener('click', () => {
  window.location.href = 'popup.html'; 
});

function changeMasterPassword() {
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;

  if (!currentPassword || !newPassword) {
    displayMessage('Please fill in both fields.', 'error');
    return;
  }

  fetch('http://127.0.0.1:5000/change-master-password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      currentPassword: currentPassword,
      newPassword: newPassword
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      displayMessage('Master password changed successfully!', 'success');
      document.getElementById('currentPassword').value = '';
      document.getElementById('newPassword').value = '';
    } else {
      displayMessage(`Error: ${data.message}`, 'error');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    displayMessage('An error occurred while changing the master password.', 'error');
  });
}

function displayMessage(message, type) {
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = message;
  resultDiv.className = type; // Apply a class for styling based on message type

  // Optional: Add styles for success and error messages
  const styles = {
    success: 'color: green; font-weight: bold;',
    error: 'color: red; font-weight: bold;'
  };
  resultDiv.style.cssText = styles[type] || '';
}
