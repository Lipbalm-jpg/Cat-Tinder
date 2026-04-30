from flask import Flask, request, redirect, url_for, jsonify, render_template
import sqlite3

app = Flask(__name__)

db = "cats.db"

def get_db():
    return sqlite3.connect(db)

@app.route("/")
def home_db():
    return render_template("index.html")

@app.route("/init")
def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TINYINT,
        bio TEXT,
        image BLOB
    )
    """
    )
    cur.execute("INSERT INTO cats (name, age, bio) VALUES ('Max', '6', 'Likes long walks on the beach')")
#To do: handle likes

    con.commit()
    con.close()
    return("Database initialized")

#To do: create cats

@app.route("/cats", methods = ["GET"])
def get_cats():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM cats")
    cats = cur.fetchall()
    results = [
        {"id": cat[0], "name": cat[1], "age": cat[2], "bio": cat[3], "image": cat[4]}
        for cat in cats
    ]
    con.close()
    print(results)
    return render_template("cats.html", catsarray = results)

@app.route("/catsdata", methods = ["GET"])
def get_data():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM cats")
    cats = cur.fetchall()
    con.close()
    return jsonify(cats)

@app.route("/add", methods = ["POST", "GET"])
def add_info():
    return render_template("add.html")

@app.route("/submit", methods = ["POST"])
def submit():
    catname = request.form.get("name")
    catage = request.form.get("age")
    catbio = request.form.get("bio")
    catimage = request.form.get("image")
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO cats (name, age, bio, image) VALUES (?, ?, ?, ?)", (catname, catage, catbio, catimage))
    con.commit() 
    con.close()
    return redirect(url_for("get_cats"))
    #Submit

if __name__ == "__main__":
    app.run()
