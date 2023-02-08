const allNav = document.querySelector(".nav-container");
window.onscroll = function () {
  if (document.documentElement.scrollTop > 40) {
    allNav.classList.add("sticky");
  } else {
    allNav.classList.remove("sticky");
  }
};

const responsiveNavbar = document.querySelector(".icon");
responsiveNavbar.addEventListener("click", () => {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
});

document.querySelectorAll('.card').forEach(el => {
  el.addEventListener('click', event => {
    document.querySelector('#amount').value = event.target.getAttribute('data-amount');
  });
});
