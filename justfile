# Docs: https://just.systems/man/en/

project_name := "aus-equity-streamlit"
#app_py := "app.py"
app_py := "src/app_main.py"
server_port := "8080"

set dotenv-load

# show available commands
help:
  @just -l

# create the local Python venv (.venv) and install requirements(.txt)
setup-python-venv:
	python3 -m pip install --upgrade pip
	python3 -m venv .venv
	. .venv/bin/activate
	pip-compile requirements.in
	pip install -r requirements.txt


# run app.py (in Streamlit) locally
run: 
    streamlit run {{app_py}} --server.port={{server_port}} --server.address=localhost


# check what instances of streamlit are running
ps-streamlit:
    ps -ef | grep streamlit | grep -v grep | grep -v just


# build and run app.py in a (local) docker container
run-container: 
    docker build . -t {{project_name}}
    docker run -p {{server_port}}:{{server_port}} {{project_name}}


# deploy container (including app.py) to Google Cloud (App Engine)
gcloud-deploy:
    # gcloud projects delete {{project_name}}
    gcloud projects create {{project_name}}
    gcloud config set project {{project_name}}
    gcloud beta billing projects link {{project_name}} --billing-account $BILLING_ACCOUNT_GCP

# gloud init - other stuff?
# gcloud app deploy app.yaml   (need to do region / )

gcloud-view:
    gcloud app browse


gcloud-app-disable:   # deleting project does not delete app
    gcloud app versions list
# gcloud app versions stop {{VERSION.ID}}

# TODO: Need to move billing account as a secret / .env

# gcloud projects list

# Creating App Engine application in project [aus-equity-streamlit] and region [australia-southeast1]....done.                                                                                                                                                                                         
# Services to deploy:

# descriptor:                  [/Users/mjboothaus/code/github/mjboothaus/aus-equity-streamlit/aus-equity-streamlit/app.yaml]
# source:                      [/Users/mjboothaus/code/github/mjboothaus/aus-equity-streamlit/aus-equity-streamlit]
# target project:              [aus-equity-streamlit]
# target service:              [default]
# target version:              [20220714t180032]
# target url:                  [https://aus-equity-streamlit.ts.r.appspot.com]
# target service account:      [App Engine default service account]