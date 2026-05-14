
if (localStorage.getItem("userID")) {
    var userInfo = localStorage.getItem("userID");
}
else {
    window.alert("You haven't selected a profile yet");
}
fetch("/loadchunk", {"userInfo": userInfo})
.then(response => response.json())
.then(data => console.log(data));
