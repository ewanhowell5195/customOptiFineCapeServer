from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import unquote
from mimetypes import guess_type
from requests import get
from sys import argv
from os import path

if len(argv) == 1 or argv[1] != "-silent":
	from plyer import notification
	notification.notify(title = "Cape server running", message = "The OptiFine cape server is now running", app_name = "Here is the application name")

defaultCape = get(f"https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/default/default.png")

def load_binary(file_path):
	with open(file_path, "rb") as f:
		return f.read()

class ReqHandler(BaseHTTPRequestHandler):
	def _set_response(self, status=200, type="text/html"):
		self.send_response(status)
		self.send_header("Content-type", type)
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")

	def do_GET(self):
		decoded_path = unquote(self.path)
		file_path = decoded_path[1:]
		try:
			if path.isfile(file_path):
				self._set_response(type=guess_type(file_path)[0])
				binary = load_binary(file_path)
				self.send_header("Content-Length", len(binary))
				self.end_headers()
				self.wfile.write(binary)
			else:
				r = get(f"https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/{file_path}")
				if r.status_code == 200:
					self._set_response(type=r.headers["Content-type"])
					self.send_header("Content-Length", r.headers["Content-Length"])
					self.end_headers()
					self.wfile.write(r.content)
				else:
					r = get(f"http://107.182.233.85/{file_path}")
					if r.status_code == 200:
						self._set_response(type=r.headers["Content-type"])
						self.send_header("Content-Length", r.headers["Content-Length"])
						self.end_headers()
						self.wfile.write(r.content)
					else:
						self._set_response(type=defaultCape.headers["Content-type"])
						self.send_header("Content-Length", defaultCape.headers["Content-Length"])
						self.end_headers()
						self.wfile.write(defaultCape.content)
		except:
			self.send_error(404, "Not found")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def start_server(port):
	server = ThreadedHTTPServer(("", port), ReqHandler)
	print("Starting cape server...\n")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("Interrupted.")
	server.server_close()
	print("Stopping server...\n")

start_server(80)