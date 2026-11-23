# Importamos 'subprocess' únicamente para capturar el error específico de tiempo excedido ('TimeoutExpired').
import subprocess

# Importamos 'Path' para recibir la ruta del proyecto a validar.
from pathlib import Path

# Importamos 'EjecutorComandos' para reutilizar la ejecución aislada sin duplicar código.
from mesa_redonda.ejecutor_comandos import EjecutorComandos


# Definimos 'EjecutorPruebas', cuya única responsabilidad es comprobar sintaxis e importaciones en Python real.
class EjecutorPruebas:
    # El constructor recibe la carpeta del proyecto generado.
    def __init__(self, ruta_proyecto: Path) -> None:
        # Creamos un objeto 'EjecutorComandos' apuntando a esa carpeta.
        self.comandos: EjecutorComandos = EjecutorComandos(ruta_proyecto)

    # Método público que valida sintaxis e importación de un archivo Python y devuelve (éxito, mensaje).
    def verificar_archivo(self, ruta_relativa: str) -> tuple[bool, str]:
        # Paso 1: Revisamos sintaxis con 'py_compile' (no abre ventanas gráficas ni ejecuta el programa).
        res_sintaxis = self.comandos.ejecutar(["uv", "run", "python", "-m", "py_compile", ruta_relativa])

        # Si el código de salida es distinto de 0, hay un error real de sintaxis.
        if res_sintaxis.returncode != 0:
            # Devolvemos False junto con el detalle del error.
            return False, f"Error de sintaxis detectado por Python:\n{res_sintaxis.stderr}"

        # Paso 2: Si no es 'main.py', probamos importar el módulo para verificar que todos sus 'import' funcionen.
        if ruta_relativa != "main.py" and ruta_relativa.endswith(".py"):
            # Convertimos 'carpeta/archivo.py' en 'carpeta.archivo'.
            modulo: str = ruta_relativa.removesuffix(".py").replace("/", ".").replace("\\", ".")
            # Usamos try/except para controlar si la importación supera el límite de tiempo.
            try:
                # Ejecutamos una importación rápida con límite de 15 segundos.
                res_import = self.comandos.ejecutar(["uv", "run", "python", "-c", f"import {modulo}"], tiempo_limite=15)
                # Si falló al importar, devolvemos False con el error exacto.
                if res_import.returncode != 0:
                    # Retornamos el fallo de importación para que el Tester lo analice.
                    return False, f"Error al importar '{modulo}':\n{res_import.stderr}"
            # Capturamos si el módulo se quedó bloqueado más de 15 segundos.
            except subprocess.TimeoutExpired:
                # Avisamos del exceso de tiempo sin colgar nuestro sistema.
                return False, f"El módulo '{modulo}' excedió el tiempo límite al importarse."

        # Si todo salió bien, devolvemos True con la confirmación.
        return True, f"Verificación en Python exitosa: '{ruta_relativa}' tiene sintaxis e importaciones válidas."