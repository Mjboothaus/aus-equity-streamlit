run: 
    streamlit run app.py --server.port=8080 --server.address=localhost && ps -ef | grep streamlit | grep -v grep


run-container: 
    docker build . -t $APP_NAME
    docker run -p 8080:8080 $APP_NAME

gcloud-deploy: 
    cloud app deploy app.yaml

venv-reqs:
	python3 -m pip install --upgrade pip
	python3 -m venv .venv
	. .venv/bin/activate
	pip-compile requirements.in
	pip install -r requirements.txt 