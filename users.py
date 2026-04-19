from werkzeug.security import check_password_hash, generate_password_hash
import db


def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None


def get_quests(user_id):
    sql = """SELECT id, title, difficulty, estimated_duration, created_at
             FROM sidequests WHERE user_id = ? AND status = 1 ORDER BY id DESC"""
    return db.query(sql, [user_id])


def get_stats(user_id):
    sql = """
        SELECT
            (SELECT COUNT(*) FROM sidequests WHERE user_id = ? AND status = 1) AS quest_count,
            (SELECT COUNT(*) FROM comments WHERE user_id = ?) AS comments_sent,
            (SELECT COUNT(*) FROM comments c JOIN sidequests s ON c.sidequest_id = s.id
             WHERE s.user_id = ? AND s.status = 1) AS comments_received,
            (SELECT COUNT(*) FROM completions WHERE user_id = ?) AS quests_completed
    """
    result = db.query(sql, [user_id, user_id, user_id, user_id])
    return result[0] if result else None


def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])


def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None