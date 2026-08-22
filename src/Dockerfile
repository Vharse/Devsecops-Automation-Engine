# Stage 1: Build stage pinning a specific version (Fixes S6596)
FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Distroless runtime pinning a specific version (Fixes S6596)
FROM cgr.dev/chainguard/python:latest-dev AS runtime

WORKDIR /app

# Standard COPY leaves files owned by root, making them read-only to the app user (Fixes S6504)
COPY --from=builder /app/venv /app/venv
COPY main.py .

ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Run the application as the unprivileged user
USER nonroot

ENTRYPOINT ["python", "main.py"]