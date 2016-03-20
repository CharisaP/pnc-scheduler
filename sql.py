import sqlite3

with sqlite.connect("sample.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE posts")
	c.execute("CREATE TABLE posts (title TEXT, description TEST)")
	c.execute('INSERT INTO posts VALUES("good", "I\'m good.")')
	c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')