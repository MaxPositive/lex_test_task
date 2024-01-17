FROM python:3.11.7-alpine3.19

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt /temp/
WORKDIR /app
RUN pip install -r /temp/requirements.txt

COPY src /app/src/
COPY tests /app/tests

EXPOSE 8000

