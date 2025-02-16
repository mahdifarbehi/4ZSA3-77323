.PHONY: all build down test

all:
	@echo "Bringing down Docker containers"
	sudo docker-compose down -v
	@echo "Building and starting containers"
	sudo docker-compose up --build

build:
	@echo "Building Docker containers"
	sudo docker-compose up --build

down:
	@echo "Stopping and removing containers"
	sudo docker-compose down -v

test:
	@echo "Running test_runner"
	sudo docker-compose up --build test_runner
