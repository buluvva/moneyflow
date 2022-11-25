cur.execute("DROP TABLE  test")
cur.execute("CREATE TABLE IF NOT EXISTS test(id serial PRIMARY KEY, text VARCHAR, test_value real)")
cur.execute("INSERT INTO test(text,test_value) VALUES ('тестовая строка',123458.9)")
conn.commit()