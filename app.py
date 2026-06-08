from flask import Flask, request, redirect, url_for, jsonify, render_template
import sqlite3
import re

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
    """)

    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS likes (
        receiverid INTEGER,
        likeid INTEGER,
        PRIMARY KEY (receiverid, likeid),
        FOREIGN KEY (likeid) REFERENCES cats (id),
        FOREIGN KEY (receiverid) REFERENCES cats (id)
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

@app.route("/likesData", methods = ["GET"])
def get_likes():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    con.close()
    return jsonify(likes)

@app.route("/add", methods = ["POST", "GET"])
def add_info():
    return render_template("add.html")

@app.route("/submit", methods = ["POST"])
def submit():
    file = request.files.get("image")
    catname = request.form.get("name")
    catage = request.form.get("age")
    catbio = request.form.get("bio")
    if file: 
        catimage = file.read()
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO cats (name, age, bio, image) VALUES (?, ?, ?, ?)", (catname, catage, catbio, catimage))
    con.commit() 
    con.close()
    return redirect(url_for("get_cats"))
    #Submit

@app.route("/loadprofile")
def showProfile():
    return render_template("profile.html")

@app.route("/loadchunk", methods = ["GET", "POST"])
def loadchunk():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM cats WHERE id !=" + str(request.args.get('query')))
    cats = cur.fetchall()
    con.close()
    print(request.values)
    return jsonify(cats)

@app.route("/swipe", methods = ["POST"])
def swipeRight():
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO likes VALUES (" + str(request.args.get('receiverid')) + ", " + str(request.args.get('likeid')) + ")")
    con.commit()
    con.close()
    return ("Hello world!")

@app.route("/image")
def get_Image():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT image FROM cats WHERE id=?", (cat_id, ))
    row = cur.fetchone()
    con.close()
    return (row[0], 200, {"Content-Type":"image/jpeg"})

if __name__ == "__main__":
    app.run()
