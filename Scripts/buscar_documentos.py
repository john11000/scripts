import os
import json
import subprocess
import concurrent.futures
import shutil

# Ruta a la carpeta "Documentos" en tu sistema (puede variar según el sistema operativo)
ruta_documentos = os.path.expanduser("~" + os.sep + "Documents")
animes = []
carpetas_excluidas = ['My Music', 'My Pictures', 'My Videos', 'desktop.ini']

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


def ordenar_episodios(episodios, aux_episodios, sub_ruta_episodios):
    episodios_cantidad = 0
    mp4s = []
    for episodio in episodios:
        # Verificar si el archivo es un .mp4
        if episodio.endswith(".mp4"):
            mp4s.append(sub_ruta_episodios + os.sep + episodio)
            episodios_cantidad = episodios_cantidad + 1
            
    for episodio_pertenece in range(episodios_cantidad):
        numero = episodio_pertenece + 1
        aux_episodios[str(numero)] = {
            "video" : f"episodio-{numero}.mp4",
            "subtitulos": []
         }
    return aux_episodios, mp4s

def ordenar_carpetas(episodios, ruta, datos):
    nombre_anime = "";
    
    for directorio in range(len(episodios)):
        directorio_numero = directorio + 1
        directorio_numero = str(directorio_numero)
        ruta_destino = ruta + os.sep + "episodio-" + directorio_numero
        os.makedirs(ruta_destino)
        os.makedirs(ruta_destino + os.sep + "subtitulos")
        os.makedirs(ruta_destino + os.sep + "hls")
        datos[directorio_numero]['video']
        for subtitulo in datos[directorio_numero]['subtitulos']:
            nombre_anime = ruta + os.sep + subtitulo.split(".")[0] + ".mp4"
            shutil.move(ruta + os.sep + subtitulo , ruta_destino + os.sep + "subtitulos")
        
        shutil.move(nombre_anime , ruta_destino + os.sep + "hls")
        
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
                        "id" : idx,
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
                                episodio_numero = episodio.split(".")[0].split(" ")[-1]
                                aux_episodios_1[episodio_numero]["subtitulos"].append(episodio)
                                
                        temporadas[idx]["episodios"].append(aux_episodios_1)
                        ordenar_carpetas(mp4s, sub_ruta_episodios, aux_episodios_1)
                    idx = idx + 1
            animes.append(anime)
else:
    print("La carpeta 'Documents' no existe en esta ubicación.")

with open("db1.json", "w") as f:
    json.dump({ "a": animes }, f)
