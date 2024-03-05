import sqlite3

con = sqlite3.connect("../db/Rockandplaydb.db")
cur = con.execute("""

CREATE TABLE Games
(
  id INTEGER NOT NULL ,
  name TEXT,
  genere TEXT,
  description TEXT,
  Pic TEXT,
  link TEXT,
  CONSTRAINT PK_Games PRIMARY KEY (id)
  UNIQUE (name)
);
""")
cur = con.execute("""
CREATE TABLE Players
(
  id INTEGER NOT NULL ,
  name TEXT,
  last_name TEXT,
  password TEXT,
  email TEXT,
  genere TEXT,
  CONSTRAINT PK_Players PRIMARY KEY (id)
  UNIQUE (name, last_name)
  
);""")
cur = con.execute("""
-- Table Games-Players

CREATE TABLE Games_Players
(
  id_Game INTEGER NOT NULL,
  id_player INTEGER NOT NULL,
  CONSTRAINT PK_Games_Players PRIMARY KEY (id_Game,id_player),
  CONSTRAINT Games_Game_Player FOREIGN KEY (id_Game) REFERENCES Games (id),
  CONSTRAINT Games_Player_Game FOREIGN KEY (id_player) REFERENCES Players (id)
);
""")