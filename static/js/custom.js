// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

const togglePasswordVisibility = () => {
  const passwordField = document.getElementById("password-field");
  const togglePassword = document.getElementById("toggle-password");

  if (passwordField.type === "password") {
    passwordField.type = "text";
    togglePassword.innerHTML = '<i class="fa fa-eye-slash" aria-hidden="true"></i>';
  } else {
    passwordField.type = "password";
    togglePassword.innerHTML = '<i class="fa fa-eye" aria-hidden="true"></i>';
  }
};

document.getElementById("toggle-password").addEventListener("click", togglePasswordVisibility);
