lint:
	poetry run task flake8
	poetry run task black
	poetry run task isort

test:
	poetry run task test
