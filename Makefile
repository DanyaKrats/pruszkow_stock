run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

env:
	source .venv/bin/activate

alembic_generate:
	alembic revision --autogenerate -m "defoult"

heads:
	alembic upgrade heads