const navbar = document.querySelector("#nav");
const navBtn = document.querySelector("#nav-btn");
const closeBtn = document.querySelector("#close-btn");
const sidebar = document.querySelector("#sidebar");
const date = document.querySelector("#date");
const txta = document.getElementsByTagName('textarea');
const addTagBtn = document.querySelector("#add-btn");


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
for (let i = 0; i < txta.length; i++) {
  txta[i].setAttribute('style', 'height:' + (txta[i].scrollHeight) +
    'px;overflow-y:hidden;');
  txta[i].addEventListener("input", OnInput, false);
}

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}

// send filesize as a cookie
function filesize(elem) {
  document.cookie = `filesize=${elem.files[0].size}`;
}


// add and delete tags
if (addTagBtn) {
  const deleteTagBtn = document.querySelector(".delete-tag-btn");
  const articleTags = document.querySelector(".article-tags");
  const tagText = document.querySelector(".tag-text");
  addTagBtn.addEventListener("click", function() {
    // if (articleTags.childNodes.length < 5) {
    let input = document.createElement('input');
    input.type = "text";
    input.name = `tag-${articleTags.childNodes.length}`;
    input.classList.add("create-tag");
    articleTags.appendChild(input);
    tagText.classList.remove("show");
    // }
  });

  deleteTagBtn.addEventListener("click", function() {
    if (articleTags.firstChild) {
      articleTags.removeChild(articleTags.lastChild);
      if (articleTags.childNodes.length === 0) {
        tagText.classList.add("show");
      }
    }
  });

  // show image name for image input in create_article
  const input = document.querySelector('.hidden-btn');
  const selectedImage = document.querySelector('.selected-image');

  input.addEventListener('change', function(e) {
    let fileName = e.target.value.split("\\").pop();

    selectedImage.innerText = fileName;
  });
}

// submit search on pressing enter
const searchInput = document.querySelector(".search");
// const currentSearch = document.querySelector(".current-search")
if (searchInput) {
  searchInput.addEventListener("keydown", function(e) {
    if (e.keyCode === 13) {
      e.preventDefault();
      document.getElementById("search-btn").click();
    }
  });
}