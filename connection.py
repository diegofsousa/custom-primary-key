import sqlite3
from settings import DB_NAME

def commit_close(func):
	def decorator(*args):
		con = sqlite3.connect(DB_NAME)
		cur = con.cursor()
		sql = func(*args)
		cur.execute(sql)
		con.commit()
		con.close()
	return decorator