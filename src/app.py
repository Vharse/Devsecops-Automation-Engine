import os
import sys
import json
import logging

# Configure structured logging for SIEM ingestion
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(message)s")
logger = logging.getLogger("DevSecOpsEngine")

def main():
    payload = {
        "event": "service_healthcheck",
        "status": "UP",
        "environment": os.getenv("APP_ENV", "production"),
        "python_version": sys.version.split()[0]
    }
    logger.info(json.dumps(payload))

if __name__ == "__main__":
    main()
