const currentUser = localStorage.getItem("currentUser");
function initializeLocalStorage() {
  if (!localStorage.getItem('appointments')) {
    localStorage.setItem('appointments', JSON.stringify([]));
  }

  if (!localStorage.getItem('tests')) {
    localStorage.setItem('tests', JSON.stringify([]));
  }
}
  if (!currentUser) {

    alert("Please log in first!");
    window.location.href = "/login_signup/Log-in.html";
  }



document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.check a').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault(); // stop browser navigation
      const page = e.currentTarget.dataset.page;
      loadPage(page);
    });
  });
});

function loadPage(page) {
  fetch(`${page}.html`)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.text();
    })
    .then(html => {
      document.querySelector('#app').innerHTML = html;
    })
    .catch(err => {
      console.error("Error loading page:", err);
      document.querySelector('#app').textContent = "Failed to load page.";
    });
}
const cards=document.querySelectorAll(".cards-app, .cards-test, .cards-meds");
cards.forEach(card=>{
card.addEventListener('mouseenter',function(){
card.style.transform='translateY(-10px)';
card.style.boxShadow='0 8px 25px rgba(0,0,0,0.2)';

});

card.addEventListener('mouseleave',function(){
  card.style.transform = 'translateY(0px)';
  card.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
});
});

document.getElementById("logout").addEventListener("click", () => {
    localStorage.removeItem("currentUser");
    window.location.href = "/login_signup/Log-in.html";
  });