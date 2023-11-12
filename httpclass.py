import socket
# levantamos el socket tcp para cominicanos con el navegador via http
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    servidor.bind(("localhost", 8081))
    print("On port: 8081")
except OSError:
    servidor.bind(("localhost", 8080))
    print("On port: 8080")
servidor.listen(5)
# codigos de estado http
httpstatus = {
    100: "100 Continue",
    200: "200 OK",
    400: "400 Bad request",
    404: "404 Page not found",
    500: "500 Internal server error",
    501: "501 Not implemented",
}
# extenciones de archivos mimes

httpmimes = {
    # text files
    "txt": "text/plain",
    "js": "text/javascript",
    "html": "text/html",
    "css": "text/css",
    # images formts
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "png": "image/png",
    "svg": "image/svg+xml",
    "ico": "image/x-incon",
    "webp": "image/webp",
    # binary partition
    "byte_range": "multipart/byteranges",
    "formulario_multiparte": "multipart/form-data",
    # audio
    "waw": "audio/waw",
    "ogg": "audio/ogg",
    "midi": "audio/midi",
    # video
    "mp4": "video/mp4",
    # binario
    "otro": "application/octet-stream",
    "pkcs12": "application/pkcs12",
    "vnd.mspowerpoint": "application/vnd.mspowerpoints",
    "xhtml": "application/xhtml+xml",
    "xml": "application/xml",
    "pdf": "application/pdf",
    "json": "application/json",
    "toml": "text/toml"
}


class httpmessage:
    def __init__(self) -> None:
        self._message = None
        self.command = None
        self.path = None
        self.headers = {}
        self.Post = {}
        self.Get = {}
        self.body = None

    def send_status_code(self, code):
        self._message = f"""
HTTP/1.1 {code}\r\n
        """

    def send_code(self, code):
        self._message = f"HTTP/1.1 {httpstatus[code]}\n"

    def send_header(self, key, value):
        self._message += f"{key} : {value}\n"
        
    def send_body(self, body, binari=False):
        if binari:
            self._message = self._message.encode()
            self._message += body
        else:
            self._message += f"{body}"
            self._message = self._message.encode()

    def end_header(self):
        self._message += "\r\n"

    def Do_Options(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_patch(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_Put(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_Trace(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_get(self):
        pass

    def Do_post(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_Head(self):
        pass

    def Do_connect(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_delete(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def run_forever(self):
        while True:
            enchufe, direcion = servidor.accept()
            self._message = enchufe.recv(1024).decode("utf-8")
            self.command = self._message.split(" ")[0]
            try:
                self.path = self._message.split(" ")[1]
            except IndexError as e:
                print("No puedo manejar peticiones http sin el path")
                break
            i = 1
            print(self._message)

            while self._message.splitlines()[i] != " \r\n":
                """
                    si no hay indice 1 al separar la cadena por los : , 
                    significa que ya no hay mas cabeceras
                """
                try:  
                    self.headers[
                        self._message.splitlines()[i].split(":")[0]
                    ] = self._message.splitlines()[i].split(":")[1]
                except IndexError:
                    self.headers = {}
                    break
                i += 1
          
            match self.command:
                case "CONNECT":
                    self.Do_connect()
                case "DELETE":
                    self.Do_delete()
                case "GET":
                    self.Do_get()
                case "HEAD":
                    self.Do_Head()
                case "OPTIONS":
                    self.Do_Options()
                case "PATCH":
                    self.Do_patch()
                case "POST":
                    self.Do_post()  
                case "PUT":
                    self.Do_Put()
                case "TRACE":
                    self.Do_Trace()
            print(self._message)

            try:
                enchufe.send(self._message)
            except TypeError:
                enchufe.send(self._message.encode())
            enchufe.close()
