import os
import json
import subprocess
import concurrent.futures
import shutil
import re
# Ruta a la carpeta "Documentos" en tu sistema (puede variar según el sistema operativo)
ruta_documentos = os.path.expanduser("~" + os.sep + "Documents")
animes = []
carpetas_excluidas = ['My Music', 'My Pictures', 'My Videos']

def comprimir_y_convertir_a_m3u8(nombre_video, salida):
    nombre_video_salida = nombre_video.splt(".")[-2].split(" ")[-1]
    salida_url = salida + "episodio-" + nombre_video_salida 
    
    # Comando para comprimir el video
    comando_compresion = f'ffmpeg -i {nombre_video} -vf "scale=1280:-1" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -f mp4 -'

    # Comando para convertir a .m3u8
    comando_conversion = 'ffmpeg -i pipe:0 -vf "scale=1280:-1" -c:v h264 -flags +cgop -g 30 -hls_time 4 -hls_list_size 0 -hls_segment_filename segment%d.ts ${salida_url}.m3u8'

    # Crear una tubería para conectar la compresión con la conversión
    proceso_compresion = subprocess.Popen(comando_compresion, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proceso_conversion = subprocess.Popen(comando_conversion, stdin=proceso_compresion.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Esperar a que ambos procesos terminen
    proceso_compresion.wait()
    proceso_conversion.wait()

def procesar_multiples_videos(lista_videos, salida):
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(lista_videos)) as executor:
        executor.map(comprimir_y_convertir_a_m3u8, lista_videos, salida)

def buscar_numero_capitulo(capitulo):
    if re.findall(r"Episode (\d+\.?\d*)", capitulo):
        return re.findall(r"Episode (\d+\.?\d*)", capitulo)[0]
    else:
        return "Especial"

def ordenar_episodios(episodios, aux_episodios = {}, sub_ruta_episodios = ""):
    episodios_cantidad = 0
    mp4s = []
    numeros_de_episodios = []
    nombre_episodio = ""
    for episodio in episodios:
        # Verificar si el archivo es un .mp4
        if episodio.endswith(".mp4"):
            episodio_numero = buscar_numero_capitulo(episodio)
            numeros_de_episodios.append(episodio_numero)
            mp4s.append(sub_ruta_episodios + os.sep + episodio)
            episodios_cantidad = episodios_cantidad + 1
            nombre_episodio = episodio.split(episodio_numero)[0]
    
    numeros_de_episodios = sorted(numeros_de_episodios)
  
    for episodio_pertenece in numeros_de_episodios:
        aux_episodios[str(episodio_pertenece)] = {
            "video" : f"{nombre_episodio} {episodio_pertenece}.mp4",
            "subtitulos": []
         }
        
    return aux_episodios, mp4s

def ordenar_carpetas(episodios, ruta, datos):
    nombre_anime = "";
    
    for directorio in episodios:
        directorio_numero = buscar_numero_capitulo(directorio)
        ruta_destino = ruta + os.sep + "episodio-" + directorio_numero
        if os.path.exists(ruta_destino) == False:

            os.makedirs(ruta_destino)
            os.makedirs(ruta_destino + os.sep + "subtitulos")
            os.makedirs(ruta_destino + os.sep + "hls")
            datos[directorio_numero]['video']
            nombre_anime = ruta + os.sep + directorio

            for subtitulo in datos[directorio_numero]['subtitulos']:
                shutil.move(ruta + os.sep + subtitulo , ruta_destino + os.sep + "subtitulos")
            
            print(nombre_anime)
            shutil.move(directorio , ruta_destino + os.sep + "hls")
        
        #os.rmdir(ruta + os.sep + "episodio-" + str(directorio_numero))

# Verificar si la ruta existe
if os.path.exists(ruta_documentos):
    # Obtener una lista de todas las carpetas en la carpeta "Documentos"
    carpetas_animes = [nombre for nombre in os.listdir(ruta_documentos) if os.path.isdir(os.path.join(ruta_documentos, nombre))]

    # Imprimir el nombre de todas las carpetas
    for carpeta in carpetas_animes:
        if (carpeta not in carpetas_excluidas):
            anime = {
                "titulo" : carpeta,
                "temporadas": []
            }
            sub_ruta_temporada = ruta_documentos + os.sep + carpeta
            if os.path.exists(sub_ruta_temporada):
                sub_carpetas_temporadas = [nombre for nombre in os.listdir(sub_ruta_temporada) if os.path.isdir(os.path.join(sub_ruta_temporada, nombre))]
                idx = 0
                for sub_carpeta in sub_carpetas_temporadas:
                    temporadas = anime["temporadas"]
                    temporadas.append({
                        "id" : idx + 1,
                        "episodios": []
                    })
                    sub_ruta_episodios = sub_ruta_temporada + os.sep + sub_carpeta
                    if os.path.exists(sub_ruta_episodios):
                        episodios = os.listdir(sub_ruta_episodios)
                        idx_episodio = 0
                        aux_episodios = {}
                        aux_episodios_1, mp4s = ordenar_episodios(episodios, aux_episodios, sub_ruta_episodios)
                        #procesar_multiples_videos(mp4s, sub_ruta_episodios)
                        for episodio in episodios:
                            if episodio.split('.')[-1] == "ass":
                                episodio_numero = buscar_numero_capitulo(episodio)
                                aux_episodios_1[episodio_numero]["subtitulos"].append(episodio)
                                
                        temporadas[idx]["episodios"].append(aux_episodios_1)
                        ordenar_carpetas(mp4s, sub_ruta_episodios, aux_episodios_1)
                    idx = idx + 1
            animes.append(anime)
else:
    print("La carpeta 'Documents' no existe en esta ubicación.")

#with open("db1.json", "w") as f:
#    json.dump({ "a": animes }, f)

# Directorio donde se buscarán los archivos MP4 de manera recursiva
directory = os.path.expanduser("~/Documents")

# Función para normalizar una cadena eliminando espacios y reemplazando por guiones bajos
def normalize_string(s):
    return re.sub(r'[^\w\s.-]', '', s).replace(' ', '_')

# Recorrer el directorio de forma recursiva
for root, dirs, files in os.walk(directory):
    for file_name in files:
        if file_name.endswith(".mp4"):
            file_path = os.path.join(root, file_name)
            # Normalizar el nombre del archivo y toda la ruta
            normalized_name = normalize_string(file_name)
            normalized_path = os.path.join(root, normalized_name)

            # Renombrar el archivo con la ruta normalizada
            try:
                os.rename(file_path, normalized_path)
                print(f"Renombrado: {file_path} -> {normalized_path}")
            except Exception as e:
                print(f"No se pudo renombrar {file_path}: {str(e)}")
