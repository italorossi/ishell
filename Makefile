init:
	pip install -r requirements.txt
	pip install -r test_requirements.txt

test:
	pytest --spec tests/test_shell.py