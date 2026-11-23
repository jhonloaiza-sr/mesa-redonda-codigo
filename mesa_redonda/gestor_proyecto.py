# Importamos 're' para limpiar el nombre del proyecto y quitar caracteres inválidos.
import re

# Importamos 'sys' para consultar la lista oficial de módulos nativos de Python ('stdlib_module_names').
import sys

# Importamos 'Path' para manejar rutas de archivos y carpetas.
from pathlib import Path

# Importamos nuestra clase 'EjecutorComandos' (Composición en POO: GestorProyecto usa un EjecutorComandos).
from mesa_redonda.ejecutor_comandos import EjecutorComandos


# Definimos 'GestorProyecto', cuya única responsabilidad es crear la carpeta, inicializar uv y guardar archivos.
class GestorProyecto:
    # El constructor recibe la carpeta base ('proyectos_generados') y el nombre propuesto por el Arquitecto.
    def __init__(self, carpeta_base: Path, nombre_proyecto: str) -> None:
        # Limpiamos el nombre para quitar espacios, tildes o mayúsculas.
        nombre_limpio: str = self._limpiar_nombre(nombre_proyecto)
        # Guardamos la ruta completa del nuevo proyecto.
        self.ruta_proyecto: Path = carpeta_base / nombre_limpio
        # Creamos un objeto 'EjecutorComandos' propio para delegarle la ejecución de comandos uv.
        self.comandos: EjecutorComandos = EjecutorComandos(self.ruta_proyecto)

    # Método privado que transforma cualquier texto en un nombre válido con guiones bajos.
    def _limpiar_nombre(self, nombre: str) -> str:
        # Pasamos a minúsculas y quitamos espacios en los extremos.
        texto: str = nombre.strip().lower()
        # Reemplazamos todo lo que no sea letra o número por '_'.
        texto = re.sub(r"[^a-z0-9]+", "_", texto)
        # Quitamos guiones bajos sobrantes y damos un nombre por defecto si quedara vacío.
        return texto.strip("_") or "proyecto_ia"

    # Método público que crea la carpeta, inicializa un proyecto uv independiente e instala librerías reales.
    def inicializar_entorno(self, dependencias: list[str]) -> str:
        # Creamos la carpeta física del proyecto si aún no existe.
        self.ruta_proyecto.mkdir(parents=True, exist_ok=True)
        # Lista donde acumulamos el reporte de lo que hizo uv.
        registro: list[str] = []

        # Solo inicializamos si todavía no existe 'pyproject.toml' dentro del proyecto generado.
        if not (self.ruta_proyecto / "pyproject.toml").exists():
            # Usamos '--no-workspace' para que uv NO lo agregue al pyproject.toml de 'mesa-redonda-codigo'.
            res_init = self.comandos.ejecutar(["uv", "init", "--no-workspace", "--no-readme"])
            # Registramos el resultado de la inicialización.
            registro.append(f"uv init (código {res_init.returncode}): {res_init.stdout.strip() or res_init.stderr.strip()}")

        # Filtramos dependencias: descartamos vacías y módulos que ya vienen incluidos en Python (como 'sqlite3').
        externas: list[str] = [
            # Limpiamos espacios y pasamos a minúsculas.
            dep.strip().lower()
            # Recorremos la lista sugerida por el Arquitecto.
            for dep in dependencias
            # Solo conservamos paquetes que NO pertenezcan a la librería estándar de Python.
            if dep.strip() and dep.strip().lower() not in sys.stdlib_module_names
        # Cerramos la lista filtrada.
        ]

        # Si quedaron paquetes externos reales (por ejemplo 'flet'), los instalamos con uv.
        if externas:
            # Ejecutamos 'uv add' con las librerías externas filtradas.
            res_add = self.comandos.ejecutar(["uv", "add"] + externas)
            # Guardamos el resumen de instalación.
            registro.append(f"uv add {externas} (código {res_add.returncode}): {res_add.stderr.strip()}")
        # Si no había librerías externas, dejamos constancia sin ejecutar 'uv add'.
        else:
            # Mensaje informativo cuando el proyecto solo usa Python estándar.
            registro.append("Sin dependencias externas por instalar.")

        # Devolvemos el reporte completo unido por saltos de línea.
        return "\n".join(registro)

    # Método público que guarda en disco duro un archivo Python escrito por el Programador.
    def guardar_archivo(self, ruta_relativa: str, contenido: str) -> Path:
        # Quitamos barras al inicio para asegurar que la ruta sea relativa al proyecto.
        ruta_destino: Path = self.ruta_proyecto / Path(ruta_relativa.lstrip("/\\"))
        # Creamos subcarpetas intermedias si hicieran falta.
        ruta_destino.parent.mkdir(parents=True, exist_ok=True)
        # Limpiamos espacios al inicio y al final del código.
        codigo_limpio: str = contenido.strip()

        # Si el modelo incluyó bloques markdown ```python, los eliminamos automáticamente.
        if codigo_limpio.startswith("```"):
            # Dividimos el código en líneas individuales.
            lineas: list[str] = codigo_limpio.splitlines()
            # Quitamos la primera línea (```python) y la última si cierra con ```.
            codigo_limpio = "\n".join(lineas[1:-1] if lineas[-1].strip() == "```" else lineas[1:])

        # Guardamos el código en disco con codificación UTF-8.
        ruta_destino.write_text(codigo_limpio, encoding="utf-8")
        # Devolvemos la ruta donde quedó guardado.
        return ruta_destino