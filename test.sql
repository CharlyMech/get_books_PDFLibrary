/*
	This is a test database for login/signin functionallity
*/

-- Create the schema if not exists & Use it
CREATE SCHEMA IF NOT EXISTS testLibrary;
USE testLibrary;

/*
	First of all, create all independent tables
*/

-- Create TIER table if not exists
CREATE TABLE IF NOT EXISTS testLibrary.tiers (
	-- Attributes
	tier_id INT NOT NULL DEFAULT 1,
	name VARCHAR(25),
	-- Constraints
	CONSTRAINT PK_ID_TIERS PRIMARY KEY (tier_id)
);

-- Create USERS table if not exists
CREATE TABLE IF NOT EXISTS testLibrary.users (
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
);


/*
	Now we insert some test data
*/

-- Insert data into testLibrary.tiers
INSERT INTO testLibrary.tiers values (1, "Free");
INSERT INTO testLibrary.tiers values (2, "Pro");
INSERT INTO testLibrary.tiers values (3, "Premium");

-- Insert data into testLibrary.users
INSERT INTO testLibrary.users(user_name, user_surname, mail, passwd, tier_id) values ("Admin", "Admin Admin", "admin@admin.admin", "8C6976E5B5410415BDE908BD4DEE15DFB167A9C873FC4BB8A81F6F2AB448A918", 3);