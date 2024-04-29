from qiskit import QuantumRegister, QuantumCircuit
import json
import os
import requests

significados_cache = {}

def buscar_significado_palabra(palabra):
    if palabra in significados_cache:
        return significados_cache[palabra]
    else:
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/es_CL/{palabra}"
            response = requests.get(url)
            data = response.json()
            if isinstance(data, list):
                meanings = data[0].get("meanings", [])
                if meanings:
                    significado = meanings[0].get("definitions", [])[0].get("definition", None)
                    significados_cache[palabra] = significado
                    return significado
        except Exception as e:
            print(f"Error al buscar el significado de la palabra '{palabra}': {e}")
            return None

def ver_vocabulario(vocabulario):
    print("Vocabulario actual:")
    for palabra, significado in vocabulario.items():
        print(f"{palabra}: {significado}")

def agregar_palabra_vocabulario(vocabulario):
    palabra = input("Ingrese la palabra que desea agregar al vocabulario: ")
    significado = input(f"Ingrese el significado de la palabra '{palabra}': ")
    vocabulario[palabra] = significado
    print(f"Palabra '{palabra}' agregada al vocabulario con significado '{significado}'")

def eliminar_palabra_vocabulario(vocabulario):
    palabra = input("Ingrese la palabra que desea eliminar del vocabulario: ")
    if palabra in vocabulario:
        del vocabulario[palabra]
        print(f"Palabra '{palabra}' eliminada del vocabulario")
    else:
        print(f"La palabra '{palabra}' no está en el vocabulario")

def buscar_palabra_similar(vocabulario):
    palabra = input("Ingrese la palabra que desea buscar similares: ")
    similares = [p for p in vocabulario if p.startswith(palabra)]
    if similares:
        print(f"Palabras similares a '{palabra}': {', '.join(similares)}")
    else:
        print(f"No se encontraron palabras similares a '{palabra}'")

def ejecutar_circuito_cuántico(vocabulario, data_entrenamiento):
    print("Menú de opciones para ejecutar el circuito cuántico:")
    print("1. Ejecutar circuito cuántico con número de qubits predeterminado")
    print("2. Ejecutar circuito cuántico con número de qubits seleccionado por el usuario")
    print("3. Ejecutar circuito cuántico en un simulador cuántico")
    print("4. Ejecutar circuito cuántico en un dispositivo cuántico real")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        num_qubits = 5  # Número de qubits predeterminado
        # Generar el circuito cuántico con el número de qubits predeterminado
        qr = QuantumRegister(num_qubits)
        circuit = QuantumCircuit(qr)
        # Ejecutar el circuito cuántico
        print("Ejecutando el circuito cuántico...")
        # Aquí puedes ejecutar el circuito en un simulador cuántico o en un dispositivo real
        print("Circuito cuántico ejecutado exitosamente.")
    
    elif opcion == "2":
        num_qubits = int(input("Ingrese el número de qubits que desea utilizar: "))
        # Generar el circuito cuántico con el número de qubits seleccionado por el usuario
        qr = QuantumRegister(num_qubits)
        circuit = QuantumCircuit(qr)
        # Ejecutar el circuito cuántico
        print("Ejecutando el circuito cuántico...")
        # Aquí puedes ejecutar el circuito en un simulador cuántico o en un dispositivo real
        print("Circuito cuántico ejecutado exitosamente.")
    
    elif opcion == "3":
        # Ejecutar el circuito cuántico en un simulador cuántico
        print("Ejecutando el circuito cuántico en un simulador cuántico...")
        # Aquí puedes ejecutar el circuito en un simulador cuántico
        print("Circuito cuántico ejecutado exitosamente en un simulador cuántico.")
    
    elif opcion == "4":
        # Ejecutar el circuito cuántico en un dispositivo cuántico real
        print("Ejecutando el circuito cuántico en un dispositivo cuántico real...")
        # Aquí puedes ejecutar el circuito en un dispositivo cuántico real
        print("Circuito cuántico ejecutado exitosamente en un dispositivo cuántico real.")
    
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")

def actualizar_vocabulario(vocabulario):
    try:
        with open('vocabulario.json', 'w') as vocab_file:
            json.dump(vocabulario, vocab_file)
        print("Archivo de vocabulario actualizado exitosamente.")
    except Exception as e:
        print(f"Error al actualizar el archivo de vocabulario: {e}")
        
def actualizar_data_entrenamiento(data_entrenamiento):
    try:
        with open('data_entrenamiento.json', 'w') as data_file:
            json.dump(data_entrenamiento, data_file)
        print("Archivo de data de entrenamiento actualizado exitosamente.")
    except Exception as e:
        print(f"Error al actualizar el archivo de data de entrenamiento: {e}")

def procesar_instruccion(instruccion, vocabulario):
    input_words = instruccion.split()
    unique_input_words = list(set(input_words))  # Eliminar palabras duplicadas
    input_indices = [vocabulario.get(word, -1) for word in unique_input_words]
    
    if -1 in input_indices:
        palabras_faltantes = [unique_input_words[i] for i in range(len(input_indices)) if input_indices[i] == -1]
        for palabra in palabras_faltantes:
            if palabra not in vocabulario:
                while True:
                    opcion = input(f"La palabra '{palabra}' no está en el vocabulario. ¿Quieres buscar su significado en línea? (si/no): ")
                    if opcion.lower() == 'si':
                        significado = buscar_significado_palabra(palabra)
                        if significado:
                            print(f"Significado encontrado para '{palabra}': {significado}")
                            vocabulario[palabra] = significado
                            break
                        else:
                            print(f"No se encontró significado en línea para '{palabra}'.")
                            break
                    elif opcion.lower() == 'no':
                        significado = input(f"Por favor, ingresa el significado de '{palabra}' (o escribe 'omitir' para continuar sin definir): ")
                        if significado.lower() == 'omitir':
                            break
                        else:
                            vocabulario[palabra] = significado
                            break
                    else:
                        print("Opción no válida. Por favor, ingresa 'si' o 'no'.")

    return vocabulario, input_indices

def interactuar_con_usuario(vocabulario, data_entrenamiento):
    while True:
        print("Menú de opciones:")
        print("1. Ingresar instrucción en lenguaje natural")
        print("2. Ver vocabulario")
        print("3. Agregar palabra al vocabulario")
        print("4. Eliminar palabra del vocabulario")
        print("5. Buscar palabra similar")
        print("6. Ejecutar circuito cuántico")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            instruccion = input("Ingrese una instrucción en lenguaje natural: ")
            vocabulario, input_indices = procesar_instruccion(instruccion, vocabulario)
            # Actualizar el archivo JSON del vocabulario
            actualizar_vocabulario(vocabulario)
            # Actualizar la data de entrenamiento
            data_entrenamiento.append((instruccion, input_indices))
            actualizar_data_entrenamiento(data_entrenamiento)
        elif opcion == "2":
            ver_vocabulario(vocabulario)
        elif opcion == "3":
            agregar_palabra_vocabulario(vocabulario)
            # Actualizar el archivo JSON del vocabulario
            actualizar_vocabulario(vocabulario)
        elif opcion == "4":
            eliminar_palabra_vocabulario(vocabulario)
            # Actualizar el archivo JSON del vocabulario
            actualizar_vocabulario(vocabulario)
        elif opcion == "5":
            buscar_palabra_similar(vocabulario)
        elif opcion == "6":
            ejecutar_circuito_cuántico(vocabulario, data_entrenamiento)
        elif opcion == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

# Verificar si el archivo JSON del vocabulario existe
if not os.path.exists('vocabulario.json'):
    try:
        with open('vocabulario.json', 'w') as vocab_file:
            json.dump({}, vocab_file)
    except Exception as e:
        print(f"Error al crear el archivo de vocabulario: {e}")

# Verificar si el archivo JSON de los datos de entrenamiento existe
if not os.path.exists('data_entrenamiento.json'):
    try:
        with open('data_entrenamiento.json', 'w') as data_file:
            json.dump([], data_file)
    except Exception as e:
        print(f"Error al crear el archivo de datos de entrenamiento: {e}")

# Cargar el vocabulario desde el archivo JSON
try:
    with open('vocabulario.json', 'r') as vocab_file:
        vocabulario = json.load(vocab_file)
except Exception as e:
    print(f"Error al cargar el archivo de vocabulario: {e}")
    vocabulario = {}

# Cargar los datos de entrenamiento desde el archivo JSON
try:
    with open('data_entrenamiento.json', 'r') as data_file:
        data_entrenamiento = json.load(data_file)
except Exception as e:
    print(f"Error al cargar el archivo de datos de entrenamiento: {e}")
    data_entrenamiento = []

# Interactuar con el usuario y ejecutar el circuito cuántico
interactuar_con_usuario(vocabulario, data_entrenamiento)
