# Importamos nuestras tres clases de agentes especializados desde 'agentes.py'.
from mesa_redonda.agentes import AgenteArquitecto, AgenteProgramador, AgenteTester

# Importamos nuestra clase 'Configuracion' desde 'configuracion.py'.
from mesa_redonda.configuracion import Configuracion

# Importamos 'EjecutorPruebas' desde su propio módulo dedicado.
from mesa_redonda.ejecutor_pruebas import EjecutorPruebas

# Importamos 'GestorProyecto' desde su propio módulo dedicado.
from mesa_redonda.gestor_proyecto import GestorProyecto


# Definimos la función principal que prueba toda la línea de producción con el primer archivo.
def main() -> None:
    # Creamos la configuración central del sistema.
    config = Configuracion()
    # Aseguramos que exista la carpeta padre 'proyectos_generados'.
    config.preparar_entorno()

    # Instanciamos a los 3 miembros de nuestra Mesa Redonda de Código.
    arquitecto = AgenteArquitecto(config)
    # Instanciamos al Programador.
    programador = AgenteProgramador(config)
    # Instanciamos al Tester.
    tester = AgenteTester(config)

    # Definimos la petición de prueba: tu aplicación de recordatorio de pastas.
    peticion: str = (
        # Describimos la funcionalidad principal en Windows 11 con Flet.
        "Crea una app de escritorio en Flet para Windows 11 que funcione como recordatorio de tomar pastas. "
        # Añadimos los requisitos de notificación flotante, intensidad según importancia, check obligatorio e historial.
        "Debe permitir programar horarios con nivel de importancia, mostrar una notificación flotante que no se cierre hasta marcar un check, y guardar el historial de tomas en SQLite."
    # Cerramos el texto de la petición.
    )

    # Paso 1: El Arquitecto diseña la arquitectura modular del proyecto.
    plan = arquitecto.disenar_arquitectura(peticion)
    # Imprimimos el nombre y las dependencias originales que propuso el Arquitecto.
    print(f"\n=== PLAN: {plan.nombre_proyecto} | Dependencias sugeridas: {plan.dependencias_uv} ===")

    # Paso 2: Creamos el 'GestorProyecto' que limpia el nombre de la carpeta y prepara el entorno con uv.
    gestor = GestorProyecto(carpeta_base=config.carpeta_salida, nombre_proyecto=plan.nombre_proyecto)
    # Inicializamos el nuevo proyecto con uv e instalamos únicamente las dependencias externas reales (filtrando 'sqlite3').
    log_entorno = gestor.inicializar_entorno(plan.dependencias_uv)
    # Imprimimos en qué carpeta física quedó el proyecto y qué instaló uv.
    print(f"\n=== ENTORNO CREADO EN: {gestor.ruta_proyecto} ===")
    # Mostramos el resumen de lo que hicieron 'uv init' y 'uv add'.
    print(log_entorno)

    # Paso 3: Verificamos que el plan tenga archivos por construir.
    if len(plan.archivos) > 0:
        # Tomamos el primer módulo del plan (usualmente el de modelos de datos).
        primer_archivo = plan.archivos[0]
        # El Programador genera el código POO para ese primer archivo.
        codigo_generado = programador.escribir_archivo(plan=plan, archivo=primer_archivo)
        # Guardamos ese código en un archivo real dentro de la carpeta del proyecto nuevo.
        ruta_guardada = gestor.guardar_archivo(
            # Indicamos la ruta relativa elegida por el Arquitecto.
            ruta_relativa=codigo_generado.ruta_relativa,
            # Pasamos el código Python generado.
            contenido=codigo_generado.codigo_python,
        # Cerramos la llamada a 'guardar_archivo'.
        )
        # Avisamos por consola dónde se guardó el archivo real.
        print(f"\n[Archivo guardado en disco]: {ruta_guardada}")

        # Paso 4: Creamos el 'EjecutorPruebas' apuntando a la carpeta del nuevo proyecto.
        ejecutor = EjecutorPruebas(ruta_proyecto=gestor.ruta_proyecto)
        # Ejecutamos la verificación real de sintaxis e importación en Python sobre el archivo guardado.
        paso_tecnico, salida_consola = ejecutor.verificar_archivo(codigo_generado.ruta_relativa)
        # Imprimimos lo que respondió Python al probar ese archivo real.
        print(f"\n[Resultado Python real (Éxito={paso_tecnico})]: {salida_consola}")

        # Paso 5: El 'AgenteTester' analiza el código junto con la salida real de Python y da su veredicto.
        veredicto = tester.revisar_codigo(
            # Le decimos qué archivo está revisando.
            ruta_archivo=codigo_generado.ruta_relativa,
            # Le pasamos el código exacto que se guardó.
            codigo=codigo_generado.codigo_python,
            # Le entregamos la evidencia real de la terminal.
            salida_consola=salida_consola,
        # Cerramos la llamada a 'revisar_codigo'.
        )

        # Mostramos en pantalla el veredicto estructurado del AgenteTester.
        print("\n=== VEREDICTO DEL TESTER ===")
        # Imprimimos si aprobó o rechazó el archivo.
        print(f"Aprobado: {veredicto.aprobado}")
        # Imprimimos el resumen de fallos o confirmación.
        print(f"Resumen: {veredicto.resumen_fallos}")
        # Imprimimos las instrucciones de corrección si las hubo.
        print(f"Correcciones: {veredicto.instrucciones_correccion}")


# Bloque estándar que arranca la función principal al ejecutar este archivo.
if __name__ == "__main__":
    # Llamamos a 'main()'.
    main()