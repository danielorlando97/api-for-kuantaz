run_test:
	python -m pytest -v test --tb=short

run_api:
	python -m src

run_api_docker: down_all
	docker-compose -f docker-api.yml up 

run_test_docker: down_all
	docker-compose -f docker-test.yml up

build_db: down_all
	docker-compose -f docker-db.yml up -d 

run_full_stack: down_all
	docker-compose -f docker-test.yml up 
	docker-compose -f docker-test.yml down 
	docker-compose -f docker-api.yml up 

down_all:
	docker-compose -f docker-api.yml down 
	docker-compose -f docker-test.yml down 
	docker-compose -f docker-db.yml down