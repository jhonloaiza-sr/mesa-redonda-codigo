# Importamos 'os' para copiar y limpiar variables de entorno de Windows 11.
import os

# Importamos 'subprocess' para ejecutar comandos reales de terminal desde Python.
import subprocess

# Importamos 'Path' para recibir rutas de carpetas de forma segura.
from pathlib import Path


# Definimos la clase 'EjecutorComandos', cuya única responsabilidad es correr comandos aislados en terminal.
class EjecutorComandos:
    # El constructor recibe la carpeta donde se ejecutarán los comandos.
    def __init__(self, ruta_trabajo: Path) -> None:
        # Guardamos la carpeta de trabajo dentro del objeto.
        self.ruta_trabajo: Path = ruta_trabajo

    # Método privado que elimina 'VIRTUAL_ENV' para que uv use el entorno del proyecto generado y no el nuestro.
    def _entorno_aislado(self) -> dict[str, str]:
        # Copiamos las variables de entorno actuales de Windows 11.
        entorno: dict[str, str] = os.environ.copy()
        # Quitamos la referencia al entorno virtual padre si existe.
        entorno.pop("VIRTUAL_ENV", None)
        # Devolvemos el diccionario limpio.
        return entorno

    # Método público que ejecuta cualquier comando en la terminal con codificación UTF-8 y límite de tiempo.
    def ejecutar(self, comando: list[str], tiempo_limite: int = 60) -> subprocess.CompletedProcess[str]:
        # Llamamos a 'subprocess.run' devolviendo el objeto resultado completo (código, stdout y stderr).
        return subprocess.run(
            # Lista del comando y sus argumentos (ej. ['uv', 'init']).
            comando,
            # Carpeta donde se ejecuta el comando.
            cwd=self.ruta_trabajo,
            # Capturamos la salida estándar y de errores.
            capture_output=True,
            # Pedimos texto legible en lugar de bytes.
            text=True,
            # Forzamos UTF-8 para evitar fallos con tildes o símbolos en PowerShell de Windows 11.
            encoding="utf-8",
            # Reemplazamos cualquier byte extraño sin detener el programa.
            errors="replace",
            # Evitamos que un proceso se quede colgado indefinidamente.
            timeout=tiempo_limite,
            # Aplicamos el entorno aislado.
            env=self._entorno_aislado(),
        # Cerramos la llamada a 'subprocess.run'.
        )