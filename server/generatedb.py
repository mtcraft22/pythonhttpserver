import sqlite3

con = sqlite3.connect("../db/Rockandplaydb.db")
cur = con.execute("""


CREATE TABLE Games
(
  id integer NOT NULL,
  name TEXT,
  genere TEXT,
  description TEXT,
  image TEXT,
  link TEXT,
  CONSTRAINT PK_Games PRIMARY KEY (id)
);
""")
cur = con.execute("""
CREATE TABLE Players
(
  id integer NOT NULL,
  name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  password TEXT,
  email TEXT,
  genere TEXT,
  games TEXT,
  CONSTRAINT PK_Players PRIMARY KEY (id)
  CONSTRAINT UK_uniquePlayers unique (name,last_name)
  CONSTRAINT UK_uniquePlayersemail unique (email)         
);
""")
cur = con.execute("""



CREATE TABLE Games_Players
(
  id_Game integer NOT NULL,
  id_player integer NOT NULL,
  name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  CONSTRAINT PK_Games_Players PRIMARY KEY (id_Game,id_player,name,last_name),
  CONSTRAINT Games_Players FOREIGN KEY (id_Game) REFERENCES Games (id),
  CONSTRAINT Players_Games FOREIGN KEY (id_player) REFERENCES Players (id)
);

""")