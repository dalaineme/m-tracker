var form_el = document.getElementById("signup-form");
form_el.addEventListener("submit", function(evt) {
  evt.preventDefault();
  signupFunction();
});
function signupFunction() {
  window.location.href = "login.html";
}
