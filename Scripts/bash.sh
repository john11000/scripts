#!/bin/bash

# Directorio donde se buscarán los archivos MP4 de manera recursiva
directory="$HOME/Documents"

# Verificar si FFmpeg está instalado
if ! command -v ffmpeg &>/dev/null; then
  echo "FFmpeg no está instalado. Por favor, instálalo antes de continuar."
  exit 1
fi

# Generar el archivo de lista de archivos
find "$directory" -type f -name "*.mp4" > lista_archivos.txt

# Leer y procesar la lista de archivos línea por línea
while IFS= read -r mp4file; do
  # Obtener el nombre del archivo sin extensión
  filename_no_extension="${mp4file%.*}"

  echo "Procesando archivo: $mp4file"
  
  # Comprimir y convertir a M3U8 (con la ruta entre comillas)
  ffmpeg -c:v libx264 -c:a aac -hls_time 10 -hls_list_size 0 -hls_segment_filename "${filename_no_extension}_%03d.ts" "${filename_no_extension}.m3u8" -i "$mp4file" -y
  
  # Opcional: Eliminar el archivo MP4 original si lo deseas
  rm "$mp4file"
done < lista_archivos.txt

echo "La conversión y compresión de los archivos MP4 en $directory se ha completado."
