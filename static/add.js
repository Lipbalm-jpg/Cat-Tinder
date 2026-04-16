import sqlite3 from "sqlite3";

export function addCat() {
    const db = sqlite3.Database(cats.db)
    debugger;
    
    db.run("INSERT INTO cats VALUES (name, bio, age, image)", [
        document.getElementById("fname").value,
        document.getElementById("bio").value,
        document.getElementById("age").value,
        document.getElementById("image").value
    ]);
    console.log(db.exec("SELECT * FROM cats"));
    db.close();

    return("Cat added to database");
}