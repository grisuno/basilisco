# API

## main.py
- `Vocabulario.__init__` (method) `main.py:15` `def __init__(self, data)`
- `Vocabulario.cargar_vocabulario` (method) `main.py:18` `def cargar_vocabulario(self)`
- `Vocabulario.agregar_palabra` (method) `main.py:26` `def agregar_palabra(self, palabra, significado)`
- `Vocabulario.eliminar_palabra` (method) `main.py:30` `def eliminar_palabra(self, palabra)`
- `Vocabulario.guardar_vocabulario` (method) `main.py:35` `def guardar_vocabulario(self)`
- `Vocabulario.transformar_a_modelo` (method) `main.py:42` `def transformar_a_modelo(self)`
- `Modelo.__init__` (method) `main.py:48` `def __init__(self, vocabulario)`
- `Modelo.transformar_vocabulario_a_modelo` (method) `main.py:52` `def transformar_vocabulario_a_modelo(self)`
- `Modelo.entrenar_modelo` (method) `main.py:56` `def entrenar_modelo(self, data_entrenamiento)`
- `Modelo.buscar_significado_palabra` (method) `main.py:60` `def buscar_significado_palabra(palabra)`
- `Modelo.ver_vocabulario` (method) `main.py:78` `def ver_vocabulario(vocabulario)`
- `Modelo.agregar_palabra_vocabulario` (method) `main.py:83` `def agregar_palabra_vocabulario(vocabulario)`
- `Modelo.eliminar_palabra_vocabulario` (method) `main.py:88` `def eliminar_palabra_vocabulario(vocabulario)`
- `Modelo.buscar_palabra_similar` (method) `main.py:92` `def buscar_palabra_similar(vocabulario)`
- `Modelo.ejecutar_circuito_cuántico` (method) `main.py:100` `def ejecutar_circuito_cuántico(vocabulario, data_entrenamiento)`
- `Modelo.crear_y_entrenar_modelo` (method) `main.py:133` `def crear_y_entrenar_modelo(vocabulario, data_entrenamiento)`
- `Modelo.procesar_instruccion` (method) `main.py:138` `def procesar_instruccion(instruccion, vocabulario, modelo)`
- `Modelo.ejecutar_instruccion_lenguaje_natural` (method) `main.py:170` `def ejecutar_instruccion_lenguaje_natural(vocabulario, instruccion)`
- `Modelo.responder_pregunta` (method) `main.py:179` `def responder_pregunta(pregunta, vocabulario, modelo)`
- `Modelo.generar_texto` (method) `main.py:197` `def generar_texto(topic, vocabulario, modelo)`
- `Modelo.interactuar_con_usuario` (method) `main.py:239` `def interactuar_con_usuario(vocabulario, data_entrenamiento)`
