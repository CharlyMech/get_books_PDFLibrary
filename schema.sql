-- Create the schema if not exists & Use it
CREATE SCHEMA IF NOT EXISTS Library;
USE Library;

/*
	First of all, create all independent tables
*/

-- Create TIER table if not exists
CREATE TABLE IF NOT EXISTS Library.tiers (
	-- Attributes
	tier_id INT NOT NULL DEFAULT 1,
	tier_name VARCHAR(25),
	-- Constraints
	CONSTRAINT PK_ID_TIERS PRIMARY KEY (tier_id)
);

-- Create CATEGORIES table if not exists
CREATE TABLE IF NOT EXISTS Library.categories (
	-- Attributes
	cat_id INT NOT NULL,
	cat_name VARCHAR(25) NOT NULL,
	n_books INT DEFAULT 1,
	-- Constraints
	CONSTRAINT PK_ID_CATEGORIES PRIMARY KEY (cat_id)
);

-- Create AUTHORS table if not exists
CREATE TABLE IF NOT EXISTS Library.authors (
	-- Attributes
	author_id INT NOT NULL AUTO_INCREMENT,
	author_name varchar(100) NOT NULL,
	n_books INT DEFAULT 1,
	-- Constraints
	CONSTRAINT PK_ID_AUTHORS PRIMARY KEY (author_id)
);

/*
	Once independent tables are created, the 1-N relation tables will be created
*/

-- Create USERS table if not exists
CREATE TABLE IF NOT EXISTS Library.users (
	-- Attributes
	user_id INT NOT NULL AUTO_INCREMENT,	
	user_name VARCHAR(50) NOT NULL,
	user_surname VARCHAR(100) NOT NULL,
	mail VARCHAR(150) NOT NULL,
	passwd VARCHAR(256) NOT NULL,
	tier_id INT NOT NULL,
	-- Constraints
	CONSTRAINT PK_ID_USERS PRIMARY KEY (user_id),
	CONSTRAINT UQ_MAIL_USERS UNIQUE (mail),
	CONSTRAINT FK_ID_TIERS FOREIGN KEY (tier_id) REFERENCES Library.tiers(tier_id)
		ON UPDATE CASCADE 
	-- No need constraints for tiers
);

-- Create BOOKS table if not exists
CREATE TABLE IF NOT EXISTS Library.books (
	-- Attributes
	book_id INT NOT NULL,
	title VARCHAR(150) NOT NULL,
	author_id INT DEFAULT 0,
	publisher VARCHAR(75),
	pub_year INT NOT NULL,
	lang VARCHAR(20) NOT NULL,
	book_description LONGTEXT NOT NULL,
	pages INT NOT NULL,
	cover VARCHAR(255) NOT NULL,
	thumbnail VARCHAR(255) NOT NULL,
	pdf VARCHAR(255) NOT NULL,
	tier_id INT NOT NULL,
	-- Constraints
	CONSTRAINT PK_ID_BOOKS PRIMARY KEY (book_id),
	CONSTRAINT FK_ID_AUTHORS FOREIGN KEY (author_id) REFERENCES Library.authors(author_id)
		ON DELETE SET DEFAULT ON UPDATE CASCADE,
	CONSTRAINT FK_ID_TIERS FOREIGN KEY (tier_id) REFERENCES Library.tiers(tier_id)
	-- No need constraints for Tiers
);

/*
	Last but not least, the N-N relation tables
*/

-- Create BOOKSCAT table if not exists
CREATE TABLE IF NOT EXISTS Library.bookscats (
	-- Attributes
	bookcat_id INT NOT NULL AUTO_INCREMENT,
	book_id INT NOT NULL,
	cat_id INT NOT NULL,
	-- Constraints
	CONSTRAINT PK_ID_BOOKCATS PRIMARY KEY (bookcat_id),
	CONSTRAINT FK_ID_BOOKS FOREIGN KEY (book_id) REFERENCES Library.books(book_id)
		ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_ID_CATEGORIES FOREIGN KEY (cat_id) REFERENCES Library.categories(cat_id)
		ON DELETE SET DEFAULT ON UPDATE CASCADE
);

-- Create USERSBOOKS if not exists
CREATE TABLE IF NOT EXISTS Library.usersbooks (
	-- Attributes
	user_id INT NOT NULL,
	book_id INT NOT NULL,
	added BOOLEAN DEFAULT FALSE,
	readed BOOLEAN DEFAULT FALSE,
	-- Constraints
	CONSTRAINT PK_ID_USERSBOOKS PRIMARY KEY (user_id, book_id), -- Composed PK
	CONSTRAINT FK_ID_USERS FOREIGN KEY (user_id) REFERENCES Library.users(user_id)
		ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_ID_BOOKS FOREIGN KEY (book_id) REFERENCES Library.books(book_id)
		ON DELETE CASCADE ON UPDATE CASCADE
);



/*
	There is some data that needs to be inserted manually instead of extracted from 
	OpenLibra's API. 
	Insert data for Tiers and admin user (default one)
*/

-- Insert data into Library.tiers
INSERT INTO Library.tiers VALUES (1, "Free");
INSERT INTO Library.tiers VALUES (2, "Pro");
INSERT INTO Library.tiers VALUES (3, "Premium");

-- Insert data into Library.users
INSERT INTO Library.users(user_name, user_surname, mail, passwd, tier_id) VALUES ("Admin", "Admin Admin", "admin@admin.admin", "8C6976E5B5410415BDE908BD4DEE15DFB167A9C873FC4BB8A81F6F2AB448A918", 3);

-- Insert DEFAULT author into Library.authors
INSERT INTO Library.authors (author_id, author_name, n_books) VALUES (0, 'no-author', 0);

-- Insert DEFAULT category into Library.categories
INSERT INTO Library.categories (cat_id, cat_name, n_books) VALUES (0, 'no-category', 0);