FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY classes classes
COPY data data
COPY templates templates
COPY app.py .
COPY wsgi.py .

CMD flask run -h 0.0.0.0 -p 5000