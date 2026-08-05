FROM python:3.14

ENV FLASK_APP=manage.py
WORKDIR /app

COPY manage.py unicorn.py requirements.txt ./
COPY app app
COPY migrations migrations

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["uvicorn", "unicorn:app", "--host", "0.0.0.0", "--port", "5000"]
