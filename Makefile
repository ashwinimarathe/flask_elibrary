setup:
	python3 -m venv flask_project
	. flask_project/bin/activate
    export FLASK_APP=flaskr
    export FLASK_ENV=production
    


install:
	pip install requirements.txt