import httpclass
import json
import platform

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
        if (self.path == "/user"):
            valores = self._message.splitlines()[-1]
            for i in valores.split("&"):
                self.Post[i.split("=")[0]] = i.split("=")[1]
            self.send_code(200)
            self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
            self.send_header("location", "/")
            self.end_header()
            with open("usuarios.json", "r+") as DB:
                try:
                    lista = json.loads(DB.read())
                except json.decoder.JSONDecodeError:
                    lista = {"usuarios": []}
                lista["usuarios"].append(self.Post)
                DB.seek(0,0)
                DB.write(json.dumps(lista, indent=4))
                DB.write("\n")

Api = api()
print("Servidor Iniciado")
Api.run_forever()
