.PHONY: install-frontend install-backend migrate-db seed-data run run-frontend run-backend clean check-env build-frontend setup-env all

# Install Angular dependencies
install-frontend:
	cd ./frontend && npm install

# Create Python virtual environment and install Flask dependencies
install-backend:
	python -m venv ./backend/venv
	./backend/venv/bin/pip install -r ./backend/requirements.txt

# Initialize and apply PostgreSQL migrations
migrate-db:
	cd ./backend && \
	venv/bin/python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"

# Generate test data
seed-data:
	cd ./backend && venv/bin/python seed_data.py

# Start both frontend and backend servers
run:
	make run-backend & make run-frontend

# Start Angular development server
run-frontend:
	cd ./frontend && npm run start

# Start Flask server
run-backend:
	cd backend && venv/bin/python main.py

# Clean up generated files
clean:
	rm -rf ./frontend/dist
	rm -rf ./frontend/node_modules
	rm -rf ./backend/venv
	rm -rf ./backend/__pycache__
	rm -rf ./backend/app/__pycache__

# Check environment
check-env:
	@echo "Checking PostgreSQL..."
	@command -v psql >/dev/null 2>&1 || { echo >&2 "PostgreSQL client not found. Please install PostgreSQL."; exit 1; }
	@echo "PostgreSQL client found."
	@echo "Checking Node.js..."
	@command -v node >/dev/null 2>&1 || { echo >&2 "Node.js not found. Please install Node.js."; exit 1; }
	@echo "Node.js found: $$(node --version)"
	@echo "Checking Python..."
	@command -v python >/dev/null 2>&1 || { echo >&2 "Python not found. Please install Python 3.8+."; exit 1; }
	@echo "Python found: $$(python --version)"

# Build frontend for production
build-frontend:
	cd ./frontend && npm run build

# Setup environment variables
setup-env:
	@echo "Creating .env file in backend directory..."
	@echo "DB_USER=postgres" > backend/.env
	@echo "DB_PASSWORD=postgres" >> backend/.env
	@echo "DB_HOST=localhost" >> backend/.env
	@echo "DB_PORT=5432" >> backend/.env
	@echo "DB_NAME=esc_db" >> backend/.env
	@echo "JWT_SECRET_KEY=dev-secret-key-change-in-production" >> backend/.env
	@echo "SECRET_KEY=dev-secret-key-change-in-production" >> backend/.env
	@echo "DEBUG=True" >> backend/.env
	@echo ".env file created. Please update with your actual database credentials."

# Complete setup and run
all: check-env install-frontend install-backend setup-env migrate-db seed-data run

# Help command
help:
	@echo "Available commands:"
	@echo "  make install-frontend  - Install Angular dependencies"
	@echo "  make install-backend   - Create Python virtual environment and install Flask dependencies"
	@echo "  make migrate-db        - Initialize and apply PostgreSQL migrations"
	@echo "  make seed-data         - Generate test data"
	@echo "  make run               - Start both frontend and backend servers"
	@echo "  make run-frontend      - Start Angular development server"
	@echo "  make run-backend       - Start Flask server"
	@echo "  make clean             - Clean up generated files"
	@echo "  make check-env         - Check if required software is installed"
	@echo "  make build-frontend    - Build frontend for production"
	@echo "  make setup-env         - Create .env file with default environment variables"
	@echo "  make all               - Complete setup and run (check env, install, setup env, migrate, seed, run)"