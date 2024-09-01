document.addEventListener('DOMContentLoaded', () => {
    const btnBack = document.getElementById('btnBack');
    const btnDeveloperInfo = document.getElementById('btnDeveloperInfo');
  
    if (btnBack) {
      btnBack.addEventListener('click', () => {
        window.location.href = 'popup.html';
      });
    } else {
      console.error('Button with ID "btnBack" not found.');
    }
  
    if (btnDeveloperInfo) {
      btnDeveloperInfo.addEventListener('click', showDeveloperInfo);
    } else {
      console.error('Button with ID "btnDeveloperInfo" not found.');
    }
  });
  
  function showDeveloperInfo() {
    alert('Developer: Arielle Jessica\nEmail: ibajessica243@gmail.com\nLinkedIn: linkedin.com/in/ariellejessicaiba');
  }
  
