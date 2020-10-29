install:
	poetry install

build:
	poetry build

publish:
	poetry publish --repository testpypi

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest --cov=page_loader --cov-report xml tests/

check: lint test

report:
	poetry run coverage report