DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS mangroves;


CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE models (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model_name TEXT UNIQUE NOT NULL,
  model_path TEXT NOT NULL,
  is_active INTEGER NOT NULL
);

CREATE TABLE mangroves (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  data_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  banner_path TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);