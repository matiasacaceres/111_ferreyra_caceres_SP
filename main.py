from game import *

def main():
    print("ADIVINAR LA PALABRA - CONSOLA")
    user_data = login()
    if not user_data:
        user_data = crear_usuario()
    victoria, stats = jugar_juego_completo(user_data)
    if victoria:
        print("VICTORIA! Completaste los 5 niveles")
    else:
        print("Derrota. Inténtalo de nuevo!")
    guardar_usuario(stats)
    mostrar_stats(stats)

if __name__ == "__main__":
    main()