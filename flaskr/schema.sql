DROP TABLE IF EXISTS login;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users_books;

CREATE TABLE login (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE users (
  id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE books (
id TEXT UNIQUE NOT NULL,
name TEXT NOT NULL,
author TEXT,
publisher TEXT,
yera_of_publication INTEGER );

CREATE TABLE users_books (
  ownerid TEXT NOT NULL,
  bookid TEXT,
  possessedid TEXT
);