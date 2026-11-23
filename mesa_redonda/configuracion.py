# Importamos 'Path' de 'pathlib' para manejar rutas y carpetas de forma segura en Windows 11. 
from pathlib import Path

#Definimos la clase 'Configuracion', que actuará como el "panel de control" central de nuestro sistema.
class Configuracion:
    #El método especial '__init__' es el constructor: se ejecuta automáticamente al crear un objeto de esta clase.
    def __init__(self)-> None:
        #Guardamos el nombre del modelo que usará el Agente Arquitecto (bueno para planear y estructurar ideas).
        self.modelo_arquitecto: str = "qwen3.5:9b"
        #Guardamos el nombre del modelo que usará el Agente Programador (especialista en escribir código).
        self.modelo_programador: str = "qwen2.5-coder:7b"
        #Guardamos el nombre del modelo que usará el Agente Tester (encargado de revisar y validar resultados).
        self.modelo_tester: str = "qwen3.5:9b"
        #Definimos el número máximo de veces que el Programador puede intentar corregir un error antes de detenerse.
        self.max_intentos_correcion: int = 3
        #Definimos la carpeta donde los agentes guardarán los proyectos que construyan (por ejemplo, la app de pastas).
        self.carpeta_salida: Path = Path("proyectos_generados")

    #Definimos un método (una acción que sabe hacer este objeto) para crear la carpeta de salida si no existe aún.
    def preparar_entorno(self)-> None:
        #Usamos '.mkdir()' para crear la carpeta; 'exist_ok=True' evita errores si la carpeta ya habia sido creada antes.
        self.carpeta_salida.mkdir(parents=True, exist_ok=True)