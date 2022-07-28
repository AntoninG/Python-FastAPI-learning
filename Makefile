test:
	coverage run -m pytest -vv
	coverage report -m | more
	coverage-badge -f -o coverage-badge.svg

make pylint:
	pylint app | tee pylint.txt
	python -m anybadge -l pylint -v `sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint.txt` -f pylint-badge.svg 2=red 4=orange 8=yellow 10=green
	rm pylint.txt

server:
	uvicorn app.main:app --reload

requirements:
	pip3 install -r requirements.txt