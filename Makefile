init:
	pip install -r requirements.txt

run:
	python -m health.main $(ARGS)

test:
	nosetests tests
