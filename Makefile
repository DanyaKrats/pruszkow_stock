run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

env:
	source .venv/bin/activate

alembic_generate:
	alembic revision --autogenerate -m "defoult"

heads:
	alembic upgrade heads

purge:
	docker-compose exec -T postgres psql -U postgres -d pruszkow_stock -c "TRUNCATE TABLE alembic_version;"
	docker-compose exec -T postgres psql -U postgres -d pruszkow_stock -c "DO \$$\$$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != 'alembic_version') LOOP EXECUTE 'DROP TABLE IF EXISTS public.' || r.tablename || ' CASCADE'; END LOOP; END \$$\$$;"
