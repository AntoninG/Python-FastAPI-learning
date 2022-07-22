test:
	coverage run -m pytest -vv
	coverage report -m | more
	coverage-badge -f -o coverage-badge.svg

make pylint:
	pylint app

server:
	uvicorn app.main:app --reload

requirements:
	pip3 install -r requirements.txt