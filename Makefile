test:
	coverage run -m pytest -vv

coverage:
	coverage report -m | more

server:
	uvicorn app.main:app --reload

requirements:
	pip3 install -r requirements.txt