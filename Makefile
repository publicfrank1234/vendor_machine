.PHONY: setup test clean

setup: ## Setup the virtual environment and install dependencies
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

test: ## Run tests with pytest
	. venv/bin/activate; PYTHONPATH=$(PWD) pytest  -vv -s

clean: ## Clean up pyc files and __pycache__ directories
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

format: ## Format style with black
	. venv/bin/activate; black . --exclude='/venv/'

lint: ## Check style with flake8
	. venv/bin/activate; flake8 . --exclude=venv

docker-build: ## Build Docker container
	docker build -t vendor_machine_xyz .

docker-run: ## Run Docker container
	docker run --rm -p 8000:8000 vendor_machine_xyz

docker-test: ## Run tests inside Docker container
	docker run --rm vendor_machine_xyz pytest -vv -s

run-local: ## Run the application locally
	. venv/bin/activate; python app/main.py

.PHONY: help 
help: ## Help message
	@echo "List of valid make commands:"
	@awk 'BEGIN {FS = ": .*##"; printf "\033[36m\033[0m"} /^[$$()% 0-9a-zA-Z_-]+(\\:[$$()% 0-9a-zA-Z_-]+)*:.*?##/ { gsub(/\\:/,":", $$1); printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) | sort