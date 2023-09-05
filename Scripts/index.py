from moviepy.editor import VideoFileClip
import os
def comprimir_y_convertir_a_m3u8(nombre_video, salida_video):
    clip = VideoFileClip(nombre_video)
    clip_resized = clip.resize(width=1280)
    clip_resized.write_videofile(salida_video, codec="libx264", audio_codec="aac", fps=30)

directorio_documentos = os.path.join(os.path.expanduser("~"), "Documents")
carpetas_excluidas = ['My Music', 'My Pictures', 'My Videos']
lista_videos = []

def buscar_archivos_mp4(ruta_directorio):
    archivos = os.listdir(ruta_directorio)
    for archivo in archivos:
        if archivo not in carpetas_excluidas:
            if archivo.endswith(".mp4"):
                lista_videos.append(os.path.join(ruta_directorio, archivo))
                print(os.path.join(ruta_directorio, archivo))

buscar_archivos_mp4(directorio_documentos)

for video in lista_videos:
    salida_video = os.path.splitext(video)[0] + "_salida.mp4"
    comprimir_y_convertir_a_m3u8(video, salida_video)
