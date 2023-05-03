# Importing mysql.connector for MySQL Server connection
import mysql.connector

class MySQL:
	# Constructor
	def __init__(self, host, schema='Library'):
		self.__host = host
		self.__schema = schema

		# Create connector
		self.__conn = mysql.connector.connect(
  			host= self.__host, # VM IP -> This will be changed to server's IP
  			user= "library",
  			password= "library",
			database= self.__schema
		)
		# Create cursor
		self.__cur = self.__conn.cursor()

	# STR (toString)
	def __str__(self):
		return f"HOST:{self.__host}\nSCHEMA:{self.__schema}"

	
	# TEST METHOD
	def test(self) -> list: # Users
		self.__cur.execute("SELECT * FROM tiers WHERE name='Free'")
		return self.__cur.fetchall()
	
	'''
		CRUD METHODS NEEDED FOR DATA INSERTION
		These methods are designed for all possible cases that might happent while data is being inserted
		So not all CRUD possibilities will be coded for all tables
	'''
	
	# SELECT * FROM [table] WHERE ...
	def select_author_by_id(self, author_id): # Author by ID
		self.__cur.execute(f"SELECT * FROM authors WHERE author_id={author_id}")
		return self.__cur.fetchall()
	
	def select_category_by_id(self, cat_id): # Category by ID
		self.__cur.execute(f"SELECT * FROM categories WHERE cat_id={cat_id}")
		return self.__cur.fetchall()

	def select_author_by_name(self, author_name): # Author by NAME
		# Remember that OpenLibra does not store separately the Authors seems (at least there is no option in the API)
		# So the relation between BOOKS-AUTHORS in N-1
		sql = "SELECT * FROM authors WHERE author_name=%s"
		val = [author_name]
		self.__cur.execute(sql, val)
		return self.__cur.fetchall()
	
	def select_count_authors(self): # Count authors -> For new author ID
		self.__cur.execute("SELECT COUNT(author_id) FROM authors")
		return self.__cur.fetchall() # RETURN : [(N,)]
	
	def select_book_by_id(self, book_id): # Book by ID
		self.__cur.execute(f"SELECT * FROM books WHERE book_id={book_id}")
		return self.__cur.fetchall()

	def select_author_n_books(self, author_id): # Number of books from author ID
		self.__cur.execute(f"SELECT n_books FROM authors WHERE author_id={author_id}")
		return self.__cur.fetchall()
	
	def select_cat_n_books(self, cat_id): # Number of books from category ID
		self.__cur.execute(f"SELECT n_books FROM categories WHERE cat_id={cat_id}")
		return self.__cur.fetchall()

	# INSERT INTO ...
	def insert_book(self, book_id, title, author_id, publisher, pub_year, lang, book_description, pages, cover, thumbnail, pdf, tier_id): # Insert new book
		sql = "INSERT INTO books (book_id, title, author_id, publisher, pub_year, lang, book_description, pages, cover, thumbnail, pdf, tier_id) \
			    				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		val = (book_id, title, author_id, publisher, pub_year, lang, book_description, pages, cover, thumbnail, pdf, tier_id)
		self.__cur.execute(sql, val)

		self.__conn.commit()

	def insert_author(self, author_name): # Insert new author
		sql = "INSERT INTO authors (author_name) VALUES (%s)"
		val = [author_name]
		self.__cur.execute(sql, val)

		self.__conn.commit()
	
	def insert_category(self, cat_id, cat_name): # Insert new category
		sql = "INSERT INTO categories (cat_id, cat_name) VALUES (%s, %s)"
		val = (cat_id, cat_name)
		self.__cur.execute(sql, val)

		self.__conn.commit()

	def insert_book_category(self, book_id, cat_id):
		sql = "INSERT INTO bookscats (book_id, cat_id) VALUES (%s, %s)"
		val = (book_id, cat_id)
		self.__cur.execute(sql, val)

		self.__conn.commit()
	
	# UPDATE ...
	def update_authors_n_books(self, author_id): # Update auhtor's total books
		sql = "UPDATE authors SET n_books=%s WHERE author_id=%s"
		new = self.select_author_n_books(author_id)[0][0] + 1
		self.__cur.execute(sql,(new, author_id))

		self.__conn.commit()
	
	def update_cat_n_books(self, cat_id): # Update category's total books
		sql = "UPDATE categories SET n_books=%s WHERE cat_id=%s"
		new = self.select_cat_n_books(cat_id)[0][0] + 1
		self.__cur.execute(sql,(new, cat_id))

		self.__conn.commit()
		

	# CLOSE CONNECTION -> Once the main script has ended executing all needed operations, this method will be called to end the connection
	def close_connection(self):
		self.__conn.close()