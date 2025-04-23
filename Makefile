.PHONY: api scan run

api:
	python3 app/api.py

run:
	@echo "Starting API in background..."
	python3 app/api.py & sleep 2

check-python:
	@python3 --version

help:
	@echo "make api           # Run API in foreground"
	@echo "make run           # Run API in background"
	@echo "make check-python  # Check Python version"


