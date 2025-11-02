from game import *

def main():
    print("=" * 50)
    print("    ADIVINAR LA PALABRA - MODO CONSOLA")
    print("=" * 50)

    datos_usuario = {
        'nombre_usuario': 'jugador_prueba',
        'estadisticas': {
            'puntaje': 0,
            'errores': 0,
            'tiempo_total': 0,
            'niveles_completados': 0,
            'partidas_jugadas': 0
        },
        'comodines': [True, True, True],  
        'reinicios': 0
    }

    print(f"\n¡Bienvenido, {datos_usuario['nombre_usuario']}!\n")
    input("Presiona Enter para comenzar el juego...")

  
    victoria = jugar_juego_completo(datos_usuario)

 
    print("\n" + "=" * 50)
    if victoria:
        print("        ¡VICTORIA TOTAL!")
        print("    Completaste los 5 niveles")
    else:
        print("        DERROTA")
        print("    No lograste completar todos los niveles.")
        print("    ¡Inténtalo de nuevo!")
    print("=" * 50)


    mostrar_stats(datos_usuario)

if __name__ == "__main__":
    main()