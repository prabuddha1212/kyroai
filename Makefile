.PHONY: help dev test test-backend test-frontend build lint clean

help:
	@echo "Available commands:"
	@echo "  make dev            - Run both backend and frontend via docker-compose"
	@echo "  make test           - Run backend and frontend tests"
	@echo "  make test-backend   - Run backend tests with pytest"
	@echo "  make test-frontend  - Run frontend type-check"
	@echo "  make build          - Build production images"
	@echo "  make clean          - Remove temporary build artifacts"

dev:
	docker-compose up --build

test: test-backend test-frontend

test-backend:
	cd backend && python -m pytest tests/ -v

test-frontend:
	cd frontend && npm run build

build:
	docker-compose build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".next" -exec rm -rf {} +
