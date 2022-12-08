import psycopg2


# Создаем класс подключающийся к указанной базе данных
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
			Number INT8 Primary key,
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
		print(self.cur.fetchall())


if __name__ == '__main__':
	# Ввести свои данные
	with ClientDataBase('xxx', "xxx", "xxx") as my_clients:
		my_clients.create_db()
		my_clients.add_client('Женя', 'Субкин', 'Vet@mail.ru')
		my_clients.add_client('Маша', 'Губкина', 'Mash@mail.ru')
		my_clients.add_client('Паша', 'Пашин', 'Pash@mail.ru')
		my_clients.add_client('Вера', 'Комова', 'Ver@yandex.ru')
		my_clients.change_client(3, name="БРАБОРА", surname='ДАРАБОРА', email="dara@yandex.ru")
		my_clients.add_number(3333333, 2)
		my_clients.add_number(2323462346, 4)
		my_clients.add_number(2345243, 2)
		my_clients.add_number(984325, 1)
		my_clients.add_number(98433325, 2)
		my_clients.add_number(12321535, 3)
		my_clients.add_number(5453246574, 4)
		my_clients.add_number(2222222, 1)
		my_clients.delete_client(2)
		my_clients.delete_number (2323462346)
		my_clients.find('5453246574')



		# my_clients.delete_db()

