CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE sidequests (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    time_estimate TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id)
);