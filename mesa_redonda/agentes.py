#Importamos la clase padre 'AgenteBase' desde el archivo vecino 'agente_base.py'.
from mesa_redonda.agente_base import AgenteBase

#Importamos nuestra clase 'Configuracion' para saber qué modelo le corresponde a cada especialista.
from mesa_redonda.configuracion import Configuracion

#Importamos nuestros 4 moldes estrictos de Pydantic desde 'modelos_datos.py'.
from mesa_redonda.modelos_datos import (
    #Molde de diseño por archivo.
    ArchivoDiseno,
    #Molde de código generado.
    ArchivoCodigo,
    #Molde del plano general del proyecto.
    PlanArquitectura,
    #Molde del veredicto del Tester.
    ResultadoRevision,
    #Cerramos la importación múltiple.
)

#Definimos 'AgenteArquitecto' heredando todas las capacidades de 'AgenteBase'.
class AgenteArquitecto(AgenteBase):
    #El constructor solo pide el objeto 'config' para tomar su modelo asignado.
    def __init__ (self, config: Configuracion)-> None:
        #Definimos las instrucciones permanentes del Arquitecto enfocadas en modularidad, POO y realismo
        reglas : str = (
            #Le indicamos su rol y que diseñe siempre en archivos pequeños y POO.
            "Eres un Arquitecto de Software Senior experto en Python, arquitectura modular y Programación Orientada a Objetos (POO)."
            #Le pedimo que divida cualquier proyecto en maximo 3 o 4 archivos claros para mantenerlo simple y mantenible.
            "Divide siempre los proyectos en 3 o 4 módulos pequeños con clases bien definidas, terminando en 'main.py'."
            #Le recordamos responder estrictamente en el esquema JSON  solicitado y en español.
            "Responde siempre en español respetando estrictamente la estructura JSON  pedida."
            #Cerramos el texto de reglas.
        )
        #'super().__init__' llama al constructor de la clase padre 'AgenteBase' para configurar nombre, rol, modelo y memoria.
        super().__init__(
            #Nombre visible del agente.
            nombre = "Arquitecto",
            #Rol descriptivo.
            rol = "Diseño Modular y POO",
            #Modelo tomado desde nuestra configuración central.
            modelo = config.modelo_arquitecto,
            #Reglas definidas arriba.
            instrucciones_sistema = reglas,
            #Cerramos la llamada al constructor padre.
        )

    #Método propio del Arquitecto: recibe la idea del usuario y devuelve un objeto validado 'PlanArquitectura'.
    def disenar_arquitectura(self, peticion_usuario: str)-> PlanArquitectura:
        #Construimos un prompt claro que incluye el recordatorio de lo que necesitamos diseñar.
        prompt : str = (
            #Pasamos la petición original del usuario
            f"Diseña la arquitectura modular en Python con POO para el siguiente proyecto: \n'{peticion_usuario}'\n\n"
            #Reforzamos que use dependencias reales y mantenga los módulos simples y bien separados.
            "Asegúrate de listar en orden los archivos a crear (el último debe ser 'main.py') y las clases exacts de cada archivo."
            #Cerramos el texto del prompot.
        )
        #Llamamos al método '.pensar()' heredado de 'AgenteBase', pasandole el esquema JSON generado por Pydantic.
        respuesta_json : str = self.pensar(
            #Enviamos el prompt construido.
            mensaje = prompt,
            #Convertimos la clase 'PlanArquitectura' en un esquema JSON que Ollama usara como camisa de fuerza.
            formato_schema = PlanArquitectura.model_json_schema(),
            #Cerramos la llamada a '.pensar()'.
        )
        #Validamos el texto JSON devuelto por el modelo y lo transfomarmos en un objeto Python 'PlanArquitectura' real.
        return PlanArquitectura.model_validate_json(respuesta_json)

#Definimos 'AgenteProgramador' heredando tambien de 'AgenteBase'.
class AgenteProgramador(AgenteBase):
    #El constructor recibe 'config' para usar el modelo especialista en código.
    def __init__(self, config: Configuracion)-> None:
        # Definimos las reglas del Programador: POO limpia, importaciones completas y prohibición de '=' en lambdas.
        reglas: str = (
            # Le ordenamos programar estrictamente con clases y métodos en Python moderno.
            "Eres un Programador Senior de Python experto en Programación Orientada a Objetos (POO). "
            # Exigimos importar todo, no ejecutar código fuera de 'main.py' y jamás asignar '=' dentro de un 'lambda'.
            "Importa siempre arriba todas las clases de otros módulos que uses (ej. 'from modelos import ...'), tipos como 'Optional' o 'datetime', NUNCA pongas '=' dentro de una función 'lambda' (usa métodos 'def' normales para botones 'on_click'), y NUNCA llames a 'ft.app'/'ft.run' fuera de 'main.py'. "
            # Le pedimos responder únicamente con el bloque de código Python para extraerlo sin errores de JSON.
            "Responde ÚNICAMENTE con el código Python completo dentro de un bloque ```python ... ``` sin explicaciones extra."
        # Cerramos las reglas.
        )
        #Inicializamos la clase padre 'AgenteBase' con los datos del Progranador.
        super().__init__(
            #Nombre visible del agente.
            nombre = "Programador",
            #Rol descriptivo.
            rol = "Implementación POO en Python",
            #Modelo especialista en código (qwen2.5-coder: 7b).
            modelo = config.modelo_programador,
            #Reglas definidas arriba.
            instrucciones_sistema =reglas,
            #Cerramos la llamada a 'super().__init__'.
        )

    #Método propio del Programador: escribe un archivo especifico del plan, conociendo los archivos ya escritos.
    def escribir_archivo(
            #Referencia al objeto mismo.
            self,
            #El plano completo creado por el Arquitecto
            plan : PlanArquitectura,
            #El archivo puntual que toca programar ahora.
            archivo : ArchivoDiseno,
            #Texto opcional con el codigo de módulos anteriores para que las importaciones coincidan exactamente.
            contexto_codigo : str = "",
            #Texto opcional con errores reportados por el Tester si estamos en un intento de correccion.
            errores_previos : str = "",
            #Indicamos que este método devuelve un objeto validado 'ArchivoCodigo'.
    )-> ArchivoCodigo:
        #Preparamos una sección de contexto si ya existen otros archivos programados antes que este.
        bloque_contexto : str = (
            #Si hay contexto previo, lo incluimos para que el Programador vea los nombres reales de clases y métodos.
            f"\n\nCódigo de los módulos ya creados (úsalos para hacer los 'import' exactos): \n{contexto_codigo}"
            #Condición: solo si 'contexto_codigo' no está vacío.
            if contexto_codigo
            #Si esta vacio, no agregamos nada extra.
            else ""
            #Cerramos la expresion del bloque de contexto.            
        )
        #Preperamos una sección de errores si el Tester rechazo la versión anterior de este archivo.
        bloque_errores : str = (
            #Le mostramos al Programador exactamente que fallo para que lo corrija.
            f"\n\nATENCIÓN _ Corrige los siguientes errores detectados previamente: \n{errores_previos}"
            #Condición: solo si 'errores_previos' contiene texto.
            if errores_previos
            #Si no hubo errores previos, queda vacio.
            else ""
            #Cerramos la expresión del bloque de errores.
        )

        # Verificamos si este archivo específico realmente pertenece a la interfaz gráfica o es 'main.py'.
        es_archivo_ui: bool = any(palabra in f"{archivo.ruta_relativa} {archivo.proposito}".lower() for palabra in ("vista", "interfaz", "ventana", "ui", "flet", "main"))
        # Si el proyecto usa Flet Y este módulo trata sobre la interfaz gráfica, damos instrucciones exactas de Flet 1.1+.
        bloque_flet: str = (
            # Ordenamos usar 'import flet as ft', definir vistas SIN herencia y usar 'ft.AlertDialog' en vez de 'ft.Modal'.
            "\n\nREGLAS FLET 1.1+: Usa siempre 'import flet as ft' (NO uses 'from flet import ...'). Define TODAS las clases de vista SIN herencia (ej: 'class VentanaPrincipal:') recibiendo 'page: ft.Page'. Para alertas usa 'ft.AlertDialog' (NO existe ft.Modal). Usa 'ft.run(main)', 'ft.Button', 'ft.Icons' y 'ft.Colors'."
            # Condición: solo si 'flet' está en dependencias Y este archivo sí es de interfaz o 'main.py'.
            if any("flet" in dep.lower() for dep in plan.dependencias_uv) and es_archivo_ui
            # Si es un archivo de lógica/datos (como modelos o controladores), no metemos reglas de Flet para no confundirlo.
            else ""
        # Cerramos el bloque de reglas Flet.
        )

        #Armamos la orden completa para programar exactamente el archivo actual.
        prompt : str = (
            #Contexto general del proyecto.
            f"Proyecto: {plan.nombre_proyecto}\n"
            #Resumen técnico diseñado por el Arquitecto.
            f"Arquitectura: {plan.resumen_tecnico}\n"
            #Archivo especifico a escribir en este turno.
            f"Archivo a programar ahora: '{archivo.ruta_relativa}'\n"
            #Que debe hacer este archivo.
            f"Propósito: {archivo.proposito}\n"
            #Que clases POO debe contener obligatoriamente.
            f"Clases requeridas: {','.join(archivo.clases_a_crear)}\n"
            # Recordamos explícitamente importar las clases de módulos anteriores para evitar NameError.
            "Regla: si usas clases de archivos anteriores, impórtalas arriba (ej. 'from modelos import Recordatorio')."
            #Añadimos el código previo (si existe).
            f"{bloque_contexto}"
            #Añadimos los errores a corregir (si existen)
            f"{bloque_errores}"
            # Añadimos reglas de Flet 1.1+ si este proyecto usa Flet.
            f"{bloque_flet}"
            #Cerramos el prompt.
        )

        # Llamamos a '.pensar()' sin esquema JSON para que el modelo escriba Python fluido sin romper comillas.
        respuesta_codigo: str = self.pensar(mensaje=prompt)
        # Empaquetamos la respuesta en 'ArchivoCodigo' para respetar el tipo de retorno esperado por el sistema.
        return ArchivoCodigo(ruta_relativa=archivo.ruta_relativa, codigo_python=respuesta_codigo)

# Definimos 'AgenteTester' heredando también de 'AgenteBase'.
class AgenteTester(AgenteBase):
    # El constructor recibe 'config' para asignar el modelo evaluador.
    def __init__(self, config: Configuracion) -> None:
        # Definimos las reglas del Tester: justo, práctico y certero con errores de importación y lambdas.
        reglas: str = (
            # Le damos el papel de revisor técnico práctico.
            "Eres un Ingeniero QA práctico experto en Python y POO. "
            # Le enseñamos a aprobar cuando Python pasa, y dar diagnóstico real en NameError y lambda con '='.
            "Si la verificación real en Python fue exitosa, APRUEBA el archivo (aprobado=true) salvo fallo grave; no rechaces 'main.py' solo por usar una función. Si Python da NameError, indica qué 'import' agregar arriba. Si Python da SyntaxError en un 'lambda' con '=', indica reemplazar el 'lambda' por un método 'def' normal."
        # Cerramos las reglas.
        )
        # Llamamos al constructor de la clase padre 'AgenteBase'.
        super().__init__(
            # Nombre visible del agente.
            nombre="Tester",
            # Rol descriptivo.
            rol="Revisión y Pruebas de Código",
            # Modelo asignado desde configuración.
            modelo=config.modelo_tester,
            # Reglas definidas arriba.
            instrucciones_sistema=reglas,
        # Cerramos la llamada a 'super().__init__'.
        )

    # Método propio del Tester: evalúa un archivo junto con el resultado real de haberlo probado en Python.
    def revisar_codigo(self, ruta_archivo: str, codigo: str, salida_consola: str) -> ResultadoRevision:
        # Armamos el reporte de inspección para que el Tester emita su veredicto.
        prompt: str = (
            # Indicamos qué archivo se está revisando.
            f"Archivo revisado: '{ruta_archivo}'\n\n"
            # Mostramos el código fuente que escribió el Programador.
            f"Código fuente:\n{codigo}\n\n"
            # Mostramos lo que respondió Python al intentar validar/ejecutar este archivo.
            f"Resultado real de verificación en consola:\n{salida_consola}\n\n"
            # Pedimos el veredicto final estructurado.
            "Indica si está aprobado o si requiere correcciones."
        # Cerramos el prompt.
        )
        # Llamamos a '.pensar()' forzando el esquema JSON de 'ResultadoRevision'.
        respuesta_json: str = self.pensar(
            # Enviamos el prompt.
            mensaje=prompt,
            # Forzamos el molde 'ResultadoRevision'.
            formato_schema=ResultadoRevision.model_json_schema(),
        # Cerramos la llamada a '.pensar()'.
        )
        # Validamos y devolvemos el objeto 'ResultadoRevision'.
        return ResultadoRevision.model_validate_json(respuesta_json)