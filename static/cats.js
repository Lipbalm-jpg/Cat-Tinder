console.log('{{ catsarray }}');
var acatarray = document.getElementById("datadiv").dataset.catsarray;

var datadiv = document.getElementById("datadiv");
fetch("/catsdata")
.then(res => res.json())
.then(data => console.log(data));

for (let i = 0; i < acatarray.length; i++){
    let catdiv = document.createElement("div");
    catdiv.innertext = acatarray[i];
    let catbutton = document.createElement("button");

    catbutton.dataset.id = i + 1;
    datadiv.appendChild(catdiv);
    datadiv.appendChild(catbutton);
}