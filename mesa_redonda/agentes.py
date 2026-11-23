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
        #Definimos las reglas del Programador: POO limpia, tipado y comentarios en cada línea.
        reglas : str = (
            #Le ordenamos programar estrictamente con clases y métodos en Python moderno.
            "Eres un Programador Senior de Python experto en Programación Orientada a Objetos (POO)."
            #Le exigimos buenas practica: tipado, manejo de errores y código comentado línea por línea en español.
            "Escribe código limpio, modular, con anotaciones de tipo y comentarios breves en español explicando cada línea."
            #Le recordamos nunca envolver el código en comillas triples markdown dentro del JSON.
            "Entrega únicamente código Python válido y completo dentro del campo solicitado."
            #Cerramos las reglas.
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
            f"Clases requeridas: {','.join(archivo.clases_a_crear)}"
            #Añadimos el código previo (si existe).
            f"{bloque_contexto}"
            #Añadimos los errores a corregir (si existen)
            f"{bloque_errores}"
            #Cerramos el prompt.
        )

        # Llamamos a '.pensar()' forzando el esquema JSON de 'ArchivoCodigo'.
        respuesta_json: str = self.pensar(
            # Enviamos el prompt.
            mensaje=prompt,
            # Forzamos que devuelva exactamente 'ruta_relativa' y 'codigo_python'.
            formato_schema=ArchivoCodigo.model_json_schema(),
        # Cerramos la llamada a '.pensar()'.
        )
        # Validamos el JSON recibido y devolvemos el objeto 'ArchivoCodigo'.
        return ArchivoCodigo.model_validate_json(respuesta_json)

# Definimos 'AgenteTester' heredando también de 'AgenteBase'.
class AgenteTester(AgenteBase):
    # El constructor recibe 'config' para asignar el modelo evaluador.
    def __init__(self, config: Configuracion) -> None:
        # Definimos las reglas del Tester: ser exigente con sintaxis, importaciones y POO.
        reglas: str = (
            # Le damos el papel de revisor técnico estricto.
            "Eres un Ingeniero QA (Quality Assurance) experto en Python y POO. "
            # Le explicamos que debe analizar el código y la salida real de ejecución para decidir si pasa o falla.
            "Analiza si el código tiene errores de sintaxis, importaciones rotas, fallos lógicos o incumple la POO. "
            # Le pedimos ser objetivo y dar instrucciones claras en español si algo falla.
            "Sé estricto pero constructivo, respondiendo siempre en español bajo el esquema JSON pedido."
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