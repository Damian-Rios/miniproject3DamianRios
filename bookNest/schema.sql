DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS favorite;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL
);


CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    rating REAL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(id)
);


CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(book_id) REFERENCES book(id)
);


CREATE TABLE favorite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(book_id) REFERENCES book(id)
);