import httpclass


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
                    Html= html.read()

                self.send_header("content-Lenght", str(len(Html)))
                self.end_header()
            except IndexError:
                self.send_code(400)
                self.send_header("Archivo", "No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server", "Mtcraft_http_server(python 3.11.1)")
                self.send_header("Archivo", "No encontrado")
                self.end_header()
    def Do_get(self):
        if self.path == "/":
            self.send_code(200)
            self.send_header("Server", "Mtcraft_http_server(python 3.11.1)")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
            with open("hola.html", "r") as body:
                Html = body.read()
            self.send_body(Html)
        else:
            try:
                self.send_code(200)
                self.send_header("Server", "Mtcraft_http_server(python 3.11.1)")
                self.send_header(
                    "content-type", httpclass.httpmimes[self.path.split(".")[1]]
                )
                with open(f".{self.path}", "rb") as body:
                    Html = body.read()
                self.send_header("content-Lenght", str(len(Html)))
                self.end_header()
                if (
                    httpclass.httpmimes[self.path.split(".")[1]].split("/")[0]
                    in "audiovideoimage"
                ):
                    self.send_body(Html, True)
                else:
                    self.send_body(Html.decode())
            except IndexError:
                self.send_code(400)
                self.send_header("Server", "Mtcraft_http_server(python 3.11.1)")
                self.send_header("Archivo", "No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server", "Mtcraft_http_server(python 3.11.1)")
                self.send_header("Archivo", "No encontrado")
                self.end_header()


Api = api()
print("Servidor Iniciado")
Api.run_forever()
