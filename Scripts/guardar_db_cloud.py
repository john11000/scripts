import os
import json
import requests
 # Conexion a mongodb

# base de datos para desarrollo
carpetas_excluidas = ['My Music', 'My Pictures', 'My Videos', 'desktop.ini']

def directorio_a_json(directorio):
    estructura = []
    for item in os.listdir(directorio):
        if item not in carpetas_excluidas:
            anime = {}
            ruta_item = os.path.join(directorio, item)
            if os.path.isdir(ruta_item):
                anime[item] = directorio_a_json(ruta_item)
            elif os.path.isfile(ruta_item):
                anime[item] = item
            estructura.append(anime) 
    return estructura

directorio_base = os.path.expanduser("~" + os.sep + "Documents")  # Reemplaza con la ruta de tu directorio "Documents"
estructura_json = directorio_a_json(directorio_base)

# Guardar la estructura en un archivo JSON
# with open("estructura.json", "w") as archivo_json:
#     json.dump(estructura_json, archivo_json, indent=4)
#     collection_dev.insert_one([*estructura_json])
# Serialize the Python object to JSON
json_data = json.dumps({"animes":estructura_json})
# Send the JSON data in the request
response = requests.post("https://flask-server2.vercel.app/saveToDb", data=json_data, headers={"Content-Type": "application/json"})

print(response)
   # collection_dev.insert_one(video_to_save)
print("Estructura JSON generada y guardada en estructura.json")


# with open("db1.json", "w") as f:
#     json.dump({"animes":estructura_json}, f)
