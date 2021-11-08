DROP TABLE IF EXISTS photos;

CREATE TABLE photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_path TEXT NOT NULL,
    photo_name TEXT NOT NULL,
    photo_description TEXT NOT NULL
);