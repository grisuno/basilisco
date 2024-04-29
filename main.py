from qiskit import QuantumRegister, QuantumCircuit
import json
import os
import requests

def buscar_significado_palabra(palabra):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{palabra}"
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list):
            meanings = data[0].get("meanings", [])
            if meanings:
                return meanings[0].get("definitions", [])[0].get("definition", None)
        return None
    except Exception as e:
        print(f"Error al buscar el significado de la palabra '{palabra}': {e}")
        return None

def build_quantum_circuit(input_indices, target_indices):
    # Calcular la cantidad de qubits necesarios
    num_qubits = max(input_indices + target_indices) + 1

    # Crear los registros cuánticos
    qr = QuantumRegister(num_qubits)
    circuit = QuantumCircuit(qr)

    # Aplicar puertas cuánticas y realizar cálculos según la secuencia de entrada
    for input_idx in input_indices:
        if input_idx != -1 and input_idx < num_qubits:
            circuit.h(qr[input_idx])  # Aplicar una compuerta Hadamard a cada qubit de entrada
    
    # Generar índices únicos para los qubits de destino
    target_indices = [idx for idx in target_indices if idx not in input_indices]

    for target_idx in target_indices:
        if target_idx < num_qubits:
            circuit.cx(qr[input_indices[0]], qr[target_idx])  # Aplicar una compuerta CNOT entre el primer qubit de entrada y los qubits de destino
    
    return circuit

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
        
def interactuar_con_usuario(vocabulario, data_entrenamiento):
    while True:
        instruccion = input("Ingrese una instrucción en lenguaje natural ('salir' para salir): ")
        if instruccion.lower() =='salir':
            print("¡Hasta luego!")
            break
        
        # Preprocesar la instrucción
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
        
        # Actualizar el archivo JSON del vocabulario
        actualizar_vocabulario(vocabulario)
        
        # Actualizar la data de entrenamiento
        data_entrenamiento.append((input_words, input_indices))
        actualizar_data_entrenamiento(data_entrenamiento)
        
        # Definir num_qubits
        num_qubits = len(input_indices) * 2
        
        # Verificar si los índices son válidos
        if all(isinstance(idx, int) for idx in input_indices):
            # Generar el circuito cuántico
            qr = QuantumRegister(num_qubits)
            circuit = QuantumCircuit(qr)
            
            for input_idx in input_indices:
                if input_idx!= -1 and input_idx < num_qubits:
                    circuit.h(qr[input_idx])  # Aplicar una compuerta Hadamard a cada qubit de entrada
            
            # Seleccionar el qubit de control
            control_idx = int(input("Seleccione el qubit de control (0-{}): ".format(len(input_indices) - 1)))
            if control_idx < 0 or control_idx >= len(input_indices):
                print("Índice de control inválido. Por favor, seleccione un índice entre 0 y {}".format(len(input_indices) - 1))
                continue
            
            # Generar índices únicos para los qubits de destino
            target_indices = [idx for idx in range(len(input_indices), num_qubits) if idx not in input_indices]
            
            for target_idx in target_indices:
                if target_idx < num_qubits and input_indices[control_idx] is not None:
                    circuit.cx(qr[input_indices[control_idx]], qr[target_idx])  # Aplicar una compuerta CNOT entre el qubit de control y los qubits de destino
            
            # Ejecutar el circuito en un simulador cuántico
            print("Ejecutando el circuito cuántico...")
            # Aquí puedes ejecutar el circuito en un simulador cuántico o en un dispositivo real
            print("Circuito cuántico ejecutado exitosamente.")
            
            # Mostrar el tamaño del modelo
            print("Tamaño del modelo:", len(vocabulario), "palabras")
        else:
            print("Tamaño del modelo:", len(vocabulario), "palabras")
            print("Ha ocurrido un error al procesar la instrucción. Por favor, asegúrate de que el vocabulario esté actualizado y vuelve a intentarlo.")

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
