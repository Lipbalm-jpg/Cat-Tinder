console.log('{{ catsarray }}');
var acatarray = [];

var datadiv = document.getElementById("datadiv");
fetch("/catsdata")
.then(res => res.json())
.then(data => { 
    acatarray.push(...data)
    console.log(acatarray);

    for (let i = 0; i < acatarray.length; i++){
        let catdiv = document.createElement("p");
        catdiv.textContent = acatarray[i][1];
        let tupperwarediv = document.createElement("div");
        let catbutton = document.createElement("button");
        catbutton.onClick = () => {
            localStorage.setItem("userID", this.dataset.id);
        window.location.href = '../';
        }

        catbutton.dataset.id = i + 1;
        tupperwarediv.appendChild(catdiv);
        datadiv.appendChild(tupperwarediv);
        tupperwarediv.appendChild(catbutton);
        tupperwarediv.style = "display:flex;";
        console.log(acatarray[i][1]);
    }
}
);
