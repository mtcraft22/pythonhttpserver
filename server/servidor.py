import httpclass
import json
import platform
import hashlib
import sqlite3

con = sqlite3.connect("../db/Rockandplaydb.db")
cur = con.cursor()

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
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("Archivo", "No encontrado")
                self.end_header()

    def Do_get(self):
        print("loged", self.sessions)
        if "db" in self.path:
            self.send_code(400)
            self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
            self.send_body("""<h1>no permitido</h1>""")

        if self.path == "/":
            self.send_code(200)
            self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
            with open("../main.html", "r") as body:
                html = body.read()
            self.send_body(html)
        
       

        else:
            try:
                with open(f"./../{self.path}", "rb") as body:
                    html = body.read()
               
                self.send_code(200)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header(
                    "content-type", httpclass.httpmimes[self.path.split(".")[1]]
                )
                
                self.send_header("content-Lenght", str(len(html)))
                self.end_header()
                if(
                    httpclass.httpmimes[self.path.split(".")[1]].split("/")[0]
                    in "audiovideoimagefont"
                ):
                    self.send_binary(html)
                else:
                    self.send_body(html.decode())
            except IndexError:
                self.send_code(400)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("Archivo", "No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("Archivo", "No encontrado")
                self.end_header()

    def Do_post(self):
        self.Post = {}
        try:
            
            valores = self._message.splitlines()[-1]
            if "&" in valores:
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
            else:
                self.Post[valores.split("=")[0]]=valores.split("=")[1]
        except  IndexError:
            self.Post={}
        if self.path == "/usuarios":
            self.send_code(201)
            self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
            self.send_header("Location", f"http://{httpclass.ip}:{httpclass.port}/registrado.html")
            self.end_header()

            with open("./../db/leage/inscritos.json", "r+") as DB:
                try:
                    lista = json.loads(DB.read())
                except json.decoder.JSONDecodeError:
                    lista = {"inscritos": []}
                
                self.Post["contra"] = hashlib.sha512(str(self.Post["contra"]).encode("utf-8")).hexdigest()
                if not("juegos" in self.Post):
                    self.Post["juegos"] = [] 
                lista["inscritos"].append(self.Post)
                DB.truncate(0)
                DB.seek(0,0)
                DB.write(json.dumps(lista, indent=4))
                DB.write("\n")
            consulta = f"INSERT INTO Players (id,name,last_name,password,email,genere) VALUES (NULL,'{self.Post['nombre'].lower()}','{self.Post['apedillo'].lower()}','{self.Post['contra']}','{self.Post['correo'].lower()}','{self.Post['genero'].lower()}')"
            cur.execute(consulta)
            cur.execute("COMMIT")
        elif self.path == "/logedinfo":
            try:
                for cookie in self.headers["Cookie"].split(";"):
                    if "session-id" in cookie.split("=")[0]:
                        print("value",cookie.split("=")[1] )
                        id =  cookie.split("=")[1]
                        self.send_code(200)
                        self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                        self.send_header("content-type", httpclass.httpmimes['json'])
                        self.end_header()
                        self.sessions[id[:-1]]["loged"]=True
                        self.send_body(json.dumps(self.sessions[id[:-1]]))
            except KeyError:
                self.send_code(200)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("content-type", httpclass.httpmimes['json'])
                self.end_header()
                self.send_body(json.dumps({"loged":False}))
        elif self.path == "/apcetar":
            if "Cookie" in self.headers:
                for cookie in self.headers["Cookie"].split(";"):
                    if "session-id" in cookie.split("=")[0]:
                        print("value",cookie.split("=")[1] )
                        id =  cookie.split("=")[1]
                        with open("./../db/leage/inscritos.json","r+") as JugaroresDB:
                            DB = json.loads(JugaroresDB.read())
                            for i in DB["inscritos"]:
                                if (i["nombre"] == self.sessions[id[:-1]]["nombre"]):
                                    if (type(i["juegos"])!=list):
                                        prev = self.sessions[id[:-1]]["juegos"]
                                        self.sessions[id[:-1]]["juegos"] = list(self.sessions[id[:-1]]["juegos"])
                                        self.sessions[id[:-1]]["juegos"].clear()
                                        self.sessions[id[:-1]]["juegos"].append(prev)  
                                        self.sessions[id[:-1]]["juegos"].append(self.Post["game"])
                                        prev = i["juegos"]
                                        i["juegos"] = list(i["juegos"])
                                        i["juegos"].clear()
                                        i["juegos"].append(prev)  
                                        i["juegos"].append(self.Post["game"])
                                    else:
                                        self.sessions[id[:-1]]["juegos"].append(self.Post["game"])
                                        i["juegos"].append(self.Post["game"])
                            JugaroresDB.truncate(0)
                            JugaroresDB.seek(0,0)
                            JugaroresDB.write(json.dumps(DB, indent=4))
                            JugaroresDB.write("\n")
                        self.send_code(200)
                        self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                        self.end_header()
                        self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Liga de juegos</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Inscrito en {self.Post["game"]}</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/catalogo.html'>Ir a catalogo</a>
</html>""")
        elif self.path == "/cancelar":
            if "Cookie" in self.headers:
                for cookie in self.headers["Cookie"].split(";"):
                    if "session-id" in cookie.split("=")[0]:
                        print("value",cookie.split("=")[1] )
                        id =  cookie.split("=")[1]
                        with open("./../db/leage/inscritos.json","r+") as JugaroresDB:
                            DB = json.loads(JugaroresDB.read())
                            for i in DB["inscritos"]:
                                if (i["nombre"] == self.sessions[id[:-1]]["nombre"]):
                                    if (type(i["juegos"])!=list):
                                        i["juegos"] = []
                                        self.sessions[id[:-1]]["juegos"] = []
                                    else:
                                        self.sessions[id[:-1]]["juegos"].remove(self.Post["game"])
                                        i["juegos"].remove(self.Post["game"])
                            JugaroresDB.truncate(0)
                            JugaroresDB.seek(0,0)
                            JugaroresDB.write(json.dumps(DB,indent=4))
                            JugaroresDB.write("\n")
                        self.send_code(200)
                        self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                        self.end_header()
                        self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Liga de juegos</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Eliminado de {self.Post["game"]}</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/catalogo.html'>Ir a catalogo</a>
</html>""")
                                                                          

        elif self.path == "/catalogo":
            if "Cookie" in self.headers:
                    for cookie in self.headers["Cookie"].split(";"):
                        if "session-id" in cookie.split("=")[0]:
                            try:
                                user =  self.sessions[cookie.split("=")[1][:-1]]
                            except KeyError:
                                self.send_code(403)
                                self.send_header("Server",f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                                self.end_header()
                                self.send_body("""<!DOCTYPE html>
<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='/css/main.css'>
</head>
<body><h1>No disponible</h1></body>
""")
                            games = user["juegos"]
                            with open("./../db/leage/juegos.json", "r+") as gamesDB:
                                try:
                                    GamesDB = json.loads(gamesDB.read())
                                except json.decoder.JSONDecodeError:
                                    GamesDB = {}
                            for i in GamesDB["video_games"]:
                                if (i["name"] in games):
                                    i["subscrito"] = True
                                else:
                                    i["subscrito"] = False
                            self.send_code(200)
                            self.send_header("Server",f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                            self.send_header("content-type",httpclass.httpmimes["json"])
                            self.end_header()
                            self.send_body(json.dumps(GamesDB, indent=4))


            else:
                self.send_code(403)
                self.send_header("Server",f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.end_header()
                self.send_body("""<!DOCTYPE html>
<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='/css/main.css'>
</head>""")
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
    <link rel='stylesheet' href='/css/main.css'>
</head>""")
            self.send_body(f"<h1> Sessión cerrada </h1>")
            self.send_body(f"<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Inicio </a>")
            

        elif self.path == "/login":
            with open("./../db/leage/inscritos.json", "r+") as DB:
                try:
                    lista = json.loads(DB.read())
                except json.decoder.JSONDecodeError:
                    self.send_code(400)
                    self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                    self.send_header("Location", f'http://{httpclass.ip}:{httpclass.port}/liga.html')
                    self.end_header()
                    self.send_raw_body("<h1>NO AUTORIZADO </h1>")
            with open("./../db/leage/inscritos.json", "r+") as DB:
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
    <link rel='stylesheet' href='/css/main.css'>
</head>""")
                    self.send_body(f"<h1>Hola {user['nombre']}</h1>")
                    self.send_body(f"<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Vuelve al inicio</a>")
                else:
                    self.send_code(403)
                    self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                    self.end_header()
                    self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Liga de juegos</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Usuario o contraseña incorrectos</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Intente de nuevo</a>
</html>""")

            else:
                self.send_code(403)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.end_header()
                self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Liga de juegos</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Usuario o contraseña incorrectos</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Intente de nuevo</a>
</html>""")




Api = api()
print("Servidor Iniciado")
Api.run_forever()
