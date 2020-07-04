const navbar = document.querySelector("#nav");
const navBtn = document.querySelector("#nav-btn");
const closeBtn = document.querySelector("#close-btn");
const sidebar = document.querySelector("#sidebar");
const date = document.querySelector("#date");
// add fixed class to navbar
window.addEventListener("scroll", function() {
  if (window.pageYOffset > 80) {
    navbar.classList.add("navbar-fixed");
  } else {
    navbar.classList.remove("navbar-fixed");
  }
});
// show sidebar
navBtn.addEventListener("click", function() {
  sidebar.classList.add("show-sidebar");
});
closeBtn.addEventListener("click", function() {
  sidebar.classList.remove("show-sidebar");
});
// set year
date.innerHTML = new Date().getFullYear();

// add resizable textarea
const txta = document.getElementsByTagName('textarea');
for (let i = 0; i < txta.length; i++) {
  txta[i].setAttribute('style', 'height:' + (txta[i].scrollHeight) + 'px;overflow-y:hidden;');
  txta[i].addEventListener("input", OnInput, false);
}

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}

// send filesize as a cookie
function filesize(elem){
    document.cookie = `filesize=${elem.files[0].size}`;
  }
