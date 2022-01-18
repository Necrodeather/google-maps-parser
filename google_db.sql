CREATE DATABASE IF NOT EXISTS Test;
USE Test;
CREATE TABLE IF NOT EXISTS main
(
	id INT NOT NULL AUTO_INCREMENT,
    S_Name varchar(30),
    Category varchar(30),
	Reviews varchar(15),
    Rating varchar(3),
    Services text,
    Address text,
	Location text,
    Work_time text,
    Find_a_table boolean,
	Menu text,
    Website text,
    Phone text,	
	Plus_code text,
	primary key(id)
);
CREATE TABLE IF NOT EXISTS photo(
	id integer,
	fk_Photo integer,
	S_Name varchar(30),
	Photo text,
	primary key(id),
);
CREATE TABLE IF NOT EXISTS reviews(
    id integer,	
	fk_Reviews integer, 	
	S_Name varchar(30),
	Author_name varchar(30),	
	Avatar_Author text,
	Rating varchar(3),	
	Full_Text text,
    primary key(id)
)
    