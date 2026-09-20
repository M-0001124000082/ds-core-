import subprocess
import threading
import http.server
import socketserver
import os
import re
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
print(f"Local server started on port {PORT}")

# Now run ssh to localhost.run
cmd = ["ssh", "-R", f"80:localhost:{PORT}", "-o", "StrictHostKeyChecking=no", "nokey@localhost.run"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

for line in proc.stdout:
    sys.stdout.write(line)
    sys.stdout.flush()
    match = re.search(r'(https://[a-zA-Z0-9-]+\.lhr\.life)', line)
    if match:
        url = match.group(1)
        print("\n" + "="*60)
        print(">>> LIVE PUBLIC LINK: " + url)
        print("="*60 + "\n")
        with open(os.path.join(DIRECTORY, "live_url.txt"), "w", encoding="utf-8") as f:
            f.write(url)

proc.wait()
