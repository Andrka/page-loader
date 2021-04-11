install:
	poetry install

build:
	poetry build

publish:
	poetry publish --repository testpypi

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest page_loader tests

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/

selfcheck:
	poetry check

check: selfcheck lint test

report:
	poetry run coverage report