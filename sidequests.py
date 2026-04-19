import db


def get_all_quests():
    sql = """SELECT s.id, s.title, s.description, s.difficulty, s.estimated_duration,
                    s.created_at, u.username, u.id user_id
             FROM sidequests s JOIN users u ON s.user_id = u.id
             WHERE s.status = 1 ORDER BY s.id DESC"""
    return db.query(sql)


def get_quest(quest_id):
    sql = """SELECT s.*, u.username, u.id user_id
             FROM sidequests s JOIN users u ON s.user_id = u.id
             WHERE s.id = ? AND s.status = 1"""
    result = db.query(sql, [quest_id])
    return result[0] if result else None

def get_completed_ids(user_id):
    sql = "SELECT quest_id FROM completions WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return {row["quest_id"] for row in result}


def add_quest(title, description, instructions, difficulty, duration, user_id):
    sql = """INSERT INTO sidequests
             (title, description, instructions, difficulty, estimated_duration, user_id, created_at)
             VALUES (?, ?, ?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [title, description, instructions, difficulty, duration, user_id])


def update_quest(quest_id, title, description, instructions, difficulty, duration):
    sql = """UPDATE sidequests
             SET title=?, description=?, instructions=?, difficulty=?, estimated_duration=?
             WHERE id=?"""
    db.execute(sql, [title, description, instructions, difficulty, duration, quest_id])


def remove_quest(quest_id):
    sql = "UPDATE sidequests SET status = 0 WHERE id = ?"
    db.execute(sql, [quest_id])


def find_quests(query, difficulty, duration, tag_id):
    sql = """SELECT DISTINCT s.id, s.title, s.description, s.difficulty, s.estimated_duration,
                    s.created_at, u.username, u.id user_id
             FROM sidequests s JOIN users u ON s.user_id = u.id
             LEFT JOIN sidequest_tags st ON s.id = st.sidequest_id
             WHERE s.status = 1"""
    params = []
    if query:
        sql += " AND (s.title LIKE ? OR s.description LIKE ? OR s.instructions LIKE ?)"
        params += [f"%{query}%", f"%{query}%", f"%{query}%"]
    if difficulty:
        sql += " AND s.difficulty = ?"
        params.append(difficulty)
    if duration:
        sql += " AND s.estimated_duration = ?"
        params.append(duration)
    if tag_id:
        sql += " AND st.tag_id = ?"
        params.append(tag_id)
    sql += " ORDER BY s.id DESC"
    return db.query(sql, params)


def get_all_tags():
    sql = "SELECT id, name FROM tags ORDER BY name"
    return db.query(sql)


def get_quest_tags(quest_id):
    sql = """SELECT t.id, t.name FROM tags t
             JOIN sidequest_tags st ON t.id = st.tag_id
             WHERE st.sidequest_id = ?"""
    return db.query(sql, [quest_id])


def save_quest_tags(quest_id, tag_ids):
    db.execute("DELETE FROM sidequest_tags WHERE sidequest_id = ?", [quest_id])
    for tag_id in tag_ids:
        db.execute(
            "INSERT OR IGNORE INTO sidequest_tags (sidequest_id, tag_id) VALUES (?, ?)",
            [quest_id, tag_id]
        )


def get_comments(quest_id):
    sql = """SELECT c.id, c.content, c.created_at, u.username, u.id user_id
             FROM comments c JOIN users u ON c.user_id = u.id
             WHERE c.sidequest_id = ?
             ORDER BY c.id ASC"""
    return db.query(sql, [quest_id])


def get_comment(comment_id):
    sql = "SELECT * FROM comments WHERE id = ?"
    result = db.query(sql, [comment_id])
    return result[0] if result else None


def add_comment(quest_id, user_id, content):
    sql = """INSERT INTO comments (sidequest_id, user_id, content, created_at)
             VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [quest_id, user_id, content])


def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])


def get_completion(quest_id, user_id):
    sql = "SELECT id FROM completions WHERE quest_id = ? AND user_id = ?"
    result = db.query(sql, [quest_id, user_id])
    return result[0] if result else None


def add_completion(quest_id, user_id):
    sql = """INSERT OR IGNORE INTO completions (quest_id, user_id, completed_at)
             VALUES (?, ?, datetime('now'))"""
    db.execute(sql, [quest_id, user_id])


def remove_completion(quest_id, user_id):
    sql = "DELETE FROM completions WHERE quest_id = ? AND user_id = ?"
    db.execute(sql, [quest_id, user_id])


def get_completion_count(quest_id):
    sql = "SELECT COUNT(*) FROM completions WHERE quest_id = ?"
    result = db.query(sql, [quest_id])
    return result[0][0]