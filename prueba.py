'''import json, hashlib
with open("inscritos.json", "r+") as DB:
    try:
        lista = json.loads(DB.read())
    except json.decoder.JSONDecodeError:
        lista = {"inscritos": []}
try:
    user =next(i for i in lista["inscritos"] if i["nombre"]==iuser)
except StopIteration:
    user = "not guessed"

if user != "not guessed":
    if user["contra"]==hashlib.sha512(str(ipass).encode("utf-8")).hexdigest():
        print("Loged")'''

caca="caca:tua:5:tis"
import platform
print(platform.python_compiler)


