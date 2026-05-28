.PHONY: help install run test lint format clean docker-up docker-down

help:
	@echo "Comandos disponíveis:"
	@echo "  make install      - Instala dependências"
	@echo "  make run          - Roda a aplicação"
	@echo "  make test         - Roda os testes"
	@echo "  make lint         - Verifica código"
	@echo "  make format       - Formata código"
	@echo "  make clean        - Limpa arquivos temporários"
	@echo "  make docker-up    - Sobe containers Docker"
	@echo "  make docker-down  - Para containers Docker"

install:
	pip install -r requirements.txt

run:
	python src/scripts/init_db.py
	uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest src/tests/ -v --cov=src --cov-report=html

lint:
	flake8 src
	mypy src

format:
	black src
	isort src

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down