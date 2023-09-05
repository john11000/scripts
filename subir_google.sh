#!/bin/bash

# Obtén la ruta a la carpeta Documents
DOCUMENTS_DIR="$HOME/Documents"
# Crea una variable para el bucket de Google Cloud Storage
BUCKET_NAME="videos-bucket-01"

# Lista de carpetas excluidas
carpetas_excluidas=("My Music" "My Pictures" "My Videos")

# Recorre todas las carpetas de Documents
for folder in "$DOCUMENTS_DIR"/*; do
    # Si la carpeta es un directorio y no está en la lista de carpetas excluidas, súbela
    if [ -d "$folder" ]; then
        nombre_carpeta=$(basename "$folder")
        
        # Verifica si el nombre de la carpeta está en la lista de carpetas excluidas
        excluida=false
        for excluida_folder in "${carpetas_excluidas[@]}"; do
            if [ "$nombre_carpeta" == "$excluida_folder" ]; then
                excluida=true
                break
            fi
        done
        
        if [ "$excluida" == false ]; then
            # Sube la carpeta a Google Cloud Storage
            gsutil cp -r "$folder" "gs://$BUCKET_NAME/$nombre_carpeta"
            # Borra la carpeta local
            rm -r "$folder"
        fi
    fi
done
