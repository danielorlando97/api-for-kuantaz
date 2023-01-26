run_test:
	python -m pytest -v test --tb=short

run_api:
	python -m src

run_api_docker:
	docker-compose -f docker-api.yml up 