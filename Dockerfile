FROM python:3.9.12

# remember to expose the port your app'll be exposed on.
EXPOSE 8080

RUN pip install -U pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy into a directory of its own (so it isn't in the toplevel dir)
RUN mkdir -p /app
COPY app.py app/app.py
COPY src app/src
WORKDIR /app

# run it!
ENTRYPOINT ["streamlit", "run", "src/app_main.py", "--server.port=8080", "--server.address=0.0.0.0"]