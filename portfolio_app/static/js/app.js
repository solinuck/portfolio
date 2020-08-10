const navBtn = document.querySelector("#nav-btn");
const closeBtn = document.querySelector("#close-btn");
const sidebar = document.querySelector("#sidebar");
const date = document.querySelector("#date");
const txta = document.getElementsByTagName('textarea');
const addTagBtn = document.querySelector("#add-btn");
const blogArticle = document.querySelector(".blog-article");
const expandSearchBtn = document.querySelector(".expand-search-btn");


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
const searchForm = document.getElementById("search-form");
if (searchInput) {
  searchInput.addEventListener("keydown", function(e) {
    if (e.keyCode === 13) {
      e.preventDefault();
      searchForm.action = `/blog/${searchInput.value}`;
      document.getElementById("search-btn").click();
    }
  });
}

if (blogArticle) {
  const otherArticles = document.querySelector(".other-articles");
  if (otherArticles.childNodes.length === 1) {
    otherArticles.classList.remove("article-footer");
    otherArticles.classList.add("article-footer-only-one");

  }
}

if (expandSearchBtn) {
  const expandSearchArrow = document.querySelector(".fa-angle-down");
  const searchContainer = document.querySelector(".expanded-blog-search");
  const articlesSection = document.querySelector(".blog-articles");
  expandSearchBtn.addEventListener("click", function() {
    articlesSection.classList.toggle("blog-articles-small");
    if (expandSearchArrow.classList.contains("rotate")) {
      searchContainer.classList.remove("z-index");
      setTimeout(function() {
        expandSearchArrow.classList.toggle("rotate");
        searchContainer.classList.toggle("show-blog-search");
      }, 200);
    } else {
      expandSearchArrow.classList.toggle("rotate");
      searchContainer.classList.toggle("show-blog-search");
      setTimeout(function() {
        searchContainer.classList.toggle("z-index");
      }, 300);
    }

  });

  const dropdownBtns = document.querySelectorAll("#dropdown-btn");
  const yearOptions = document.querySelector(".year-option");
  const monthOptions = document.querySelector(".month-option");

  dropdownBtns.forEach((btn) => {
    const dropdownContent = btn.nextElementSibling;
    btn.addEventListener("click", () => {
      dropdownContent.classList.toggle("show");
    });

    window.addEventListener("click", function(event) {
      if (event.target != btn && event.target.parentElement != btn) {
        if (dropdownContent.classList.contains("show")) {
          dropdownContent.classList.remove("show");
        }
      }
    });
  });


}