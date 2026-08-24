FROM cgr.dev/chainguard/python:3.13.2 AS builder

WORKDIR /app

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

FROM cgr.dev/chainguard/python:lastest

WORKDIR /app

COPY --from=builder /app/venv /app/venv
COPY main.py .

ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER nonroot

ENTRYPOINT ["python", "main.py"]