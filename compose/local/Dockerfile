ARG PYTHON_VERSION=3.12-slim-bullseye
ARG APP_HOME=/app

FROM python:${PYTHON_VERSION} as python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}
COPY . ${APP_HOME}
RUN pip install -r ${APP_HOME}/requirements/local.txt

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
