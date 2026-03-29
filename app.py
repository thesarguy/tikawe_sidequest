from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import config

app = Flask(__name__)
app.secret_key = config.secret_key




#ALOITUSSIVUN JUTUT
@app.route("/")
def index():
    db = get_db()
    sort = request.args.get("sort", "name")
    search = request.args.get("search", "")
    
    if sort == "time_asc":
        order = "CASE time_estimate WHEN '<15min' THEN 1 WHEN '15-30min' THEN 2 WHEN '30min-1h' THEN 3 WHEN '1h-2h' THEN 4 WHEN '>2h' THEN 5 END"
    elif sort == "time_desc":
        order = "CASE time_estimate WHEN '<15min' THEN 1 WHEN '15-30min' THEN 2 WHEN '30min-1h' THEN 3 WHEN '1h-2h' THEN 4 WHEN '>2h' THEN 5 END DESC"
    elif sort == "completed":
        order = "completed DESC, name"
    else:
        order = "name"
    
    sidequests = db.execute("SELECT * FROM sidequests WHERE name LIKE ? ORDER BY " + order,
                            ["%" + search + "%"]).fetchall()
    db.close()
    return render_template("index.html", sidequests=sidequests, sort=sort, search=search)


#DATABASE
def get_db(): 
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db


#UUDEN KÄYTTÄJÄN LUONTI
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"
        password_hash = generate_password_hash(password1)
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", [username, password_hash])
            db.commit()
            return redirect("/")
        except:
            return "VIRHE: käyttäjänimi on jo käytössä"
        finally:
            db.close()
    return render_template("register.html")

#KIRJAUTUMINEN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", [username]).fetchone()
        db.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")
        return "VIRHE: väärä käyttäjänimi tai salasana"
    return render_template("login.html")



#ULOSKIRJAUTUMINEN
@app.route("/logout") 
def logout():
    session.clear()
    return redirect("/")



#SIDEQUESTIN LUONTI
@app.route("/new", methods=["GET", "POST"])
def new():
    if not session.get("user_id"):
        return redirect("/login")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        time_estimate = request.form["time_estimate"]
        db = get_db()
        db.execute("INSERT INTO sidequests (name, description, time_estimate, user_id) VALUES (?, ?, ?, ?)",
                   [name, description, time_estimate, session["user_id"]])
        db.commit()
        db.close()
        return redirect("/")
    return render_template("new.html")



#SIDEQUESTIN TIEDOT
@app.route("/quest/<int:id>")
def quest(id):
    db = get_db()
    quest = db.execute("SELECT * FROM sidequests WHERE id=?", [id]).fetchone()
    db.close()
    if not quest:
        return "Questia ei löydy"
    return render_template("quest.html", quest=quest)


#SUORITTAMISEKSI MERKKAUS
@app.route("/complete/<int:id>")
def complete(id):
    if not session.get("user_id"):
        return redirect("/login")
    db = get_db()
    quest = db.execute("SELECT * FROM sidequests WHERE id=?", [id]).fetchone()
    if quest["completed"]:
        db.execute("UPDATE sidequests SET completed=0 WHERE id=?", [id])
    else:
        db.execute("UPDATE sidequests SET completed=1 WHERE id=?", [id])
    db.commit()
    db.close()
    return redirect("/quest/" + str(id))


#MUOKKAUS
@app.route("/edit/<int:id>", methods=["GET", "POST"]) 
def edit(id):
    if not session.get("user_id"):
        return redirect("/login")
    db = get_db()
    quest = db.execute("SELECT * FROM sidequests WHERE id=?", [id]).fetchone()
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        time_estimate = request.form["time_estimate"]
        db.execute("UPDATE sidequests SET name=?, description=?, time_estimate=? WHERE id=?",
                   [name, description, time_estimate, id])
        db.commit()
        db.close()
        return redirect("/quest/" + str(id))
    db.close()
    return render_template("edit.html", quest=quest)


#POISTAMINEN
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("user_id"):
        return redirect("/login")
    db = get_db()
    db.execute("DELETE FROM sidequests WHERE id=?", [id])
    db.commit()
    db.close()
    return redirect("/")