# Mesa Redonda de Código (Multi-Agente Local en POO)

Sistema multi-agente 100% local en Python construido con arquitectura modular, **Programación Orientada a Objetos (POO)**, **`uv`** y **Ollama**, donde tres agentes especializados (**Arquitecto**, **Programador** y **Tester**) colaboran, ejecutan pruebas reales en Python y se auto-corrigen automáticamente para construir proyectos desde cero.

---

## Hardware y Modelos Locales Utilizados

* **SO / Editor:** Windows 11 + VS Code
* **CPU / RAM:** Intel Core i9 (14ª gen) + 64 GB RAM
* **GPU:** NVIDIA RTX 4060 (8 GB VRAM)
* **Gestor de proyectos:** `uv` (entornos aislados por proyecto)
* **Modelos gratuitos en Ollama:**
  * `qwen2.5-coder:7b`: **Arquitecto** y **Tester** (respuestas estructuradas estrictas en JSON con Pydantic).
  * `qwen3.5:9b` (con `think=False`): **Programador** (escritura fluida de código Python moderno y POO).

---

## Arquitectura Modular (POO)

```text
mesa-redonda-codigo/
├── main.py                         # Punto de entrada minimalista
├── pyproject.toml                  # Dependencias del proyecto gestionadas con uv
└── mesa_redonda/                   # Paquete modular orientado a objetos
    ├── configuracion.py            # Clase Configuracion (modelos, límites y rutas)
    ├── modelos_datos.py            # Contratos estrictos con Pydantic (Plan, Archivo, Veredicto)
    ├── agente_base.py              # Clase padre AgenteBase (memoria, Ollama, num_ctx y think)
    ├── agentes.py                  # Clases hijas (AgenteArquitecto, AgenteProgramador, AgenteTester)
    ├── ejecutor_comandos.py        # Clase EjecutorComandos (subprocesos UTF-8 con entorno aislado)
    ├── gestor_proyecto.py          # Clase GestorProyecto (uv --no-workspace, filtros y limpieza)
    ├── ejecutor_pruebas.py         # Clase EjecutorPruebas (py_compile e import real con timeout)
    ├── constructor_modulo.py       # Clase ConstructorModulo (bucle de pruebas y auto-corrección)
    └── orquestador.py              # Clase MesaRedonda (coordinación general de los módulos)
```

### Principios de POO aplicados

* **Herencia:** `AgenteArquitecto`, `AgenteProgramador` y `AgenteTester` heredan memoria, manejo de errores y conexión a Ollama desde `AgenteBase`.
* **Composición:** `GestorProyecto` y `EjecutorPruebas` delegan la ejecución de terminal a `EjecutorComandos`; `MesaRedonda` delega la construcción por archivo a `ConstructorModulo`.
* **Responsabilidad Única:** Cada clase y módulo tiene un archivo pequeño y una única tarea clara.

---

## Hallazgos Técnicos Reales y Soluciones (Bitácora de Aprendizaje)

Durante la construcción y pruebas reales con LLMs locales de 7B–9B, se detectaron y resolvieron los siguientes retos de ingeniería:

1. **Conflicto de modelos *thinking* (`qwen3.5:9b`) con esquemas JSON (`format=`):**
   * *Hallazgo:* Al combinar `qwen3.5:9b` con `format=schema` de Pydantic, el modelo agotaba su turno en el campo oculto `thinking` y devolvía `message.content` vacío (`''`), provocando `ValidationError` en Pydantic.
   * *Solución:* Usar `qwen2.5-coder:7b` para los roles que exigen JSON estricto (`Arquitecto` y `Tester`), y usar `qwen3.5:9b` con `think=False` únicamente en el `Programador` (sin esquema JSON).

2. **Ventana de contexto insuficiente por defecto en Ollama (`status code: 400`):**
   * *Hallazgo:* Al acumular el código de varios módulos previos como contexto para el siguiente archivo, Ollama arrojó error `400` por superar su `num_ctx` por defecto (~2048–4096 tokens).
   * *Solución:* Configurar explícitamente `"num_ctx": 16384` en las opciones de `ollama.chat`, aprovechando cómodamente los 8 GB de VRAM de la RTX 4060.

3. **Bucles infinitos de repetición y generación de código dentro de JSON:**
   * *Hallazgo:* Pedir archivos largos de Python dentro de un campo JSON hizo que el modelo 7B entrara en bucles de repetición (`_tint_tint_tint...`) y cortara el JSON sin cerrarlo. Además, en ocasiones dejaba líneas sueltas de Markdown (```` ``` ````) dentro del `.py`.
   * *Solución:* Dejar al Programador generar código en bloque Markdown libre, añadir `"repeat_penalty": 1.15`, extraer el bloque con `re.search` y filtrar cualquier línea que empiece por ```` ``` ```` en `GestorProyecto`.

4. **Alucinaciones estructurales del Arquitecto (barandas deterministas en Python):**
   * *Hallazgo:* Los modelos pequeños a veces incluían librerías nativas de Python (como `sqlite3`) en `dependencias_uv`, proponían nombres con espacios para carpetas, u olvidaban incluir `main.py` al final del plan.
   * *Solución:* En lugar de depender solo del *prompt*, se implementaron barandas en Python: filtrado contra `sys.stdlib_module_names`, sanitización de rutas con expresiones regulares y adición automática de `main.py` si faltaba en el plan.

5. **Aislamiento de entornos virtuales con `uv` (`workspace` y `VIRTUAL_ENV`):**
   * *Hallazgo:* Al ejecutar `uv init` dentro de `proyectos_generados/`, `uv` detectaba el `pyproject.toml` padre y amarraba la app generada como miembro de un *workspace*. Además, heredaba la variable `VIRTUAL_ENV` del proyecto padre.
   * *Solución:* Usar `uv init --no-workspace --no-readme` y eliminar `VIRTUAL_ENV` de la copia de variables de entorno en `EjecutorComandos`.

6. **Validación técnica real vs. librerías UI recientes (`Flet 1.1.3`):**
   * *Hallazgo:* `py_compile` revisa sintaxis pero no detecta `NameError` ni `ImportError`, por lo que hubo que ejecutar `import <modulo>` (incluido `main.py` con timeout de 8s) para validar las importaciones reales. Adicionalmente, `Flet 1.1.3` cambió su API frente a Flet 0.x (`ft.run`, `ft.Button`, `ft.DropdownOption`, `page.show_dialog`), causando alucinaciones en modelos 7B–9B (`ElevatedButton`, `UserControl`, `ft.Modal`, herencia de `ft.Page`, o `=` dentro de `lambda`).
   * *Solución:* Reglas positivas explícitas de Flet 1.1+, prohibición explícita de asignaciones dentro de `lambda`, y validación humana final sobre la interfaz de la app generada (*App Recordatorio de Pastas* con ventana flotante `always_on_top`, intensidad sonora con `winsound` según prioridad, checkbox modal obligatorio e historial en SQLite).

---

## Instalación y Uso

```powershell
# Instalar dependencias del proyecto
uv sync

# Ejecutar la Mesa Redonda de Código
uv run main.py
```

*(Requiere tener [Ollama](https://ollama.com/) corriendo en local con los modelos `qwen2.5-coder:7b` y `qwen3.5:9b` descargados).*
