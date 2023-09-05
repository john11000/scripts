import os
import shutil

carpetas_excluidas = ['My Music', 'My Pictures', 'My Videos', 'desktop.ini']
def buscar_y_borrar(directorio):
  for directorio_documento in os.listdir(directorio):
    if (directorio_documento not in carpetas_excluidas):
      if os.path.isdir(os.path.join(directorio, directorio_documento)):
        buscar_y_borrar(os.path.join(directorio, directorio_documento))
      else:
        #if directorio_documento.endswith(".mp4") and "_comprimido" in directorio_documento:
        if directorio_documento.endswith(".m3u8") or directorio_documento.endswith(".ts"):
          os.remove(os.path.join(directorio, directorio_documento))


directorio = os.path.expanduser("~" + os.sep + "Documents")
print(directorio)
buscar_y_borrar(directorio)