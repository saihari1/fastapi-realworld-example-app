FROM python:3.9.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 8000

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./

# Install poetry WITHOUT upgrading setuptools globally
RUN pip install "poetry==1.1.0" "poetry-core==1.0.0"

# Configure poetry
RUN poetry config virtualenvs.in-project true

# Install project dependencies
RUN poetry install --no-dev

# Install setuptools INSIDE poetry virtualenv only
RUN /app/.venv/bin/pip install "setuptools<66"

COPY . .

CMD poetry run alembic upgrade head && \
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
