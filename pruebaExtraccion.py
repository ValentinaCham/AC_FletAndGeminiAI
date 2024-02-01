import json
import re
from datetime import datetime

def fechaHora():
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now()

    # Formatear la fecha y hora como una cadena
    formato = "%Y-%m-%d %H:%M:%S"  # Puedes ajustar el formato según tus preferencias
    fecha_hora_str = fecha_hora_actual.strftime(formato)
    return fecha_hora_str

def pasarData(contenido):

    # Patrón de expresión regular para extraer el contenido entre las comillas triples ```
    patron = r'```(.*?)```'

    # Busca coincidencias en el JSON usando la expresión regular
    coincidencias = re.findall(patron, contenido, re.DOTALL)

    # Si hay coincidencias, toma la primera (en este caso, debería ser la única)
    if coincidencias:
        contenido_extraido = coincidencias[0]


    try:
        # Intenta cargar el contenido como JSON
        datos_json = json.loads(contenido_extraido)

        # Resto del código...
        concepto = datos_json["concepto"]
        respuesta = datos_json["respuesta"]
        nuevo_json = {concepto: respuesta}
        print(json.dumps(nuevo_json, indent=2, ensure_ascii=False))

    except json.decoder.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
    except Exception as e:
        print(f"Error general: {e}")

    # Nombre del archivo JSON existente
    archivo_existente = 'data.json'

    # Leer el contenido del archivo JSON existente
    with open(archivo_existente, 'r') as archivo:
        contenido_existente = json.load(archivo)

    # Agregar el nuevo JSON al contenido existente
    contenido_existente.update(nuevo_json)

    # Escribir el contenido actualizado de vuelta al archivo
    with open(archivo_existente, 'w') as archivo:
        json.dump(contenido_existente, archivo, indent=2)
    
    print(f"Se agregó el nuevo JSON al archivo {archivo_existente}.")
