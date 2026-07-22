import requests
import urllib.parse

# Configuración de las URLs y tu llave API
ruta_geocode = "https://graphhopper.com/api/1/geocode?"
ruta_route = "https://graphhopper.com/api/1/route?"
key = "a32903d5-7284-4c20-b534-7a134da19f22"

while True:
    print("\n--- Planificador de Viajes ---")
    origen = input("Ingrese Ciudad de Origen (o presione 'v' para salir): ")
    if origen.lower() == 'v':
        print("Saliendo del programa...")
        break

    destino = input("Ingrese Ciudad de Destino (o presione 'v' para salir): ")
    if destino.lower() == 'v':
        print("Saliendo del programa...")
        break

    print("\nOpciones de transporte: car (auto), bike (bicicleta), foot (a pie)")
    vehiculo = input("Elija el tipo de medio de transporte a utilizar: ")
    if vehiculo.lower() == 'v':
        print("Saliendo del programa...")
        break

    # Obtener coordenadas de la Ciudad de Origen
    url_origen = ruta_geocode + urllib.parse.urlencode({"q": origen, "limit": "1", "key": key})
    respuesta_origen = requests.get(url_origen).json()
    
    # Obtener coordenadas de la Ciudad de Destino
    url_destino = ruta_geocode + urllib.parse.urlencode({"q": destino, "limit": "1", "key": key})
    respuesta_destino = requests.get(url_destino).json()

    # Validar que se encontraron las ciudades
    if "hits" in respuesta_origen and len(respuesta_origen["hits"]) > 0 and "hits" in respuesta_destino and len(respuesta_destino["hits"]) > 0:
        lat_origen = respuesta_origen["hits"][0]["point"]["lat"]
        lng_origen = respuesta_origen["hits"][0]["point"]["lng"]
        lat_destino = respuesta_destino["hits"][0]["point"]["lat"]
        lng_destino = respuesta_destino["hits"][0]["point"]["lng"]

        # Solicitar la ruta a Graphhopper
        parametros_ruta = {
            "point": [f"{lat_origen},{lng_origen}", f"{lat_destino},{lng_destino}"],
            "vehicle": vehiculo,
            "locale": "es",
            "key": key
        }
        
        url_ruta = ruta_route + urllib.parse.urlencode(parametros_ruta, doseq=True)
        respuesta_ruta = requests.get(url_ruta).json()

        if "paths" in respuesta_ruta:
            datos_ruta = respuesta_ruta["paths"][0]
            
            # Cálculos de distancia y duración
            distancia_km = datos_ruta["distance"] / 1000
            distancia_millas = distancia_km * 0.621371
            duracion_segundos = datos_ruta["time"] / 1000
            duracion_horas = int(duracion_segundos / 3600)
            duracion_minutos = int((duracion_segundos % 3600) / 60)

            # Imprimir resultados
            print(f"\nDistancia del viaje: {distancia_km:.2f} kilómetros / {distancia_millas:.2f} millas.")
            print(f"Duración del viaje: {duracion_horas} horas y {duracion_minutos} minutos.")
            print("\nNarrativa del viaje paso a paso:")
            
            for instruccion in datos_ruta["instructions"]:
                distancia_instruccion = instruccion["distance"] / 1000
                print(f"- {instruccion['text']} ({distancia_instruccion:.2f} km)")
        else:
            print("No se pudo calcular una ruta con el medio de transporte seleccionado.")
    else:
        print("Error: No se encontraron las coordenadas de una o ambas ciudades.")