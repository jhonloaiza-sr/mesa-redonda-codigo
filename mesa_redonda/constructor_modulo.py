# Importamos los agentes Programador y Tester desde 'agentes.py'.
from mesa_redonda.agentes import AgenteProgramador, AgenteTester

# Importamos el ejecutor de pruebas desde 'ejecutor_pruebas.py'.
from mesa_redonda.ejecutor_pruebas import EjecutorPruebas

# Importamos el gestor de proyectos desde 'gestor_proyecto.py'.
from mesa_redonda.gestor_proyecto import GestorProyecto

# Importamos los moldes de diseño desde 'modelos_datos.py'.
from mesa_redonda.modelos_datos import ArchivoDiseno, PlanArquitectura


# Definimos 'ConstructorModulo', cuya única responsabilidad es programar, probar y corregir un solo archivo.
class ConstructorModulo:
    # El constructor recibe al Programador, al Tester y el límite máximo de intentos.
    def __init__(self, programador: AgenteProgramador, tester: AgenteTester, max_intentos: int) -> None:
        # Guardamos la instancia del Programador, del Tester y el límite de reintentos.
        self.programador, self.tester, self.max_intentos = programador, tester, max_intentos

    # Método privado que garantiza un nombre de archivo válido con '.py' (rescatando si llegó vacío).
    def _normalizar_ruta(self, ruta: str, es_ultimo: bool = False) -> str:
        # Quitamos espacios en blanco del nombre recibido.
        limpia: str = ruta.strip()
        # Si el Arquitecto dejó el nombre vacío, asignamos 'main.py' al último archivo o un nombre seguro.
        if not limpia:
            # Devolvemos 'main.py' si es el último módulo, o 'modulo_extra.py' en otro caso.
            return "main.py" if es_ultimo else "modulo_extra.py"
        # Si ya termina en '.py' la deja igual; si no, le añade '.py'.
        return limpia if limpia.endswith(".py") else f"{limpia}.py"

    # Método privado que une el código de módulos ya aprobados en un solo texto de referencia.
    def _formatear_contexto(self, aprobados: dict[str, str]) -> str:
        # Si aún no hay archivos aprobados devolvemos vacío; si hay, los unimos claramente.
        return "" if not aprobados else "\n\n".join(f"--- Archivo existente: {n} ---\n{c}" for n, c in aprobados.items())

    # Método público que ejecuta el ciclo de escritura, prueba real en Python y revisión QA para un archivo.
    def construir(self, plan: PlanArquitectura, archivo: ArchivoDiseno, gestor: GestorProyecto, ejecutor: EjecutorPruebas, aprobados: dict[str, str], es_ultimo: bool = False) -> str:
        # Normalizamos el nombre del archivo actual evitando nombres vacíos como '.py'.
        ruta: str = self._normalizar_ruta(archivo.ruta_relativa, es_ultimo)
        # Variables para acumular errores previos y conservar el último código escrito.
        errores, ultimo_codigo = "", ""
        # Preparamos el contexto de módulos previos ya aprobados.
        contexto: str = self._formatear_contexto(aprobados)

        # Iteramos desde el intento 1 hasta alcanzar 'self.max_intentos'.
        for intento in range(1, self.max_intentos + 1):
            # Mostramos el progreso actual en consola.
            print(f"\n>>> Construyendo '{ruta}' (Intento {intento}/{self.max_intentos}) <<<")
            # Limpiamos memoria del Programador para evitar ruido de archivos anteriores.
            self.programador.reiniciar_memoria()
            # Pedimos al Programador que escriba el archivo y guardamos su texto en una variable.
            ultimo_codigo = self.programador.escribir_archivo(plan, archivo, contexto, errores).codigo_python
            # Guardamos físicamente el archivo en la carpeta del nuevo proyecto.
            gestor.guardar_archivo(ruta, ultimo_codigo)

            # Ejecutamos la validación real de sintaxis e importación en Python.
            paso_python, salida_python = ejecutor.verificar_archivo(ruta)
            # Mostramos la salida real de Python en consola.
            print(f"[Python real]: {salida_python}")

            # Limpiamos la memoria del Tester para hacer una revisión fresca e imparcial.
            self.tester.reiniciar_memoria()
            # Protegemos la llamada al Tester con try/except por si el modelo falla al emitir el JSON.
            try:
                # El Tester evalúa el código junto con la evidencia real de consola.
                veredicto = self.tester.revisar_codigo(ruta, ultimo_codigo, salida_python)
                # Imprimimos el veredicto resumido y verificamos si pasó Python Y el Tester.
                print(f"[Veredicto Tester]: Aprobado={veredicto.aprobado} | {veredicto.resumen_fallos}")
                # Solo retornamos si Python real pasó Y el Tester dio su aprobación.
                if paso_python and veredicto.aprobado:
                    # Devolvemos el código definitivo aprobado.
                    return ultimo_codigo
                # Preparamos instrucciones para corregir en el siguiente intento.
                errores = f"Salida Python:\n{salida_python}\n\nQA:\n{veredicto.resumen_fallos}\nCorrección:\n{veredicto.instrucciones_correccion}"
            # Si el Tester falló al responder JSON, usamos solo el resultado real de Python para decidir.
            except Exception as err:
                # Avisamos del fallo del Tester sin tumbar la ejecución.
                print(f"[Aviso Tester]: Error leyendo veredicto ({err}).")
                # Si al menos Python real pasó, damos por bueno el archivo; si no, reintentamos con el error de Python.
                if paso_python:
                    # Retornamos el código que sí pasó la validación técnica de Python.
                    return ultimo_codigo
                # Guardamos la salida de error de Python para que el Programador lo arregle.
                errores = f"Salida Python:\n{salida_python}"

        # Si se agotaron los intentos, avisamos en pantalla y conservamos el último código escrito.
        print(f"[Aviso]: '{ruta}' alcanzó el máximo de intentos.")
        # Devolvemos la última versión generada.
        return ultimo_codigo