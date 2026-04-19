CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
 
CREATE TABLE sidequests (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    instructions TEXT,
    estimated_duration TEXT,
    difficulty TEXT,
    user_id INTEGER REFERENCES users,
    created_at TEXT NOT NULL,
    status INTEGER DEFAULT 1
);
 
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
 
CREATE TABLE sidequest_tags (
    sidequest_id INTEGER REFERENCES sidequests ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags ON DELETE CASCADE,
    PRIMARY KEY (sidequest_id, tag_id)
);
 
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    sidequest_id INTEGER REFERENCES sidequests ON DELETE CASCADE,
    user_id INTEGER REFERENCES users,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);
 
CREATE TABLE completions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    quest_id INTEGER REFERENCES sidequests ON DELETE CASCADE,
    completed_at TEXT NOT NULL,
    UNIQUE(user_id, quest_id)
);
 
-- Seed default tags
INSERT INTO tags (name) VALUES
    ('ulkona'),
    ('sisällä'),
    ('opiskelu'),
    ('luovuus'),
    ('liikunta'),
    ('sosiaalinen'),
    ('yksin'),
    ('haastava'),
    ('helppo'),
    ('teknologia');
