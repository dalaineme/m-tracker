CREATE TYPE e_user_level AS ENUM
(
  'Admin',
  'User'
);
CREATE TYPE e_request_status AS ENUM
(
  'Sent',
  'Approved',
  'Dissaproved',
  'Resolved'
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
  current_status e_request_status DEFAULT 'Sent',
	created_by INTEGER,
	FOREIGN KEY(created_by) REFERENCES tbl_users (user_id)
);
CREATE TABLE tbl_status_logs
(
  status_id SERIAL PRIMARY KEY,
  request_status VARCHAR(50) NOT NULL,
  date_updated timestamp without time zone default current_timestamp,
  request INTEGER,
  FOREIGN KEY(request) REFERENCES tbl_requests (request_id)
)
