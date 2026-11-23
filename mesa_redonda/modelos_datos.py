#Importamos 'BaseModel' (la clase base de Pydantic para validar datos) y 'Field' (para describir cada campo al LLM).
from pydantic import BaseModel, Field

#Definimos el molde 'ArchivoDiseno', que representa un único archivo Python planeado por el Arquitecto.
class ArchivoDiseno(BaseModel):
    #Ruta donde vivirá el archivo dentro del proyecto generado (ej, "modelos.py" o "main.py").
    ruta_relativa : str = Field(
        #La descripción ayuda al LLM a entender exactamente qué formato de texto debe colocar aquí.
        description = "Ruta relativa del archivo Python a crear, por ejemplo 'gestor.py' o 'main.py'. Sin espacios.",
        # Cerramos la definición del campo 'ruta_relativa'.
    )
    #Explicación corta de la responsabilidad única que tendrá este módulo.
    proposito : str = Field(
        #Explicamos al modelo que debe describir claramente para qué sirve este archivo.
        description = "Responsabilidad principal de este archivo dentro de la arquitectura modular.",
        #Cerramos la definición del campo 'proposito'.
    )
    #Lista de nombres de las clases POO que el Programador deberá escribir dentro de este archivo.
    clases_a_crear : list[str] = Field(
        #Aclaramos que debe ser una lista de nombres en formato PascalCase (ej, ['Recortadorio', 'GestorPastas']).
        description = "Lista con los nombres de las clases POO que deben programarse en este archivo.",
        #Cerramos la definición del campo 'clases_a_crear'.
    )

#Definimos el molde 'PlanArquitectura', que es el plano completo que entrega el Agente Arquitecto.
class PlanArquitectura(BaseModel):
    #Nombre corto de la carpeta del proyecto (din tildes ni espacios).
    nombre_proyecto : str = Field(
        #Indicamos al modelo que use guiones bajos en lugar de espacios.
        description = "Nombre corto del proyecto en minúsculas y con guiones bajos, por ejemplo 'recordatorios_pastas'.",
        #Cerramos la definición del campo 'nombre_proyecto'.
    )
    #Resumen general de cómo se conectan las clases y módulos entre sí
    resumen_tecnico : str = Field(
        #Pedimos un resumen breve de cómo interactúan los objetos del sistema.
        description = "Explicación clara y breve de cómo se comunican los módulos y clases del proyecto."
        #Cerramos la definición del campo 'resumen_tecnico'.
    )
    #Lista de librerías externas necesarias para instalar con uv ( por ejemplo ['flet'] o [] si no usa externas).
    dependencias_uv : list[str] = Field(
        #Aclaramos que solo incluya paquetes reales instalables con pip/uv, no librerias nativa como sqlite3 o pathlib.
        description = "Lista de paquetes externos instalables con uv (ej, ['flet']). Lista vacía [] si solo usa Python estándar.",
        #Cerramos la definición del campo 'dependencias_uv'.
    )
    #Lista ordenada de los archivos que el Programador debe construir paso a paso.
    archivos : list[ArchivoDiseno] = Field(
        #Indicamos que los archivos base vayan primero y 'main.py' vaya al final.
        description = "Lista ordenada de módulos a crear. Los módulos base van primero y 'main.py' va al final.",
        #Cerramos la definición del campo 'archivos'.
    )

#Definimos el molde 'ArchivoCodigo', que obliga al Agente Programador a entregar código limpio y listo para guardar.
class ArchivoCodigo(BaseModel): 
    #Ruta del archivo que acaba de programar (debe coincidir con la que pidió el Arquitecto).
    ruta_relativa : str = Field(
        #Descripción para asegurar coherencia en el nombre del archivo.
        description = "Ruta relativa exacta del archivo generado.",
        #Cerramos la definición del campo 'ruta_relativa'.
    )
    #El código Python completo y comentado, sin adornos de Markdown.
    codigo_python : str = Field(
        #Instrucción clave para que no meta comillas triples de markdown dentro del string de código
        description = "Código fuente Python completo, funcional, en POO y comentado línea por línea. Sin bloques ```python."
        #Cerramos la definición del campo 'codigo_python'.
    )

#Definimos el molde 'ResultadoRevision', que usa el Agente Tester para aprobar o rechazar un código.
class ResultadoRevision(BaseModel):
    #Valor booleano (True o False) que indica si el código pasó la revisión y pruebas.
    aprobado : bool = Field(
        #Verdadero solo si no hay errores de sintaxis, ejecución ni fallos de lógica POO.
        description = "True si el código funciona correctamente y cumple los requisitos; False si tiene errores."
        #Cerramosla definición del campo 'aprobado'.
    )
    #Diagnóstico de los errores detectados (o confimación si todo salió bien).
    resumen_fallos : str = Field(
        #Pedimos puntualidad en el diagnóstico.
        description = "Descripción concreta de los errores encontrados, o 'Sin errores' si fue aprobado.",
        #Cerramos la definición del campo 'resumen_fallos'.
    )
    #Guia exacta de qué debe cambiar el Programador en el siguiente intento
    instrucciones_correccion: str = Field(
        #Si fue rechazada, aqui va la receta exacta para arreglarlo.
        description = "Pasos exactos para que el Programador corrija el archivo si aprobado es False.",
        #Cerramos la definición del campo 'instrucciones_correccion'.
    )