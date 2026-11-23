# Importamos 'Path' para devolver la ruta del proyecto creado.
from pathlib import Path

# Importamos 'ArchivoDiseno' para asegurar en Python que el plan siempre termine con 'main.py'.
from mesa_redonda.modelos_datos import ArchivoDiseno

# Importamos los 3 agentes especialistas desde 'agentes.py'.
from mesa_redonda.agentes import AgenteArquitecto, AgenteProgramador, AgenteTester

# Importamos la configuración central del sistema.
from mesa_redonda.configuracion import Configuracion

# Importamos nuestra nueva clase 'ConstructorModulo' encargada del ciclo de cada archivo.
from mesa_redonda.constructor_modulo import ConstructorModulo

# Importamos el ejecutor de pruebas para validar en Python real.
from mesa_redonda.ejecutor_pruebas import EjecutorPruebas

# Importamos el gestor de proyectos para crear carpetas e instalar dependencias.
from mesa_redonda.gestor_proyecto import GestorProyecto


# Definimos 'MesaRedonda', cuya única responsabilidad es coordinar el flujo general del proyecto.
class MesaRedonda:
    # El constructor instancia los agentes, la configuración y el constructor de módulos.
    def __init__(self, config: Configuracion) -> None:
        # Guardamos la configuración dentro del objeto.
        self.config: Configuracion = config
        # Creamos la carpeta 'proyectos_generados' si aún no existe.
        self.config.preparar_entorno()
        # Creamos al agente Arquitecto.
        self.arquitecto: AgenteArquitecto = AgenteArquitecto(config)
        # Creamos al 'ConstructorModulo' entregándole Programador, Tester y límite de intentos.
        self.constructor: ConstructorModulo = ConstructorModulo(AgenteProgramador(config), AgenteTester(config), config.max_intentos_correccion)

    # Método público que toma la idea del usuario y dirige toda la construcción paso a paso.
    def construir_proyecto(self, peticion_usuario: str) -> Path:
        # Limpiamos la memoria del Arquitecto e iniciamos el diseño modular.
        self.arquitecto.reiniciar_memoria()
        # El Arquitecto genera el plano estructurado en Pydantic.
        plan = self.arquitecto.disenar_arquitectura(peticion_usuario)

        # Si el Arquitecto olvidó incluir 'main.py' en el plan, lo agregamos automáticamente en Python.
        if not any(item.ruta_relativa.strip() in ("main", "main.py") for item in plan.archivos):
            # Añadimos 'main.py' al final del plan para garantizar que la aplicación siempre tenga punto de entrada.
            plan.archivos.append(ArchivoDiseno(ruta_relativa="main.py", proposito="Punto de entrada que conecta los módulos previos y arranca la aplicación.", clases_a_crear=[]))

        # Mostramos el título del plano diseñado.
        print(f"\n================ PLAN: {plan.nombre_proyecto} ================")
        # Listamos los archivos y clases planeadas.
        for item in plan.archivos:
            # Imprimimos cada módulo que se construirá.
            print(f"  * {item.ruta_relativa} -> Clases: {item.clases_a_crear}")

        # Inicializamos el gestor de proyecto (uv --no-workspace) en la carpeta de salida.
        gestor = GestorProyecto(self.config.carpeta_salida, plan.nombre_proyecto)
        # Mostramos en pantalla lo que instaló uv.
        print("\n" + gestor.inicializar_entorno(plan.dependencias_uv))
        # Creamos el ejecutor de pruebas apuntando a la carpeta del nuevo proyecto.
        ejecutor = EjecutorPruebas(gestor.ruta_proyecto)
        # Diccionario que almacenará cada módulo aprobado para dar contexto al siguiente.
        aprobados: dict[str, str] = {}

        # Recorremos cada archivo diseñado junto con su posición ('indice') usando 'enumerate'.
        for indice, archivo_plan in enumerate(plan.archivos):
            # Calculamos si este archivo es el último de la lista (donde normalmente va 'main.py').
            es_ultimo: bool = indice == len(plan.archivos) - 1
            # Delegamos al 'ConstructorModulo' la escritura, validación y auto-corrección de este archivo.
            codigo_final: str = self.constructor.construir(plan, archivo_plan, gestor, ejecutor, aprobados, es_ultimo)
            # Calculamos la clave normalizada exactamente igual que 'ConstructorModulo'.
            clave: str = self.constructor._normalizar_ruta(archivo_plan.ruta_relativa, es_ultimo)
            # Almacenamos el código aprobado para los módulos posteriores.
            aprobados[clave] = codigo_final

        # Imprimimos la confirmación final con la ruta donde quedó el proyecto.
        print(f"\n================ PROYECTO TERMINADO EN: {gestor.ruta_proyecto} ================")
        # Devolvemos la ruta de la carpeta creada.
        return gestor.ruta_proyecto