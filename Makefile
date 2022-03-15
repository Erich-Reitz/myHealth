init:
	pip install -r requirements.txt

run:
	python -m health.main $(ARGS)

format:
	black health/

lint:
	pylint health/

test:
	pytest --cov-report term-missing -s --cov=health tests/

