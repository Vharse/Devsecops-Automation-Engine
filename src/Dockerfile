FROM cgr.dev/chainguard/python:latest-dev@sha256:d8a571f7fb82f7aa4ebf32b7bb577a76be2d6ca0db9bfa81d5823dd7dd2e4242 AS builder

WORKDIR /app

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir --require-hashes --only-binary :all: -r requirements.txt

FROM cgr.dev/chainguard/python:latest@sha256:4b49bb3c1ae29e34e5a9538c645d949ec3058866a9876bd6cae936ffb28bf9a8

WORKDIR /app

COPY --from=builder /app/venv /app/venv
COPY main.py .

ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER nonroot

ENTRYPOINT ["python", "main.py"]