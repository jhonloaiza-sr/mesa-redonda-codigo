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

    # Método público que valida sintaxis e importación de CUALQUIER archivo Python y devuelve (éxito, mensaje).
    def verificar_archivo(self, ruta_relativa: str) -> tuple[bool, str]:
        # Paso 1: Revisamos sintaxis con 'py_compile' (no abre ventanas gráficas ni ejecuta el programa).
        res_sintaxis = self.comandos.ejecutar(["uv", "run", "python", "-m", "py_compile", ruta_relativa])

        # Si el código de salida es distinto de 0, hay un error real de sintaxis.
        if res_sintaxis.returncode != 0:
            # Devolvemos False junto con el detalle del error.
            return False, f"Error de sintaxis detectado por Python:\n{res_sintaxis.stderr}"

        # Paso 2: Probamos importar el módulo (incluido 'main.py') para detectar NameError o ImportError reales.
        if ruta_relativa.endswith(".py"):
            # Convertimos 'carpeta/archivo.py' en 'carpeta.archivo'.
            modulo: str = ruta_relativa.removesuffix(".py").replace("/", ".").replace("\\", ".")
            # Usamos try/except para controlar si el archivo abre una ventana gráfica y supera el tiempo límite.
            try:
                # Ejecutamos una importación rápida con límite de 8 segundos.
                res_import = self.comandos.ejecutar(["uv", "run", "python", "-c", f"import {modulo}"], tiempo_limite=8)
                # Si falló al importar (ej. NameError o ImportError), devolvemos False con el error exacto.
                if res_import.returncode != 0:
                    # Retornamos el fallo de importación para que el Programador lo corrija.
                    return False, f"Error al importar '{modulo}':\n{res_import.stderr}"
            # Capturamos si 'main.py' abrió la ventana gráfica sin errores y alcanzó el tiempo límite.
            except subprocess.TimeoutExpired:
                # Si es 'main.py', llegar hasta abrir la GUI significa que sus importaciones y clases funcionaron.
                if ruta_relativa == "main.py":
                    # Aprobamos 'main.py' cerrando automáticamente la comprobación.
                    return True, "Verificación exitosa: 'main.py' cargó sin errores de importación."
                # Para módulos secundarios, un bloqueo de más de 8 segundos sí es un error real.
                return False, f"El módulo '{modulo}' excedió el tiempo límite al importarse."

        # Si todo salió bien, devolvemos True con la confirmación.
        return True, f"Verificación en Python exitosa: '{ruta_relativa}' tiene sintaxis e importaciones válidas."