import httpclass
import json
import platform
import hashlib

VERSION=platform.python_version()


class api(httpclass.httpmessage):
    def __init__(self):
        super().__init__()
        
    def Do_Head(self):
        if self.path == "/":
            self.send_code(200)
            self.send_header("Server", "Mtcraft_http_server")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
        else:
            try:
                self.send_code(200)
                self.send_header("Server", "Mtcraft_http_server")
                self.send_header(
                    "content-type", httpclass.httpmimes[self.path.split(".")[1]]
                )
                with open(f".{self.path}","rb") as html:
                    html = html.read()

                self.send_header("content-Lenght", str(len(html )))
                self.end_header()
            except IndexError:
                self.send_code(400)
                self.send_header("Archivo", "No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
                self.send_header("Archivo", "No encontrado")
                self.end_header()
    def Do_get(self):
        if self.path == "/":
            self.send_code(200)
            self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
            with open("hola.html", "r") as body:
                html = body.read()
            self.send_body(html)
        else:
            try:
                self.send_code(200)
                self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
                self.send_header(
                    "content-type", httpclass.httpmimes[self.path.split(".")[1]]
                )
                with open(f".{self.path}", "rb") as body:
                    html = body.read()
                self.send_header("content-Lenght", str(len(html)))
                self.end_header()
                if (
                    httpclass.httpmimes[self.path.split(".")[1]].split("/")[0]
                    in "audiovideoimage"
                ):
                    self.send_body(html, True)
                else:
                    self.send_body(html.decode())
            except IndexError:
                self.send_code(400)
                self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
                self.send_header("Archivo", "No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
                self.send_header("Archivo", "No encontrado")
                self.end_header()
    def Do_post(self):
        try:
            valores = self._message.splitlines()[-1]
            for i in valores.split("&"):
                self.Post[i.split("=")[0]] = i.split("=")[1]
        except  IndexError:
            self.Post={}
        if self.path == "/usuarios":
            
            self.send_code(201)
            self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
            self.send_header("Location", f"http://localhost:{httpclass.port}/registrado.html")
            self.end_header()
            with open("inscritos.json", "r+") as DB:
                try:
                    lista = json.loads(DB.read())
                except json.decoder.JSONDecodeError:
                    lista = {"inscritos": []}
                
                self.Post["contra"] = hashlib.sha512(str(self.Post["contra"]).encode("utf-8")).hexdigest()
                lista["inscritos"].append(self.Post)
                DB.seek(0,0)
                DB.write(json.dumps(lista, indent=4))
                DB.write("\n")
        elif self.path == "/logout":
            self.send_code(200)
            self.send_header("Set-cookie","session-id=deleted;Expires=Thu, 01 Jan 1970 00:00:00 GMT")

        elif self.path == "/login":
            with open("inscritos.json", "r+") as DB:
                try:
                    lista = json.loads(DB.read())
                except json.decoder.JSONDecodeError:
                    self.send_code(400)
                    self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
                    self.send_header("Location", f'http://localhost:{httpclass.port}/hola.html')
                    self.end_header()
                    self.send_raw_body("<h1>NO AUTORIZADO </h1>")
            with open("inscritos.json", "r+") as DB:
                try:
                    lista = json.loads(DB.read())
                except json.decoder.JSONDecodeError:
                    lista = {"inscritos": []}
            try:
                user = next(i for i in lista["inscritos"] if i["nombre"]==self.Post["user"])
            except StopIteration:
                user = "not guessed"

            if user != "not guessed":
                if user["contra"]==hashlib.sha512(str(self.Post["password"]).encode("utf-8")).hexdigest():
                    self.send_code(200)
                    self.send_header(
                    "content-type", "text/html"
                    )
                    self.send_header("Set-cookie",f"session-id={hashlib.sha256(str(user['nombre']).encode('utf-8')).hexdigest()}")
                    self.end_header()
                    self.sessions[hashlib.sha256(str(user["nombre"]).encode("utf-8")).hexdigest()]=user
                    self.send_body(f"<h1>Hola {user['nombre']}</h1>")




Api = api()
print("Servidor Iniciado")
Api.run_forever()
