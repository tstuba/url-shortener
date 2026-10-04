help:
	@echo "Available commands:"
	@echo "  build                      - Build the Docker container"
	@echo "  build-no-cache             - Build the Docker container without cache"
	@echo "  start                      - Start the Docker containers"
	@echo "  start-detached             - Start the Docker containers in detached mode"
	@echo "  stop-app                   - Stop the App container"
	@echo "  start-dev-app              - Start the database, and App in development mode"
	@echo "  stop                       - Stop the Docker containers"
	@echo "  help                       - Show this help message"
	@echo "  migration                  - Create a new Alembic migration with a message (message=\"Your message\")"
	@echo "  migrate                    - Run Alembic migrations in the App container"
	@echo "  downgrade                  - Downgrade to a specific Alembic migration (revision=\"specific revision\" or revision=\"head-1\" to downgrade one step or more)"
	@echo "  mypy                       - Run mypy checks"
	@echo "  lint                       - Run ruff checks"
	@echo "  format                     - Format with ruff"


build:
	@echo "Building Docker container..."
	docker compose build

build-no-cache:
	@echo "Building Docker container without cache..."
	docker compose build --no-cache

start:
	@echo "Starting Docker container..."
	docker compose up

start-detached:
	@echo "Starting Docker container..."
	docker compose up -d

stop-backend:
	@echo "Stopping App container..."
	docker compose stop app

start-dev-backend:
	@echo "Starting Database..."
	docker compose up -d db
	@echo "Running App in development mode..."
	docker compose run --rm --service-ports app uvicorn src.url_shortener.main:app --host 0.0.0.0 --port 8000 --reload

stop:
	@echo "Stopping Docker containers..."
	docker compose stop

migration:
	@echo "Creating new migration..."
	docker compose exec app alembic revision --autogenerate -m "$(message)"
	@echo "Migration created successfully."

migrate:
	@echo "Running Alembic migrations..."
	docker compose exec app alembic upgrade head

downgrade:
	@echo "Running Alembic downgrade..."
	docker compose exec app alembic downgrade $(revision)
	@echo "Downgrade completed."

mypy:
	@echo "Running mypy checks..."
	mypy
	@echo "Mypy check completed."

lint:
	@echo "Running ruff checks..."
	ruff check src/
	@echo "Ruff check completed."

format:
	@echo "Formatting with ruff..."
	ruff format src/
	@echo "Formatting with ruff completed."