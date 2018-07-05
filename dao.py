import sqlite3
from connection import commit_close
from settings import DB_NAME

benefits = ["BAE", "AC"]

class Students:
	def __init__(self, pk='0', name="", benefit="", id_per_benefit='0'):
		self.pk = pk
		self.name = name
		self.benefit = benefit
		self.id_per_benefit = id_per_benefit

	@commit_close
	def save(self):
		if self.benefit not in benefits:
			raise ValueError('benefit {} is not available'.format(self.benefit))
		else:
			self.id_per_benefit = self.define_id_per_benefit()
			return """
			INSERT INTO proccess(name, benefit, id_per_benefit)
				VALUES('{}', '{}', '{}')
			""".format(self.name, self.benefit, self.id_per_benefit)

	def define_id_per_benefit(self):
		l = list_all(self.benefit)
		if len(l) == 0: return 1
		con = sqlite3.connect(DB_NAME)
		cur = con.cursor()
		sql = """
		SELECT MAX(id_per_benefit) from proccess where benefit='{}'
		""".format(self.benefit)
		cur.execute(sql)
		data = cur.fetchall()
		con.close()
		return data[0][0] + 1


	def __repr__(self):
		return "<pk: {}, name: {}, benefit: {}, id_per_benefit: {}>".format(self.pk,
								self.name, self.benefit, self.id_per_benefit)

def list_all(benefit=None):
	con = sqlite3.connect(DB_NAME)
	cur = con.cursor()

	sql = ""
	if benefit:		
		sql = """
		SELECT id, name, benefit, id_per_benefit
		FROM proccess WHERE benefit='{}'""".format(benefit)
	else:
		sql = """
		SELECT id, name, benefit, id_per_benefit
		FROM proccess"""

	cur.execute(sql)
	data = cur.fetchall()
	con.close()
	l = []
	for d in data:
		l.append(Students(d[0], d[1], d[2], d[3]))
	return l


@commit_close
def create_db():
	return """
	CREATE TABLE IF NOT EXISTS proccess (
	    id             INTEGER PRIMARY KEY AUTOINCREMENT
	                           NOT NULL,
	    name           TEXT    NOT NULL,
	    benefit        TEXT    NOT NULL,
	    id_per_benefit INT     NOT NULL
	);
	"""

@commit_close
def delete(pk):
	return """
	DELETE FROM proccess WHERE id = '{}'
	""".format(pk)


# @commit_close
# def db_insert(name, phone, email):
# 	return """
# 	INSERT INTO users(name, phone, email)
# 		VALUES('{}', '{}', '{}')
# 	""".format(name, phone, email)


# @commit_close
# def db_update(name, email):
# 	return """
# 	UPDATE users SET name = '{}' WHERE email = '{}'
# 	""".format(name, email)

# @commit_close
# def db_delete(email):	
# 	return """
# 	DELETE FROM users WHERE email='{}'
# 	""".format(email)


# def db_select(data, field):
# 	con = sqlite3.connect('base.db')
# 	cur = con.cursor()
# 	sql = """
# 	SELECT id, name, phone, email
# 	FROM users
# 	WHERE {}={}""".format(field, data)

# 	cur.execute(sql)
# 	data = cur.fetchall()
# 	con.close()
# 	return data