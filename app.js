const gentlemenCats = [
    { name: "Sir Whiskers", img: "images/sir_whiskers.jpg" },
    { name: "Mr. Fluffington", img: "images/fluffington.jpg" },
    { name: "Duke Paws", img: "images/duke_paws.jpg" },
    { name: "Lord Meowington", img: "images/lord_meowington.jpg" },
    { name: "Captain Claws", img: "images/captain_claws.jpg" },
    { name: "Baron Von Purr", img: "images/baron_purr.jpg" },
    { name: "Professor Snuggles", img: "images/professor_snuggles.jpg" }
];

const ladyCats = [
    { name: "Princess Purr", img: "images/princess_purr.jpg" },
    { name: "Lady Meow", img: "images/lady_meow.jpg" },
    { name: "Queen Mittens", img: "images/queen_mittens.jpg" },
    { name: "Duchess Fluffy", img: "images/duchess_fluffy.jpg" },
    { name: "Miss Whiskerina", img: "images/whiskerina.jpg" },
    { name: "Countess Cuddles", img: "images/countess_cuddles.png" },
    { name: "Empress Snowpaw", img: "images/snowpaw.jpg" }
];

let catslist = [];

async function loadCats(){
    let result = await fetch("/cats");
    catslist = await result.json();
    console.log(catslist);
}

let currentList = [];
let index = 0;

function start(type) {
    document.getElementById("startScreen").classList.add("hidden");
    document.getElementById("app").classList.remove("hidden");

    if (type === "gentlemen") {
        currentList = gentlemenCats;
        document.getElementById("categoryTitle").innerText = "Gentlemen Cats 🎩";
    } else {
        currentList = ladyCats;
        document.getElementById("categoryTitle").innerText = "Lady Cats 🎀";
    }

    index = 0;
    showCat();
}

function showCat() {
    const cat = currentList[index];
    document.getElementById("catImage").src = cat.img;
    document.getElementById("catName").innerText = cat.name;
}

function nextCat() {
    index = (index + 1) % currentList.length;
    showCat();
}

function matchCat() {
    const cat = currentList[index];

    const li = document.createElement("li");
    li.innerText = cat.name;

    document.getElementById("matchList").appendChild(li);

    nextCat();
}
function goHome() {
    // Hide app, show start screen
    document.getElementById("app").classList.add("hidden");
    document.getElementById("startScreen").classList.remove("hidden");

    // Reset matches
    document.getElementById("matchList").innerHTML = "";

    // Reset index
    index = 0;
}

loadCats();