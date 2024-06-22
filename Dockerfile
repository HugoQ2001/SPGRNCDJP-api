FROM python:3.10.0

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN apt-get update

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]