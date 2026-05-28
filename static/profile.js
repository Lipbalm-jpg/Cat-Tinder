var userData;
var nameDisplay = document.getElementById("cat_name");
var ageDisplay = document.getElementById("cat_age");
var bioDisplay = document.getElementById("cat_bio");
var imageDisplay = document.getElementById("cat_image")
var catIndex = 0;

if (localStorage.getItem("userID")) {
    var userInfo = localStorage.getItem("userID");
}
else {
    window.alert("You haven't selected a profile yet");
}
fetch("/loadchunk?query=" + userInfo, {"userInfo": userInfo})
.then(response => response.json())
.then(data => {userData = data;
    nameDisplay.textContent = userData[0][1];
    ageDisplay.textContent = userData[0][2];
    bioDisplay.textContent = userData[0][3];
    imageDisplay.src = userData[0][4];
    
});

function updateCat() {
    catIndex++;
    nameDisplay.textContent = userData[catIndex][1];
    ageDisplay.textContent = userData[catIndex][2];
    bioDisplay.textContent = userData[catIndex][3];
    userData[catIndex][4]?imageDisplay.src = userData[catIndex][4]:imageDisplay.src = "../static/IMG/fluffington.jpg";
}

function swipeRight() {
    fetch("/swipe?receiverid=" + receiverid + "&likeid=" + likeid)
    .then(response => console.log(response));
    updateCat();
}