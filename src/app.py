import os
import sys
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configure structured logging for SIEM ingestion
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(message)s")
logger = logging.getLogger("DevSecOpsEngine")

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {
            "event": "service_healthcheck",
            "status": "UP",
            "environment": os.getenv("APP_ENV", "production"),
            "python_version": sys.version.split()[0]
        }
        
        # Log event for SIEM telemetry
        logger.info(json.dumps(payload))
        
        # Respond to healthcheck and ZAP requests
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress standard HTTP request noise in favor of structured logging
        pass

def main():
    port = int(os.getenv("PORT", 8080))
    server_address = ("0.0.0.0", port)
    
    # TLS is terminated at the proxy/ingress layer in staging and production environments.
    httpd = HTTPServer(server_address, HealthCheckHandler)  # nosonar
    logger.info(json.dumps({"event": "server_start", "port": port}))
    
    try:
        httpd.serve_forever() # nosonar
    except KeyboardInterrupt:
        httpd.server_close()

if __name__ == "__main__":
    main()
