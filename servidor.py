from httpclass import *

class api(httpmessage):
    def __init__(self):
        super().__init__()
    def Do_get(self):
        if self.path=="/":
            self.send_code(200)
            self.send_header("Server","Mtcraft_http_server")
            self.send_header("content-type",httpmimes["html"])
            self.end_header()
            with open("hola.html","r") as body:
                Html=body.read()
            self.send_body(Html)
        else:
            try:
                self.send_code(200)
                self.send_header("Server","Mtcraft_http_server")
                self.send_header("content-type",httpmimes[self.path.split(".")[1]])
                self.end_header()
                with open(f".{self.path}","r") as body:
                    Html=body.read()
                self.send_body(Html)
            except IndexError:
                self.send_code(400)
                self.send_header("Archivo","No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server","Mtcraft_http_server")
                self.send_header("Archivo","No encontrado")
                self.end_header()

Api=api()
Api.run_forever()