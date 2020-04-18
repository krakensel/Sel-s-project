import sqlite3
import random
conn = sqlite3.connect("materials.db")
cursor = conn.cursor()


def make_result(s, lvl, t="-"):
	# Если указан тип - вывести ссылку этого типа 
	if t == "-":
		sql = f"SELECT link FROM Links WHERE sphere='{s}' AND level='{lvl}'"
	else:
		sql = f"SELECT link FROM Links WHERE sphere='{s}' AND level='{lvl}' AND type='{t}'"
	cursor.execute(sql)
	res = cursor.fetchone()[0]
	card = f"Вот материал по теме {s} уровня {lvl}: {res}"
	return card

print(make_result("Программирование", "Начальный", "Видео"))

# cursor.execute('''
# 	CREATE TABLE Links (
# 	id integer PRIMARY KEY AUTOINCREMENT,
# 	sphere text,
# 	level text,
# 	type text,
# 	link text);
# ''')

# conn.commit()

# cursor.execute('''
# 	INSERT INTO Links(sphere, level, type, link)
# 	VALUES ('Программирование', 'Начальный', 'Книга', 'asdad.asd')
# ''')
# conn.commit()



# sql = "SELECT link FROM Links WHERE sphere='Программирование'"
# cursor.execute(sql)
# a = cursor.fetchall()
# print(a)
# print(a[0])
# print(a[1])



# cursor.execute('''
# 	UPDATE Users
# 	SET state = 'size'
# 	WHERE state = 'e'
# ''')
# conn.commit()

# # colors = ['red','green', 'blue']
# # sizes = ['1','2','3']
# # states = ['q','w','e']

# # for i in range(10000):
# # 	sql = f'''
# # 		INSERT INTO Users
# # 		VALUES ({str(random.randint(10000,100000))}, '{random.choice(states)}', '{random.choice(colors)}','{random.choice(sizes)}')
# # 	'''
# # 	cursor.execute(sql)
# # 	conn.commit()






