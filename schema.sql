CREATE TYPE e_user_level AS ENUM
(
  'Admin',
  'User'
);
CREATE TABLE tbl_users
(
	user_id SERIAL PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	user_level e_user_level,
	password VARCHAR(255) NOT NULL
);
CREATE TABLE tbl_requests
(
	request_id SERIAL PRIMARY KEY,
	request_title VARCHAR(255) NOT NULL,
	request_description VARCHAR(255) NOT NULL,
	created_by INTEGER,
	FOREIGN KEY(created_by) REFERENCES tbl_users (user_id)
);
