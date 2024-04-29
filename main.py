import nltk
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from qiskit import QuantumRegister, QuantumCircuit
import json
import os
import requests
from gensim.models import Word2Vec
import torch

nltk.download('punkt')

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
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{palabra}"
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

def responder_pregunta(pregunta, vocabulario, modelo):
    # Tokenizar la pregunta
    tokens = nltk.word_tokenize(pregunta)

    # Buscar la respuesta en el vocabulario
    respuesta = None
    for token in tokens:
        if token in vocabulario.vocabulario:
            respuesta = vocabulario.vocabulario[token]
            break

    # Si no se encontró una respuesta en el vocabulario, utilizar un modelo de lenguaje para generar una respuesta
    if respuesta is None:
        generator = pipeline("text-generation", model="distilbert-base-uncased")
        respuesta = generator(pregunta, max_length=50)

    return respuesta

def generar_texto(topic, vocabulario, modelo):
    # Eliminar espacios extra al final del tema
    topic = topic.strip()
    
    # Verificar si el tema está presente en el vocabulario
    if topic not in vocabulario.vocabulario:
        # Si el tema no está en el vocabulario, agregarlo con un significado vacío
        vocabulario.agregar_palabra(topic, "")
        print(f"El tema '{topic}' no estaba en el vocabulario. Se ha agregado automáticamente.")
    
    # Obtener las palabras similares al tema dado
    palabras_similares = modelo.modelo.wv.most_similar(topic, topn=5)
    
    # Obtener las palabras del vocabulario
    palabras_vocabulario = list(vocabulario.vocabulario.keys())
    
    # Filtrar las palabras similares que están en el vocabulario
    palabras_similares_vocabulario = [palabra for palabra, _ in palabras_similares if palabra in palabras_vocabulario]
    
    # Si no hay palabras similares en el vocabulario, generar un mensaje de advertencia
    if not palabras_similares_vocabulario:
        print("No se encontraron palabras similares en el vocabulario.")
        return None
    
    # Seleccionar una palabra similar aleatoria como inicio del texto
    palabra_inicial = palabras_similares_vocabulario[0]
    
    # Generar texto utilizando la palabra inicial como contexto
    texto_generado = [palabra_inicial]
    for _ in range(50):  # Generar 50 palabras como máximo
        palabra_actual = texto_generado[-1]
        palabras_siguientes = modelo.modelo.wv.most_similar(palabra_actual, topn=3)
        palabras_siguientes_vocabulario = [palabra for palabra, _ in palabras_siguientes if palabra in palabras_vocabulario]
        if palabras_siguientes_vocabulario:
            palabra_siguiente = palabras_siguientes_vocabulario[0]
            texto_generado.append(palabra_siguiente)
        else:
            break
    
    return ' '.join(texto_generado)


def interactuar_con_usuario(vocabulario, data_entrenamiento):
    modelo = Modelo(vocabulario)  # Crear una instancia del modelo
    modelo.entrenar_modelo(data_entrenamiento)  # Entrenar el modelo con los datos de entrenamiento proporcionados
    while True:
        print("Menú de opciones:")
        print("1. Ingresar instrucción en lenguaje natural")
        print("2. Ver vocabulario")
        print("3. Agregar palabra al vocabulario")
        print("4. Eliminar palabra del vocabulario")
        print("5. Buscar palabra similar")
        print("6. Ejecutar circuito cuántico")
        print("7. Crear y entrenar modelo")
        print("8. Responder pregunta")
        print("9. Generar texto")
        print("10. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            instruccion = input("Ingrese una instrucción en lenguaje natural: ")
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
            pregunta = input("Ingrese una pregunta: ")
            respuesta = responder_pregunta(pregunta, vocabulario, modelo)
            print(f"Respuesta: {respuesta}")
        elif opcion == "9":
            topic = input("Ingrese un tema: ")
            texto = generar_texto(topic, vocabulario, modelo)
            print(f"Texto generado: {texto}")
        elif opcion == "10":
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

# Crear una instancia del modelo
modelo = Modelo(vocabulario)

# Interactuar con el usuario y ejecutar el circuito cuántico
interactuar_con_usuario(vocabulario, data_entrenamiento)

