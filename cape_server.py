from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import unquote
from mimetypes import guess_type
from json import load, loads, dumps
from os import path, getenv, walk, makedirs
from requests import get
from re import search, sub
from random import choice
from time import time
from zipfile import ZipFile

if not path.isdir("capes"):
	makedirs("capes")

if not path.isdir("capes/default"):
	makedirs("capes/default")

if not path.isdir("playermodels"):
	makedirs("playermodels")

if not path.isdir("playermodels/items"):
	makedirs("playermodels/items")

if not path.isdir("playermodels/users"):
	makedirs("playermodels/users")

def downloadSettings():
	r = get("https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/settings.json")
	with open("settings.json", "wb") as settingsFile:
		settingsFile.write(r.content)

if not path.isfile("settings.json"):
	downloadSettings()

with open("settings.json") as file:
	file_string = file.read()
	file_string = sub(r"\/\/.*|\/\*[\s\S]*?\*\/", "", file_string)
	file_string = sub(r",(?=[\s\n\r]*[}\]])", "", file_string)
	data = loads(file_string)

if any([not x in data for x in ("minecraftDirectory", "customDefaultDirectory", "notifications", "defaultCapeList", "defaultPlayerModel")]):
	downloadSettings()
	with open("settings.json") as file:
		file_string = file.read()
		file_string = sub(r"\/\/.*|\/\*[\s\S]*?\*\/", "", file_string)
		file_string = sub(r",(?=[\s\n\r]*[}\]])", "", file_string)
		data = loads(file_string)

if data["notifications"].lower() == "true":
	from plyer import notification
	notification.notify(title = "Cape server running", message = "The OptiFine cape server is now running", app_name = "Custom OptiFine Cape Server")

defaultPlayerModelEnabled = False
if data["defaultPlayerModel"].lower() == "on":
	defaultPlayerModelEnabled = True
	if path.isfile("playermodels/users/default.cfg") and path.isfile("playermodels/items/default/model.cfg") and path.isfile("playermodels/items/default/users/default.png"):
		customPlayerModel = True
	else:
		customPlayerModel = False
		defaultCFG = get("https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/playermodels/default/users/default.cfg")
		defaultModel = get("https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/playermodels/default/items/default/model.cfg") 
		defaultTexture = get("https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/playermodels/default/items/default/users/default.png")

defaultCape = []
if "defaultCapeList" in data:
	for cape in data["defaultCapeList"]:
		r = get(f"https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/capes/default/{cape}.png")
		if r.status_code == 200:
			defaultCape.append(r)
if len(defaultCape) == 0:
	defaultCape = None

previousTime = 60
customCapes = []

def getCustomDefaultCape():
	global customCapes, previousTime
	if time() - previousTime < 60:
		return
	previousTime = time()
	customCapes = []
	if path.isfile("settings.json"):
		with open("settings.json") as file:
			file_string = file.read()
			file_string = sub(r"\/\/.*|\/\*[\s\S]*?\*\/", "", file_string)
			file_string = sub(r",(?=[\s\n\r]*[}\]])", "", file_string)
			data = loads(file_string)
		if "customDefaultDirectory" in data:
			try:
				pack = ""
				if data["customDefaultDirectory"].lower() == "resource-pack":
					if "minecraftDirectory" in data and data["minecraftDirectory"] != "default":
						minecraftDirectory = data["minecraftDirectory"]
					else:
						minecraftDirectory = f"{getenv('APPDATA')}/.minecraft"
					optionsDir = path.join(minecraftDirectory, "options.txt")
					if path.isfile(optionsDir):
						with open(optionsDir) as optionsFile:
							pack = loads(search(r"\bresourcePacks:(.*)", optionsFile.read()).group(1))[-1]
							if pack.startswith("file/"):
								customDir = path.join(minecraftDirectory, "resourcepacks", pack[5:], "assets/minecraft/textures/capes")
				else:
					customDir = data["customDefaultDirectory"]
				if ".zip" in customDir:
					zipPartition = customDir.partition(".zip")
					zipPath = zipPartition[0] + zipPartition[1]
					capePath = zipPartition[2][1:]
					zf = ZipFile(zipPath)
					for zipDirectory in zf.namelist():
						if capePath in zipDirectory:
							with zf.open(zipDirectory) as zipCape:
								customCapes.append((zipCape.read(), path.join(zipPath, zipDirectory)))
				elif path.isdir(customDir):
					for subdir, dirs, files in walk(customDir):
						for file in files:
							if not file.endswith(".png"):
								continue
							capePath = path.join(path.join(subdir, file))
							customCapes.append((load_binary(capePath), capePath))
			except:
				pass
	if len(customCapes) == 0:
		if path.isdir("capes/default"):
			for subdir, dirs, files in walk("capes/default"):
				for file in files:
					if not file.endswith(".png"):
						continue
					capePath = path.join(path.join(subdir, file))
					customCapes.append((load_binary(capePath), capePath))

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
			if file_path.startswith("capes"):
				if path.isfile(file_path):
					self._set_response(type=guess_type(file_path)[0])
					binary = load_binary(file_path)
					self.send_header("Content-Length", len(binary))
					self.end_headers()
					self.wfile.write(binary)
				else:
					r = get(f"https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/{file_path}")
					if r.status_code == 200:
						self._set_response(type = r.headers["Content-type"])
						self.send_header("Content-Length", r.headers["Content-Length"])
						self.end_headers()
						self.wfile.write(r.content)
					else:
						r = get(f"http://107.182.233.85/{file_path}")
						if r.status_code == 200:
							self._set_response(type = r.headers["Content-type"])
							self.send_header("Content-Length", r.headers["Content-Length"])
							self.end_headers()
							self.wfile.write(r.content)
						else:
							getCustomDefaultCape()
							if len(customCapes) == 0:
								if defaultCape != None:
									capeTexture = choice(defaultCape)
									self._set_response(type = capeTexture.headers["Content-type"])
									self.send_header("Content-Length", capeTexture.headers["Content-Length"])
									self.end_headers()
									self.wfile.write(capeTexture.content)
							else:
								capeTexture = choice(customCapes)
								self._set_response(type = guess_type(capeTexture[1])[0])
								self.send_header("Content-Length", len(capeTexture[0]))
								self.end_headers()
								self.wfile.write(capeTexture[0])
			else:
				file_path2 = f"playermodels/{file_path}"
				if path.isfile(file_path2):
					self._set_response(type=guess_type(file_path2)[0])
					binary = load_binary(file_path2)
					self.send_header("Content-Length", len(binary))
					self.end_headers()
					self.wfile.write(binary)
				else:
					r = get(f"https://raw.githubusercontent.com/ewanhowell5195/customOptiFineCapeServer/main/playermodels/{file_path}")
					if r.status_code == 200:
						self._set_response(type = r.headers["Content-type"])
						binary = r.content
						self.send_header("Content-Length", len(r.content))
						self.end_headers()
						self.wfile.write(r.content)
					else:
						r = get(f"http://107.182.233.85/{file_path}")
						if r.status_code == 200:
							self._set_response(type = r.headers["Content-type"])
							self.send_header("Content-Length", r.headers["Content-Length"])
							self.end_headers()
							self.wfile.write(r.content)
						else:
							if defaultPlayerModelEnabled == True:
								if customPlayerModel == True:
									if file_path.startswith("users"):
										self._set_response(type = guess_type("playermodels/users/default.cfg")[0])
										binary = load_binary("playermodels/users/default.cfg")
										self.send_header("Content-Length", len(binary))
										self.end_headers()
										self.wfile.write(binary)
									else:
										if file_path.endswith(".cfg"):
											self._set_response(type = guess_type("playermodels/items/default/model.cfg")[0])
											binary = load_binary("playermodels/items/default/model.cfg")
											self.send_header("Content-Length", len(binary))
											self.end_headers()
											self.wfile.write(binary)
										else:
											self._set_response(type = guess_type("playermodels/items/default/users/default.png")[0])
											binary = load_binary("playermodels/items/default/users/default.png")
											self.send_header("Content-Length", len(binary))
											self.end_headers()
											self.wfile.write(binary)
								else:
									if file_path.startswith("users"):
										self._set_response(type = "none")
										binary = defaultCFG.content
										self.send_header("Content-Length", len(binary))
										self.end_headers()
										self.wfile.write(binary)
									else:
										if file_path.endswith(".cfg"):
											self._set_response(type = "none")
											binary = defaultModel.content
											self.send_header("Content-Length", len(binary))
											self.end_headers()
											self.wfile.write(binary)
										else:
											self._set_response(type = defaultTexture.headers["Content-type"])
											self.send_header("Content-Length", defaultTexture.headers["Content-Length"])
											self.end_headers()
											self.wfile.write(defaultTexture.content)
							else:
								self.send_error(404, "Not found")
		except:
			self.send_error(404, "Not found")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def start_server(port):
	server = ThreadedHTTPServer(("", port), ReqHandler)
	print("Cape server online\n")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("Interrupted.")
	server.server_close()
	print("Stopping server...\n")

start_server(80)