FROM python:3.14-slim

ENV FLASK_APP=manage.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY requirements.txt ./
RUN python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser manage.py unicorn.py ./
COPY --chown=appuser:appuser app app
COPY --chown=appuser:appuser migrations migrations

USER appuser

EXPOSE 5000
CMD ["uvicorn", "unicorn:app", "--host", "0.0.0.0", "--port", "5000"]
