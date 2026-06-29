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
    cur.execute("SELECT id, name, age, bio FROM cats")
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
    catimage = None
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
    cur.execute("SELECT id, name, age, bio FROM cats WHERE id !=" + str(request.args.get('query')))
    cats = cur.fetchall()
    con.close()
    print(request.values)
    return jsonify(cats)

@app.route("/swipe", methods = ["POST"])
def swipeRight():
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO likes  (receiverid, likeid) VALUES (?,?)", (str(request.args.get('receiverid')), str(request.args.get('likeid'))))
    # cur.execute("INSERT OR IGNORE INTO likes  (" + str(request.args.get('receiverid')) + ", " + str(request.args.get('likeid')) + ")")
    con.commit()
    cur.execute("SELECT A.receiverid AS likedCatA, B.receiverid AS likedCatB, A.likeid AS likerCatA, B.likeid AS likerCatB FROM likes A, likes B WHERE likedCatA = likerCatB AND likedCatB = likerCatA AND likedCatA < likedCatB AND likerCatA = " + str(request.args.get('receiverid')))
    result = cur.fetchone()
    con.close()
    if result:
        print("result")
        return(jsonify(result))
    print("not result")
    return(jsonify("Hello world!"))

@app.route("/image", methods = ["GET"])
def get_Image():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT image FROM cats WHERE id=?", (request.args.get('cat_id'),))
    row = cur.fetchone()
    con.close()
    if row is None:
        return("Cat not found", 404)
    if row[0] is None:
        return(redirect(url_for('static', filename='IMG/fluffington.jpg')))
    return (row[0], 200, {"Content-Type":"image/jpeg"})

@app.route("/matches", methods = ["GET"])
def get_Matches():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
    SELECT A.receiverid AS likedCatA, B.receiverid AS likedCatB, A.likeid AS likerCatA, B.likeid AS likerCatB 
    FROM likes A, likes B
    WHERE likedCatA = likerCatB
    AND likedCatB = likerCatA
    AND likedCatA < likedCatB
    """)
    row = cur.fetchall()
    con.close()
    return jsonify(row)

if __name__ == "__main__":
    app.run()
