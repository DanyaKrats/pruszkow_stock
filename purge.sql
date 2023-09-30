-- Очистить таблицу alembic_version
TRUNCATE TABLE alembic_version;

-- Удалить все таблицы, кроме alembic_version
DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != 'alembic_version') LOOP EXECUTE 'DROP TABLE IF EXISTS public.' || r.tablename || ' CASCADE'; END LOOP; END $$;
