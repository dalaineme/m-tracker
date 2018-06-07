CREATE TYPE e_user_level AS ENUM (
  'Admin',
  'User'
);

CREATE TABLE tbl_users (
	user_id INTEGER NOT NULL,
	first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  user_level e_user_level,
  password VARCHAR(255) NOT NULL,
	PRIMARY KEY (user_id)
);

CREATE TABLE tbl_requests (
	request_id INTEGER NOT NULL,
	request_title VARCHAR(255) NOT NULL,
  request_description VARCHAR(255) NOT NULL,
	created_by INTEGER,
	PRIMARY KEY (request_id),
	FOREIGN KEY(created_by) REFERENCES tbl_users (user_id)
);

INSERT INTO tbl_users(user_id, first_name, last_name, email, user_level, password) values(1, 'Dalin', 'Oluoch', 'mcdalinoluoch@gmail.com', 'Admin', 'password');

INSERT INTO tbl_users(user_id, first_name, last_name, email, user_level, password) values(2, 'Another', 'Oluoch', 'mcdalinoluoch@gmail.com', 'Admin', 'password');
