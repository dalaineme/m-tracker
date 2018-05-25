var form_el = document.getElementById("login-form");
form_el.addEventListener("submit", function(evt) {
  evt.preventDefault();
  loginFunction();
});
function loginFunction() {
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;
  if (email == "admin@admin.com") {
    window.location.href = "admin/index.html";
  } else {
    window.location.href = "user/index.html";
  }
}
