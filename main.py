#Importamos nuestra clase 'AgenteBase' desde el archivo 'agente_base.py' dentro de la carpeta 'mesa_redonda'.
from mesa_redonda.agente_base import AgenteBase

#Importamos nuestra clase 'Configuracion' desde el archivo 'configuracion.py' dentro de la carpeta 'mesa_redonda'
from mesa_redonda.configuracion import Configuracion

#Definimos una función principal 'main' para mantener el código ordenado y limpio.
def main()-> None:
    #Creamos una instacia (un objeto real) de la clase 'Configuracion'.
    config = Configuracion()
    #Llamamos al método 'preparar_entorno' para asegurarnos de que exista la carpeta de proyectos generados.
    config.preparar_entorno()

    #Creamos nuestro primer objero agente instanciando la clase 'AgenteBase' con datos de prueba.
    arquitecto_prueba = AgenteBase(
        #Le asignamos un nombre visible al objeto agente.
        nombre = "Arquitecto Alpha",
        #Le definimos su especialidad.
        rol = "Arquitecto de Software POO",
        #Le pasamos el modelo configurado en nuestro objeto 'config'.
        modelo = config.modelo_arquitecto,
        #Le damos sus reglas de comportamiento: diseñar con POO modular y responder en español.
        instrucciones_sistema = "Eres un Arquitecto de Software experto en Python y POO muodular. Responde en español de forma breve y estructurada.",
        #Cerramos la creación del objeto 'arquitecto_prueba'.
    )

    #Le enviamos una primera pregunta de prueba usando su método '.pensar()' y guardamos la respuesta.
    resultado = arquitecto_prueba.pensar(
        #Esta es la instrucción de prueba para confirmar que la tarjeta grafica, Ollama y nuestro código POO funciona juntos.
        "Quiero hacer una app en Python para recordar tomar mis pastas. Dime en 4 líneas qué clases principales debería tener."
        #Cerramos la llamada el método '.pensar()'.
    )

    #Imprimimos una línea separada visual en la consola.
    print("Respuesta del Agente")
    #Mostramos en pantalla la respuesta que devolvió el objeto agente.
    print(resultado)

#Este bloque estándar garantiza que 'main()' solo arranque si ejecutamos directamente 'main.py'.
if __name__ == "__main__":
    #Ejecutamos la función principal.
    main()
    