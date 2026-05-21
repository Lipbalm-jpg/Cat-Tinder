var userData;

if (localStorage.getItem("userID")) {
    var userInfo = localStorage.getItem("userID");
}
else {
    window.alert("You haven't selected a profile yet");
}
fetch("/loadchunk?query=" + userInfo, {"userInfo": userInfo})
.then(response => response.json())
.then(data => {userData = data;
    var nameDisplay = document.getElementById("cat_name");
    nameDisplay.textContent = userData[0][1];
});
