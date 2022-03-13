init:
	pip install -r requirements.txt

run:
	python -m health.main $(ARGS)

test:
	pytest --cov-report term-missing --cov=health tests/

