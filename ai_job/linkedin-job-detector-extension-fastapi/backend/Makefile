.PHONY: install dev test lint format type-check run clean

# Install production dependencies
install:
	pip install -e .

# Install development dependencies
dev:
	pip install -e ".[dev]"

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

# Run linting
lint:
	flake8 app tests
	black --check app tests
	isort --check-only app tests

# Format code
format:
	black app tests
	isort app tests

# Type checking
type-check:
	mypy app

# Run development server
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

# Help
help:
	@echo "Available commands:"
	@echo "  install     - Install production dependencies"
	@echo "  dev         - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black and isort"
	@echo "  type-check  - Run type checking with mypy"
	@echo "  run         - Run development server"
	@echo "  clean       - Clean up generated files"
	@echo "  help        - Show this help message"