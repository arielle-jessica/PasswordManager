document.getElementById('btnAuth').addEventListener('click', authenticate);

function authenticate() {
  const username = document.getElementById('username').value;
  const passcode = document.getElementById('passcode').value;

  fetch('/authenticate-duo', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, passcode })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Hide the authentication section and show the main section
      document.getElementById('authSection').style.display = 'none';
      document.getElementById('mainSection').style.display = 'block';
      
      // Set authentication state in localStorage
      localStorage.setItem('authenticated', 'true');
    } else {
      // Optionally display an error message
      document.getElementById('authSection').innerHTML += `<p class="error-message">${data.message}</p>`;
    }
  })
  .catch(error => console.error('Error:', error));
}

function checkAuthentication() {
  if (localStorage.getItem('authenticated') === 'true') {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('mainSection').style.display = 'block';
  } else {
    document.getElementById('authSection').style.display = 'block';
    document.getElementById('mainSection').style.display = 'none';
  }
}

// Run the checkAuthentication function when the page loads
document.addEventListener('DOMContentLoaded', checkAuthentication);

document.getElementById('btnLogout').addEventListener('click', () => {
  // Clear authentication state from localStorage on logout
  localStorage.removeItem('authenticated');
  document.getElementById('authSection').style.display = 'block';
  document.getElementById('mainSection').style.display = 'none';
});


// Run the checkAuthentication function when the page loads
document.addEventListener('DOMContentLoaded', checkAuthentication);


document.addEventListener('DOMContentLoaded', checkAuthentication);


document.getElementById('btnChangePassword').addEventListener('click', () => {
  window.location.href = 'change-password.html';
});
document.getElementById('btnRetrievePassword').addEventListener('click', () => {
  window.location.href = 'retrieve-password.html';
});
document.getElementById('btnGeneratePassword').addEventListener('click',() => {
  window.location.href = 'generate-password.html';
});
document.getElementById('btnSearch').addEventListener('click', search);

document.getElementById('btnDeletePassword').addEventListener('click', deletePassword);

document.getElementById('btnDeveloperInfo').addEventListener('click', () => {
  window.location.href = 'developer-info.html';
});

document.getElementById('btnLogout').addEventListener('click', logout);

function changePassword() {
  alert("Change Password button clicked");
}
function retrievePassword() {
  alert("Change Password button clicked");
}

function developerInfo() {
  alert("Change Password button clicked");
}

function generatePassword() {
  alert("Generate Password button clicked");
}


function search() {
  const criteria = prompt("Enter search criteria (website, username, or email):").toLowerCase();
  const term = prompt("Enter search term:");

  fetch('/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ criteria, term })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      let resultString = "Search Results:\n";
      data.results.forEach(result => {
        resultString += `Website: ${result.website}, Username: ${result.username}\n`;
      });
      alert(resultString);
    } else {
      alert("No matching records found.");
    }
  })
  .catch(error => console.error('Error:', error));
}

function deletePassword() {
  const confirmDeletion = confirm("Are you sure you want to delete all passwords? This action cannot be undone.");
  if (confirmDeletion) {
    fetch('/delete-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
    })
    .catch(error => console.error('Error:', error));
  } else {
    alert("Password deletion cancelled.");
  }
}

function showDeveloperInfo() {
  alert("Developer: Arielle Jessica\nEmail: ibajessica243@gmail.com\nLinkedIn: linkedin.com/ariellejessicaiba");
}

function logout() {
  localStorage.removeItem('authenticated'); 
  document.getElementById('authSection').style.display = 'block';
  document.getElementById('mainSection').style.display = 'none';
}