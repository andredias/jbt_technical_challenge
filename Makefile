run:
	hypercorn --reload --config=hypercorn.toml 'jbt_drone.main:app'


test:
	ENV=testing \
	pytest -x --cov-report term-missing --cov-report html --cov-branch \
	       --cov jbt_drone/


lint:
	@echo
	isort --diff -c .
	@echo
	blue --check --diff --color .
	@echo
	flake8 .
	@echo
	mypy .
	@echo
	bandit -qr jbt_drone/
	@echo
	pip-audit


format:
	isort .
	blue .
	pyupgrade --py310-plus **/*.py


build:
	docker build -t jbt_drone .


install_hooks:
	@ scripts/install_hooks.sh
