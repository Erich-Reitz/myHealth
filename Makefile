init:
	pip install -r requirements.txt

run:
	python3 -m health.main $(ARGS)

format:
	black health/

lint:
	pylint health/

test:
	python3 -m pytest --cov-report term-missing -s --cov=health tests/

