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
        print("loged",self.sessions)
        
            
        if self.path == "/":
            self.send_code(200)
            self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
            with open("hola.html", "r") as body:
                html = body.read()
            self.send_body(html)
        #if "/juego/" in self.path:

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
                if "Cookie" in self.headers:
                    for cookie in self.headers["Cookie"].split(";"):
                        if "session-id" in cookie.split("=")[0]:
                            print("value",cookie.split("=")[1] )
                            if httpclass.httpmimes[self.path.split(".")[1]]== "text/html":
                                try:
                                    id =  cookie.split("=")[1]
                                    self.send_body(f"<h1>Usuario: {self.sessions[id[:-1]]['nombre']}</h1>")
                                    self.send_body("<form id='logout' action='logout' method='post'><button type='submit'>Cerrar la sessiòn</button></form>")
                                except KeyError:
                                    self.send_body(f"<br>")
                if (
                    httpclass.httpmimes[self.path.split(".")[1]].split("/")[0]
                    in "audiovideoimagefont"
                ):
                    self.send_binary(html)
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
        self.Post = {}
        try:
            
            valores = self._message.splitlines()[-1]
            for i in valores.split("&"):
                if i.split("=")[0] in self.Post:
                    print (type(self.Post[i.split("=")[0]]))
                    
                    if type(self.Post[i.split("=")[0]]) != list:
                        prev = self.Post[i.split("=")[0]]
                        self.Post[i.split("=")[0]]=list(self.Post[i.split("=")[0]])
                        self.Post[i.split("=")[0]].clear()
                        self.Post[i.split("=")[0]].append(prev)  
                        self.Post[i.split("=")[0]].append(i.split("=")[1])
                    else:
                        self.Post[i.split("=")[0]].append(i.split("=")[1]) 
                else:
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
            if "Cookie" in self.headers:
                    for cookie in self.headers["Cookie"].split(";"):
                        if "session-id" in cookie.split("=")[0]:
                            print("value",cookie.split("=")[1] )
                            
                            id =  cookie.split("=")[1]
                            self.sessions.pop(id[:-1])
                            
            self.send_code(200)
            self.send_header("Set-cookie",f"session-id={cookie.split('=')[1][:-1]};Expires=Thu,01 Jan 1970 00:00:00 GMT")
            self.end_header()
            self.send_body("""<!DOCTYPE html>
<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='main.css'>
</head>""")
            self.send_body(f"<h1> Sessión cerrada </h1>")
            self.send_body(f"<a href='http://localhost:{httpclass.port}/liga.html'>Inicio </a>")
            

        elif self.path == "/login":
            with open("inscritos.json", "r+") as DB:
                try:
                    lista = json.loads(DB.read())
                except json.decoder.JSONDecodeError:
                    self.send_code(400)
                    self.send_header("Server", f"Mtcraft_http_server(python {VERSION})")
                    self.send_header("Location", f'http://localhost:{httpclass.port}/liga.html')
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
                    self.send_body("""<!DOCTYPE html>
<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='main.css'>
</head>""")
                    self.send_body(f"<h1>Hola {user['nombre']}</h1>")
                    self.send_body(f"<a href='http://localhost:{httpclass.port}/liga.html'>Vuelve al inicio</a>")




Api = api()
print("Servidor Iniciado")
Api.run_forever()
