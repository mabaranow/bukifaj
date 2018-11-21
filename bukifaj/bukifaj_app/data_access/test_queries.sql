SELECT * FROM pg_catalog.pg_tables;


select * from pg_catalog.pg_tablespace;

SELECT table_schema, table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public';


commit;

drop table publisher cascade;