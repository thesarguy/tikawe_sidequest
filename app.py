import secrets
import sqlite3

from flask import Flask, abort, flash, redirect, render_template, request, session

import config
import db
import sidequests
import users

app = Flask(__name__)
app.secret_key = config.secret_key

#closes database connection automatically at the end of each request
app.teardown_appcontext(db.close_connection)

#these lists define allowed values for difficulty and duration
#passed to templates to fill dropdown menus
DIFFICULTIES = ["helppo", "keskitaso", "haastava", "erittäin haastava"]
LENGTHS = ["alle 15 min", "15–30 min", "30–60 min", "1–3 tuntia", "useita tunteja", "useita päiviä"]


def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/")
def index():
    all_quests = sidequests.get_all_quests()
    completed_ids = set()
    if "user_id" in session:
        completed_ids = sidequests.get_completed_ids(session["user_id"])
    return render_template("index.html", quests=all_quests, completed_ids=completed_ids)


@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    difficulty = request.args.get("difficulty", "")
    duration = request.args.get("duration", "")
    tag_id = request.args.get("tag_id", "")
    results = sidequests.find_quests(query, difficulty, duration, tag_id)
    all_tags = sidequests.get_all_tags()
    return render_template("search.html", results=results, query=query,
                           difficulty=difficulty, duration=duration,
                           tag_id=tag_id, difficulties=DIFFICULTIES,
                           lengths=LENGTHS, all_tags=all_tags)


@app.route("/quest/<int:quest_id>")
def show_quest(quest_id):
    quest = sidequests.get_quest(quest_id)
    if not quest:
        abort(404)
    tags = sidequests.get_quest_tags(quest_id)
    comments = sidequests.get_comments(quest_id)
    completion_count = sidequests.get_completion_count(quest_id)
    user_completed = None
    if "user_id" in session:
        user_completed = sidequests.get_completion(quest_id, session["user_id"])
    return render_template("quest.html", quest=quest, tags=tags, comments=comments,
                           completion_count=completion_count, user_completed=user_completed)


@app.route("/complete_quest", methods=["POST"])
def complete_quest():
    require_login()
    check_csrf()
    quest_id = request.form.get("quest_id")
    if not sidequests.get_quest(quest_id):
        abort(404)
    sidequests.add_completion(quest_id, session["user_id"])
    flash("Quest marked as completed!")
    return redirect("/quest/" + str(quest_id))


@app.route("/uncomplete_quest", methods=["POST"])
def uncomplete_quest():
    require_login()
    check_csrf()
    quest_id = request.form.get("quest_id")
    if not sidequests.get_quest(quest_id):
        abort(404)
    sidequests.remove_completion(quest_id, session["user_id"])
    flash("Quest marked as incomplete.")
    return redirect("/quest/" + str(quest_id))


@app.route("/new_quest")
def new_quest():
    require_login()
    all_tags = sidequests.get_all_tags()
    return render_template("new_quest.html", difficulties=DIFFICULTIES,
                           lengths=LENGTHS, all_tags=all_tags)


@app.route("/create_quest", methods=["POST"])
def create_quest():
    require_login()
    check_csrf()
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    instructions = request.form.get("instructions", "").strip()
    difficulty = request.form.get("difficulty", "")
    duration = request.form.get("duration", "")
    selected_tags = request.form.getlist("tags")
    if not title or len(title) > 100:
        abort(403)
    if not description or len(description) > 2000:
        abort(403)
    sidequests.add_quest(title, description, instructions, difficulty, duration, session["user_id"])
    quest_id = db.last_insert_id()
    sidequests.save_quest_tags(quest_id, selected_tags)
    flash("Sidequest lisätty!")
    return redirect("/quest/" + str(quest_id))


@app.route("/edit_quest/<int:quest_id>")
def edit_quest(quest_id):
    require_login()
    quest = sidequests.get_quest(quest_id)
    if not quest:
        abort(404)
    #confirm only owner of quest can edit it
    if quest["user_id"] != session["user_id"]:
        abort(403)
    all_tags = sidequests.get_all_tags()
    current_tag_ids = {row["id"] for row in sidequests.get_quest_tags(quest_id)}
    return render_template("edit_quest.html", quest=quest,
                           difficulties=DIFFICULTIES, lengths=LENGTHS,
                           all_tags=all_tags, current_tag_ids=current_tag_ids)


@app.route("/update_quest", methods=["POST"])
def update_quest():
    require_login()
    check_csrf()
    quest_id = request.form.get("quest_id")
    quest = sidequests.get_quest(quest_id)
    if not quest:
        abort(404)
    if quest["user_id"] != session["user_id"]:
        abort(403)
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    instructions = request.form.get("instructions", "").strip()
    difficulty = request.form.get("difficulty", "")
    duration = request.form.get("duration", "")
    selected_tags = request.form.getlist("tags")
    if not title or len(title) > 100 or not description or len(description) > 2000:
        abort(403)
    sidequests.update_quest(quest_id, title, description, instructions, difficulty, duration)
    sidequests.save_quest_tags(quest_id, selected_tags)
    flash("Sidequest päivitetty!")
    return redirect("/quest/" + str(quest_id))


@app.route("/remove_quest/<int:quest_id>", methods=["GET", "POST"])
def remove_quest(quest_id):
    require_login()
    quest = sidequests.get_quest(quest_id)
    if not quest:
        abort(404)
    #only quest's creator can delete it
    if quest["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        #confirmation before deleting 
        return render_template("delete_quest.html", quest=quest)
    check_csrf()
    if "confirm" in request.form:
        #"soft delete", changes status to 0 instead of removing from database
        sidequests.remove_quest(quest_id)
        flash("Quest deleted.")
        return redirect("/")
    return redirect("/quest/" + str(quest_id))


@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()
    quest_id = request.form.get("quest_id")
    quest = sidequests.get_quest(quest_id)
    if not quest:
        abort(404)
    content = request.form.get("content", "").strip()
    if not content or len(content) > 1000:
        abort(403)
    sidequests.add_comment(quest_id, session["user_id"], content)
    flash("Kommentti lisätty!")
    return redirect("/quest/" + str(quest_id))


@app.route("/remove_comment", methods=["POST"])
def remove_comment():
    require_login()
    check_csrf()
    comment_id = request.form.get("comment_id")
    comment = sidequests.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)
    quest_id = comment["sidequest_id"]
    sidequests.remove_comment(comment_id)
    flash("Kommentti poistettu.")
    return redirect("/quest/" + str(quest_id))


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_quests = users.get_quests(user_id)
    stats = users.get_stats(user_id)
    return render_template("user.html", user=user, quests=user_quests, stats=stats)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form.get("username", "").strip()
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")
    if not username or len(username) > 20:
        flash("VIRHE: Käyttäjätunnus on pakollinen (max 20 merkkiä)")
        return redirect("/register")
    if password1 != password2:
        flash("VIRHE: Salasanat eivät täsmää")
        return redirect("/register")
    if len(password1) < 6:
        flash("VIRHE: Salasanan tulee olla vähintään 6 merkkiä")
        return redirect("/register")
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: Käyttäjätunnus on jo varattu")
        return redirect("/register")
    flash("Tunnus luotu! Voit nyt kirjautua sisään.")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer or "/")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    next_page = request.form.get("next_page", "/")
    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect(next_page)
    flash("VIRHE: Väärä tunnus tai salasana")
    return render_template("login.html", next_page=next_page, username=username)


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

