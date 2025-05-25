.PHONY: install-frontend install-backend migrate-db seed-data run run-frontend run-backend

# Install Angular dependencies
install-frontend:
	cd frontend && npm install

# Create Python virtual environment and install Flask dependencies
install-backend:
	python -m venv backend/venv
	backend/venv/bin/pip install -r backend/requirements.txt

# Initialize and apply PostgreSQL migrations
migrate-db:
	cd backend && \
	venv/bin/python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"

# Generate test data
seed-data:
	cd backend && venv/bin/python seed_data.py

# Start both frontend and backend servers
run:
	make run-backend & make run-frontend

# Start Angular development server
run-frontend:
	cd frontend && npm run start

# Start Flask server
run-backend:
	cd backend && venv/bin/python main.py

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