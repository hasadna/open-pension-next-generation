.PHONY: venv freeze

venv:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

freeze:
	venv/bin/pip freeze > requirements.txt

serve:
	venv/bin/python app.py

