
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

TOKEN = os.environ.get("REPORT_RECEIVER_TOKEN")
OUTPUT_FILE = Path(__file__).resolve().parent / "testreport.json"


class ReportReceiver(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/report":
            self.send_error(404, "Endpoint not found")
            return

        if not TOKEN or self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self.send_error(401, "Unauthorized")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            report = json.loads(self.rfile.read(length).decode("utf-8"))

            if not isinstance(report, dict):
                raise ValueError("Report must be a JSON object")

            OUTPUT_FILE.write_text(
                json.dumps(report, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"message":"Report saved successfully"}')

            print(f"Report saved to: {OUTPUT_FILE}")

        except (ValueError, json.JSONDecodeError) as error:
            self.send_error(400, str(error))

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set REPORT_RECEIVER_TOKEN before starting the receiver.")

    server = HTTPServer(("127.0.0.1", 8765), ReportReceiver)
    print("Local report receiver running at http://127.0.0.1:8765")
    print("Keep this window open.")
    server.serve_forever()
