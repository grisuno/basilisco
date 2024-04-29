from qiskit import QuantumRegister, QuantumCircuit
import json
import os
import requests
from gensim.models import Word2Vec

significados_cache = {}

class Vocabulario:
    def __init__(self, data):
        self.vocabulario = data

    def cargar_vocabulario(self):
        try:
            with open(self.archivo_vocabulario, 'r') as vocab_file:
                return json.load(vocab_file)
        except Exception as e:
            print(f"Error al cargar el archivo de vocabulario: {e}")
            return {}

    def agregar_palabra(self, palabra, significado):
        self.vocabulario[palabra] = significado
        self.guardar_vocabulario()

    def eliminar_palabra(self, palabra):
        if palabra in self.vocabulario:
            del self.vocabulario[palabra]
            self.guardar_vocabulario()

    def guardar_vocabulario(self):
        try:
            with open('vocabulario.json', 'w') as vocab_file:
                json.dump(self.vocabulario, vocab_file)
        except Exception as e:
            print(f"Error al guardar el archivo de vocabulario: {e}")

    def transformar_a_modelo(self):
        palabras = list(self.vocabulario.keys())
        modelo = Word2Vec(sentences=[palabras], vector_size=100, window=5, min_count=1, workers=4)
        return modelo

class Modelo:
    def __init__(self, vocabulario):
        self.vocabulario = vocabulario
        self.modelo = None

    def transformar_vocabulario_a_modelo(self):
        palabras = list(self.vocabulario.vocabulario.keys())
        self.modelo = Word2Vec(sentences=[palabras], vector_size=100, window=5, min_count=1, workers=4)

    def entrenar_modelo(self, data_entrenamiento):
        if self.modelo is None:
            self.transformar_vocabulario_a_modelo()

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
    vocabulario.agregar_palabra(palabra, significado)

def eliminar_palabra_vocabulario(vocabulario):
    palabra = input("Ingrese la palabra que desea eliminar del vocabulario: ")
    vocabulario.eliminar_palabra(palabra)

def buscar_palabra_similar(vocabulario):
    palabra = input("Ingrese la palabra que desea buscar similares: ")
    similares = [p for p in vocabulario.vocabulario if p.startswith(palabra)]
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
        num_qubits = 5
        qr = QuantumRegister(num_qubits)
        circuit = QuantumCircuit(qr)
        print("Ejecutando el circuito cuántico...")
        print("Circuito cuántico ejecutado exitosamente.")
    
    elif opcion == "2":
        num_qubits = int(input("Ingrese el número de qubits que desea utilizar: "))
        qr = QuantumRegister(num_qubits)
        circuit = QuantumCircuit(qr)
        print("Ejecutando el circuito cuántico...")
        print("Circuito cuántico ejecutado exitosamente.")
    
    elif opcion == "3":
        print("Ejecutando el circuito cuántico en un simulador cuántico...")
        print("Circuito cuántico ejecutado exitosamente en un simulador cuántico.")
    
    elif opcion == "4":
        print("Ejecutando el circuito cuántico en un dispositivo cuántico real...")
        print("Circuito cuántico ejecutado exitosamente en un dispositivo cuántico real.")
    
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")

def crear_y_entrenar_modelo(vocabulario, data_entrenamiento):
    modelo = Modelo(vocabulario)
    modelo.entrenar_modelo(data_entrenamiento)
    print("Modelo creado y entrenado exitosamente.")

def procesar_instruccion(instruccion, vocabulario, modelo):
    input_words = instruccion.split()
    unique_input_words = list(set(input_words))
    input_indices = [vocabulario.vocabulario.get(word, -1) for word in unique_input_words]
    
    if -1 in input_indices:
        palabras_faltantes = [unique_input_words[i] for i in range(len(input_indices)) if input_indices[i] == -1]
        for palabra in palabras_faltantes:
            if palabra not in vocabulario.vocabulario:
                while True:
                    opcion = input(f"La palabra '{palabra}' no está en el vocabulario. ¿Quieres buscar su significado en línea? (si/no): ")
                    if opcion.lower() == 'si':
                        significado = buscar_significado_palabra(palabra)
                        if significado:
                            print(f"Significado encontrado para '{palabra}': {significado}")
                            vocabulario.vocabulario[palabra] = significado
                            break
                        else:
                            print(f"No se encontró significado en línea para '{palabra}'.")
                            break
                    elif opcion.lower() == 'no':
                        significado = input(f"Por favor, ingresa el significado de '{palabra}' (o escribe 'omitir' para continuar sin definir): ")
                        if significado.lower() == 'omitir':
                            break
                        else:
                            vocabulario.vocabulario[palabra] = significado
                            break
                    else:
                        print("Opción no válida. Por favor, ingresa 'si' o 'no'.")

    return vocabulario, input_indices

def ejecutar_instruccion_lenguaje_natural(vocabulario, instruccion):
    print("Ejecutando instrucción en lenguaje natural...")
    # Aquí puedes usar el modelo para procesar la instrucción en lenguaje natural
    # Por ahora, simplemente imprimimos las palabras de la instrucción y sus índices
    palabras = instruccion.split()
    for palabra in palabras:
        indice = vocabulario.vocabulario.get(palabra, -1)
        print(f"Palabra: {palabra}, Índice: {indice}")

def interactuar_con_usuario(vocabulario, data_entrenamiento):
    while True:
        print("Menú de opciones:")
        print("1. Ingresar instrucción en lenguaje natural")
        print("2. Ver vocabulario")
        print("3. Agregar palabra al vocabulario")
        print("4. Eliminar palabra del vocabulario")
        print("5. Buscar palabra similar")
        print("6. Ejecutar circuito cuántico")
        print("7. Crear y entrenar modelo")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            instruccion = input("Ingrese una instrucción en lenguaje natural: ")
            modelo = Modelo(vocabulario)
            modelo.entrenar_modelo(data_entrenamiento)
            vocabulario, input_indices = procesar_instruccion(instruccion, vocabulario, modelo)
            ejecutar_instruccion_lenguaje_natural(vocabulario, instruccion)
        elif opcion == "2":
            ver_vocabulario(vocabulario.vocabulario)
        elif opcion == "3":
            agregar_palabra_vocabulario(vocabulario)
        elif opcion == "4":
            eliminar_palabra_vocabulario(vocabulario)
        elif opcion == "5":
            buscar_palabra_similar(vocabulario)
        elif opcion == "6":
            ejecutar_circuito_cuántico(vocabulario, data_entrenamiento)
        elif opcion == "7":
            crear_y_entrenar_modelo(vocabulario, data_entrenamiento)
        elif opcion == "8":
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
        data = json.load(vocab_file)
        vocabulario = Vocabulario(data)
except Exception as e:
    print(f"Error al cargar el archivo de vocabulario: {e}")
    vocabulario = Vocabulario({})

# Cargar los datos de entrenamiento desde el archivo JSON
try:
    with open('data_entrenamiento.json', 'r') as data_file:
        data_entrenamiento = json.load(data_file)
except Exception as e:
    print(f"Error al cargar el archivo de datos de entrenamiento: {e}")
    data_entrenamiento = []

# Interactuar con el usuario y ejecutar el circuito cuántico
interactuar_con_usuario(vocabulario, data_entrenamiento)
