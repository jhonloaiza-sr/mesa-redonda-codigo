# Importamos nuestra clase 'Configuracion' desde el módulo 'configuracion.py'.
from mesa_redonda.configuracion import Configuracion

# Importamos nuestra clase directora 'MesaRedonda' desde el módulo 'orquestador.py'.
from mesa_redonda.orquestador import MesaRedonda


# Definimos la función principal de entrada de toda la aplicación.
def main() -> None:
    # Creamos la configuración central del sistema.
    config = Configuracion()
    # Creamos el objeto director 'MesaRedonda' pasándole la configuración.
    mesa = MesaRedonda(config)

    # Definimos nuestra petición por defecto (la app de pastas con pistas exactas de Flet 1.1+ moderno).
    peticion_por_defecto: str = (
        # Descripción funcional de la app en Windows 11.
        "Crea una app de escritorio en Flet para Windows 11 que funcione como recordatorio de tomar pastas. "
        # Requisitos de horarios, ventana flotante persistente, importancia, check obligatorio e historial SQLite.
        "Permite agregar horarios con nivel de importancia (Baja, Media, Crítica), abre una ventana flotante siempre visible (page.window.always_on_top = True) que no se cierre hasta marcar un check de confirmación, y guarda el historial de tomas en SQLite. "
        # Exigimos que el último archivo planeado se llame exactamente 'main.py'.
        "Obligatorio: el último archivo del plan debe llamarse exactamente 'main.py'. "
        # Pistas exactas de sintaxis para Flet 1.1+ para evitar nombres obsoletos de Flet antiguo.
        "Regla obligatoria para Flet 1.1+: usa siempre 'import flet as ft', 'ft.run(main)' (NO ft.app), 'ft.Button' (NO ElevatedButton), 'ft.Icons' (NO icons) y 'ft.Colors' (NO colors)."
    # Cerramos el texto de la petición por defecto.
    )

    # Mostramos el título del sistema en la terminal.
    print("=== MESA REDONDA DE CÓDIGO (Multi-Agente POO Local) ===")
    # Pedimos al usuario que escriba qué programa quiere crear, o presione Enter para usar la App de Pastas.
    entrada_usuario: str = input("\nDescribe qué app quieres crear (o presiona Enter para construir la App de Pastas):\n> ").strip()
    # Elegimos lo que escribió el usuario, o la petición por defecto si solo presionó Enter.
    peticion_final: str = entrada_usuario if entrada_usuario else peticion_por_defecto

    # Lanzamos la construcción completa del proyecto multi-archivo y guardamos la ruta resultante.
    ruta_creada = mesa.construir_proyecto(peticion_final)
    # Imprimimos las instrucciones exactas para probar el proyecto recién fabricado por tus agentes.
    print(f"\nPara probar tu nueva app, ejecuta en terminal:\ncd {ruta_creada}\nuv run main.py")


# Este bloque estándar garantiza que 'main()' solo arranque si ejecutamos directamente 'main.py'.
if __name__ == "__main__":
    # Ejecutamos la función principal.
    main()