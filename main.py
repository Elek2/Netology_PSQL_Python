import psycopg2

#
# with open('bd_pass.txt') as pas_file:
# 	passw = pas_file.readline()


class ClientDataBase:
	def __init__(self, dbname, user, password):
		self.conn = psycopg2.connect(dbname=dbname, user=user, password=password)
		self.cur = self.conn.cursor()

	def create_db(self):
		self.cur.execute("""
		CREATE TABLE IF NOT EXISTS ClientData(
			id SERIAL Primary key,
			Name VARCHAR(60) NOT NULL,
			Surname VARCHAR(60) NOT NULL,
			Email VARCHAR(60) UNIQUE
			);

		CREATE TABLE IF NOT EXISTS Phone(
			Number INT Primary key,
			Client_id INT NOT NULL REFERENCES ClientData(id)
			);
		""")

		self.conn.commit()
		print('Таблицы ClientData и Phone созданы')

	def delete_db(self):
		self.cur.execute("""
		DROP TABLE Phone;
		DROP TABLE ClientData
			""")
		self.conn.commit()
		print('Все таблицы удалены')

	def add_client(self, name, surname, email):
		self.cur.execute(f"INSERT INTO ClientData (name,surname,email) VALUES ('{name}', '{surname}', '{email}')")
		self.conn.commit()
		print(f'Добавлен клиент {name}')

	def add_number(self, number, client_id):
		self.cur.execute(f"INSERT INTO Phone (Number, Client_id) VALUES ('{number}', {client_id})")
		self.conn.commit()
		self.cur.execute(f"SELECT name FROM ClientData WHERE id = '{client_id}'")
		name = self.cur.fetchone()[0]
		print(f'Номер телефона {number} добавлен клиенту {name}')

	def change_client(self, client_id, **kwargs):
		for column, value in kwargs.items():
			self.cur.execute(f"UPDATE ClientData SET {column} = '{value}' WHERE id = {client_id}")
		self.conn.commit()
		print(f'Данные клиента {client_id} изменены')

	def delete_number(self, number):
		self.cur.execute(f"DELETE FROM Phone WHERE number = {number} RETURNING Client_id")
		client_id = self.cur.fetchone()[0]
		print(f'Телефон {number} клиента {client_id} удален')

	def delete_client(self, client_id):
		self.cur.execute(f"DELETE FROM Phone WHERE client_id = '{client_id}'")
		self.cur.execute(f"DELETE FROM ClientData WHERE id = {client_id}")
		self.conn.commit()
		print(f'Клиент {client_id} удален')

	def find(self, c_data):
		self.cur.execute(f"""
		SELECT * FROM ClientData cd
		JOIN PHONE p on cd.id = p.client_id WHERE 
		LOWER(cd.name) LIKE LOWER('{c_data}') OR
		LOWER(cd.surname) = LOWER('{c_data}') OR
		LOWER(cd.email) = LOWER('{c_data}') OR		
		p.number::VARCHAR = '{c_data}'
		""")
		a = self.cur.fetchall()
		print(a)

if __name__ == '__main__':
	my_clients = ClientDataBase('clients', "postgres", "nicaragua21")
	my_clients.find('56214433')
	# my_clients.delete_client(1)
	# my_clients.delete_number (1111111)
	# my_clients.change_client(1, name="БРАБОРА", surname='ДАРАБОРА', email="dara@yandex.ru")
	# my_clients.add_number(2222222, 1)
	# my_clients.add_client('Петя', 'Дубкин', 'Pet@mail.ru')
	# my_clients.create_db()
	# my_clients.delete_db()

#

# str_params = ",".join([k + " " + v for k, v in iter(params.items())])
# with psycopg2.connect(dbname='clients', user="postgres", password='nicaragua21') as conn:
# 	with conn.cursor() as cur:
# 		cur.execute("""
# 		DROP TABLE ClientData;
# 		""")


	# client_params = {
	# 'id': "SERIAL Primary key",
	# 'Name': "VARCHAR(60) NOT NULL",
	# 'Surname': "VARCHAR(60) NOT NULL",
	# 'Email': "VARCHAR(60) UNIQUE"}
	#
	# phone_params = {
	# 'Number': "INT Primary key",
	# 'Client_id': "INT NOT NULL REFERENCES ClientData(id)"}