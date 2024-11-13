FROM python:3.10

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH=/usr/src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
