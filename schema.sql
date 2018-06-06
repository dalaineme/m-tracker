CREATE TABLE
IF NOT EXISTS test
(id serial PRIMARY KEY, num integer, data varchar);
INSERT INTO test
  (num,data)
values(10, 'Hello word');