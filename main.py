#Importamos nuestras clases especializadas desde el módulo 'agentes.py'.
from mesa_redonda.agentes import AgenteArquitecto, AgenteProgramador

#Importamos nuestra clase 'Configuracion' desde el archivo 'configuracion.py' dentro de la carpeta 'mesa_redonda'
from mesa_redonda.configuracion import Configuracion

#Definimos una función principal 'main' para mantener el código ordenado y limpio.
def main()-> None:
    #Creamos una instacia (un objeto real) de la clase 'Configuracion'.
    config = Configuracion()
    #Llamamos al método 'preparar_entorno' para asegurarnos de que exista la carpeta de proyectos generados.
    config.preparar_entorno()

    #Instanciamos (creamos) nuestros dos primeros agentes especialistas usando las clases hijas.
    arquitecto = AgenteArquitecto(config)
    #Instaciamos al Programador pasándole la misma configuración.
    programador = AgenteProgramador(config)

    # Definimos la petición de prueba: tu aplicación real de recordatorio de pastas.
    peticion: str = (
        # Describimos la funcionalidad principal de la app en Windows 11 con Flet.
        "Crea una app de escritorio en Flet para Windows 11 que funcione como recordatorio de tomar pastas. "
        # Añadimos los requisitos de notificación flotante, intensidad según importancia, check obligatorio e historial.
        "Debe permitir programar horarios con nivel de importancia, mostrar una notificación flotante que no se cierre hasta marcar un check, y guardar el historial de tomas en SQLite."
    # Cerramos el texto de la petición.
    )

    # Paso 1: Le pedimos al Arquitecto que diseñe el plano estructurado en Pydantic.
    plan = arquitecto.disenar_arquitectura(peticion)

    # Imprimimos el resumen del plano que diseñó el Arquitecto para inspeccionarlo.
    print(f"\n PLAN DEL ARQUITECTO: {plan.nombre_proyecto}")
    # Mostramos el resumen técnico.
    print(f"Resumen: {plan.resumen_tecnico}")
    # Mostramos qué librerías externas detectó que hay que instalar con uv.
    print(f"Dependencias uv: {plan.dependencias_uv}")
    # Listamos uno por uno los archivos modulares que planeó crear.
    for archivo in plan.archivos:
        # Imprimimos la ruta, las clases POO y el propósito de cada archivo planeado.
        print(f"  - {archivo.ruta_relativa} | Clases: {archivo.clases_a_crear} | {archivo.proposito}")

    # Verificamos que el Arquitecto haya planeado al menos un archivo antes de pedirle al Programador que escriba.
    if len(plan.archivos) > 0:
        # Tomamos el primer archivo del plan (índice 0) para probar cómo el Programador lo convierte en código real.
        primer_archivo = plan.archivos[0]
        # Le pedimos al Programador que escriba exactamente ese primer archivo del plan.
        codigo_generado = programador.escribir_archivo(plan=plan, archivo=primer_archivo)

        # Mostramos en pantalla el archivo generado por 'qwen2.5-coder:7b'.
        print(f"\nCÓDIGO GENERADO PARA: {codigo_generado.ruta_relativa}")
        # Imprimimos el código Python puro que devolvió el objeto 'ArchivoCodigo'.
        print(codigo_generado.codigo_python)


#Este bloque estándar garantiza que 'main()' solo arranque si ejecutamos directamente 'main.py'.
if __name__ == "__main__":
    #Ejecutamos la función principal.
    main()
    