#Importamos 'Any' del módulo 'typing' para indicar que un diccionario puede contener tipo de dato adentro.
from typing import Any

#Importamos la librería oficial de 'ollama' para enviar mensajes a nuestros modelos locales.
import ollama

#Definimos la clase padre 'AgenteBase'; de ella heredarán después el Arquitecto, el Programador y el Tester.
class AgenteBase:
    #El constructor '__init__' recibe los datos necesarios para dar vida a cualquier agente nuevo.
    def __init__(self, nombre: str, rol: str, modelo:str, instrucciones_sistema: str)-> None:
        #Guardamos el nombre identificador del agente dentro del objeto usando 'self'.
        self.nombre: str = nombre
        #Guardamos el rol o especialidad del agente (ej. "Arquitecto de Software").
        self.rol: str = rol
        #Guardamos qué modelo de Ollama va a usar este agente para pensar.
        self.modelo: str = modelo
        #Guardamos las reglas de comportamiento (prompt de sistema) que definen la personalidad del agente.
        self.instrucciones_sistema: str = instrucciones_sistema
        #Inicializamos la memoria del agente como una lista que arranca con su mensaje de sistema.
        self.historial: list[dict[str, str]]=[
            #El primer elemento es un diccionario con rol 'system' y las instrucciones permanentes del agente.
            {"role": "system", "content": self.instrucciones_sistema},
            #Cerramos la lista inicial del historial.
        ]

    #Actualizamos 'pensar' para que acepte opcionalmente un 'formato_schema' (esquema JSON) o 'None' si es texto libre.
    def pensar(self, mensaje: str, formato_schema: dict[str, Any]| None = None)-> str:
        #Agregamos la nueva petición al historial del agente con el rol 'user'.
        self.historial.append({"role": "user", "content": mensaje}) 
        #Imprimimos un aviso en consola para saber qué agente y modelo están trabajando en este momento.
        print(f"\n[{self.nombre} ({self.modelo}) está pensando...]")

        # Configuramos temperatura, 'repeat_penalty: 1.15' y 'num_ctx: 16384' para que quepan varios archivos en contexto sin error 400.
        opciones_modelo: dict[str, Any] = (
            # Opciones para respuestas estructuradas en JSON.
            {"temperature": 0.1, "num_predict": 4096, "repeat_penalty": 1.15, "num_ctx": 16384}
            # Condición: si nos pasaron un esquema JSON estricto.
            if formato_schema
            # Para escritura de código o texto libre, mantenemos fluidez, penalización de repetición y 16K de memoria.
            else {"temperature": 0.2, "num_predict": 4096, "repeat_penalty": 1.15, "num_ctx": 16384}
        # Cerramos el diccionario de opciones.
        )

        #Usamos un bloque 'try' para intentar conectarnos a Ollama de forma segura sin que el programa explote si falla.
        try:
            # Llamamos a 'ollama.chat' enviando modelo, historial, formato, opciones y desactivando 'think' si no hay JSON.
            respuesta = ollama.chat(
                # Indicamos el nombre del modelo local que ejecutará la petición en tu RTX 4060.
                model=self.modelo,
                # Pasamos la lista completa de mensajes acumulados en 'self.historial'.
                messages=self.historial,
                # Pasamos el esquema JSON al parámetro 'format' para forzar la estructura de salida (o None si es libre).
                format=formato_schema,
                # Desactivamos el modo 'thinking' en escritura libre para poder usar 'qwen3.5:9b' rápido y sin respuestas vacías.
                think=False if formato_schema is None else None,
                # Pasamos las opciones de temperatura, límite de tokens y penalización de repetición.
                options=opciones_modelo,
            # Cerramos la llamada a la función 'ollama.chat'.
            )
            # Extraemos el texto de respuesta; usamos 'or ""' por seguridad en caso de que el campo llegue como None.
            texto_respuesta: str = respuesta.message.content or ""

            # Verificamos si el contenido llegó vacío (típico cuando un modelo "thinking" gasta todo en razonar).
            if not texto_respuesta.strip():
                # Intentamos leer si el modelo dejó su texto oculto en el atributo 'thinking' de Ollama.
                pensamiento_oculto: str = getattr(respuesta.message, "thinking", "") or ""
                # Imprimimos una alerta clara para diagnosticar fácilmente por qué vino vacío.
                print(f"[Alerta]: '{self.modelo}' devolvió contenido vacío. Pensamiento interno: {len(pensamiento_oculto)} caracteres.")

            # Guardamos la respuesta del modelo en el historial con el rol 'assistant' para que recuerde lo que dijo.
            self.historial.append({"role": "assistant", "content": texto_respuesta})
            #Devolvemos el texto generado para que quien llamó al agente pueda usarlo.
            return texto_respuesta

        #El bloque 'except' captura cualquier error de conexión (por ejemplo, si Ollama está cerrado o falta el modelo).
        except Exception as error:
            #Construimos un mensaje explicativo con el detalle técnico del error ocurrido.
            mensaje_error: str = f"Error al comunicar con Ollama({self.modelo}): {error}"
            #Imprimimos el error en pantalla para que podamos diagnosticarlo rápido.
            print(mensaje_error)
            #Devolvemos el mensaje de error en lugar de detener bruscamente la aplicación.
            return mensaje_error

    #Definimos un método extra para borrar la memoria de conversación si queremos que el agente empiece una tarea limpia.
    def reiniciar_memoria(self)-> None:
        #Volvemos a dejar el historial únicamente con el mensaje original de 'system'.
        self.historial = [{"role": "system", "content": self.instrucciones_sistema}]
