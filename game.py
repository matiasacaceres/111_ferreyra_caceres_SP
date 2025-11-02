# game.py
import random
from words import PALABRAS_POR_NIVEL


# ----------------------------------------------------------------------
#  USUARIO (hardcodeado – sin archivos)
# ----------------------------------------------------------------------
def cargar_usuarios():
    return {}

def guardar_usuario(usuario_data):
    pass                     # nada se guarda (modo prueba)

def login():
    return None

def crear_usuario():
    """Devuelve un diccionario con la estructura que necesita el juego."""
    return {
        'nombre_usuario': 'jugador_prueba',
        'estadisticas': {
            'puntaje': 0,
            'errores': 0,
            'niveles_completados': 0,
            'partidas_jugadas': 0
        },
        'comodines': [True, True, True],   # 0: revelar, 1: temática, 2: extra
        'reinicios': 0
    }


# ----------------------------------------------------------------------
#  SELECCIÓN DE PALABRAS
# ----------------------------------------------------------------------
def obtener_palabra_secreta(nivel):
    categorias = PALABRAS_POR_NIVEL[nivel]
    tematica   = random.choice(list(categorias.keys()))
    palabra    = random.choice(categorias[tematica]).strip().lower()
    return palabra, tematica


def obtener_tematica(nivel):
    categorias = PALABRAS_POR_NIVEL[nivel]
    return random.choice(list(categorias.keys()))


# ----------------------------------------------------------------------
#  VERIFICACIÓN DE ADIVINANZA (sin Counter)
# ----------------------------------------------------------------------
def _contar_letras(cadena):
    """Devuelve un diccionario {letra: cantidad}."""
    conteo = {}
    for letra in cadena:
        conteo[letra] = conteo.get(letra, 0) + 1
    return conteo


def verificar_adivinanza(palabra_secreta, adivinanza):
    """Devuelve lista de colores: 'verde', 'amarillo' o 'gris'."""
    n = len(adivinanza)
    retro = ['gris'] * n
    # diccionario con cuántas veces aparece cada letra en la palabra secreta
    restantes = _contar_letras(palabra_secreta)

    # ---------- 1ª pasada: letras en posición correcta ----------
    for i in range(n):
        if adivinanza[i] == palabra_secreta[i]:
            retro[i] = 'verde'
            restantes[adivinanza[i]] -= 1

    # ---------- 2ª pasada: letras correctas pero en otra posición ----------
    for i in range(n):
        if retro[i] == 'gris' and adivinanza[i] in restantes and restantes[adivinanza[i]] > 0:
            retro[i] = 'amarillo'
            restantes[adivinanza[i]] -= 1

    return retro


# ----------------------------------------------------------------------
#  TABLERO
# ----------------------------------------------------------------------
def mostrar_tablero(adivinanzas, retroalimentaciones):
    for palabra, colores in zip(adivinanzas, retroalimentaciones):
        for letra, color in zip(palabra, colores):
            if color == 'verde':
                print('\033[92m' + letra.upper() + '\033[0m', end=' ')
            elif color == 'amarillo':
                print('\033[93m' + letra.upper() + '\033[0m', end=' ')
            else:
                print('\033[90m' + letra.upper() + '\033[0m', end=' ')
        print()
    print()


# ----------------------------------------------------------------------
#  COMODINES
# ----------------------------------------------------------------------
def usar_comodin_revelar(palabra_secreta):
    pos   = random.randint(0, len(palabra_secreta) - 1)
    letra = palabra_secreta[pos]
    print(f"Letra en posición {pos+1}: {letra.upper()}")
    return True


def usar_comodin_tematica(tematica):
    print(f"Temática: {tematica.capitalize()}")
    return True


def usar_comodin_extra(palabra_secreta):
    todas = set('abcdefghijklmnopqrstuvwxyz')
    usadas = set(palabra_secreta)
    disponibles = todas - usadas
    if disponibles:
        letra = random.choice(list(disponibles))
        print(f"Letra AUSENTE: {letra.upper()}")
    else:
        print("No hay letras para revelar como ausentes.")
    return True


# ----------------------------------------------------------------------
#  PARTIDA (una palabra)
# ----------------------------------------------------------------------
def jugar_partida(nivel, vidas_restantes, datos_usuario):
    palabra_secreta, tematica = obtener_palabra_secreta(nivel)
    longitud = len(palabra_secreta)

    adivinanzas   = []
    retroalimentaciones = []
    errores       = 0
    puntaje_partida = 0

    while vidas_restantes > 0:
        mostrar_tablero(adivinanzas, retroalimentaciones)
        print(f"Nivel {nivel} | Vidas: {vidas_restantes}")
        print("Escribe tu palabra o usa comodín (1, 2, 3):")
        entrada = input("> ").strip().lower()

        # ---------- comodines ----------
        if entrada == '1' and datos_usuario['comodines'][0]:
            usar_comodin_revelar(palabra_secreta)
            datos_usuario['comodines'][0] = False
            continue
        if entrada == '2' and datos_usuario['comodines'][1]:
            usar_comodin_tematica(tematica)
            datos_usuario['comodines'][1] = False
            continue
        if entrada == '3' and datos_usuario['comodines'][2]:
            usar_comodin_extra(palabra_secreta)
            datos_usuario['comodines'][2] = False
            continue

        # ---------- validación ----------
        if len(entrada) != longitud:
            print(f"¡Debe tener {longitud} letras!")
            continue

        # ---------- feedback ----------
        feedback = verificar_adivinanza(palabra_secreta, entrada)
        adivinanzas.append(entrada)
        retroalimentaciones.append(feedback)

        # ---------- puntuación ----------
        verdes   = feedback.count('verde')
        amarillos = feedback.count('amarillo')
        grises   = longitud - verdes - amarillos
        puntos   = verdes * 20 + amarillos * 10 + grises * (-15)
        puntaje_partida += puntos

        if verdes == longitud:
            print("¡CORRECTO!")
            return True, vidas_restantes, errores, puntaje_partida

        errores += 1
        vidas_restantes -= 1
        print("Incorrecto. -1 vida")

    print(f"¡Sin vidas! La palabra era: {palabra_secreta.upper()}")
    return False, 0, errores, 0          # 0 puntos si pierde


# ----------------------------------------------------------------------
#  NIVEL (3 partidas ganadas)
# ----------------------------------------------------------------------
def jugar_nivel(nivel, datos_usuario):
    vidas_nivel = 3
    ganadas     = 0
    errores_niv = 0
    puntaje_niv = 0

    while ganadas < 3:
        win, vidas_nivel, errores_part, puntos_part = jugar_partida(
                nivel, vidas_nivel, datos_usuario)

        errores_niv += errores_part

        if win:
            ganadas += 1
            puntaje_niv += puntos_part
            datos_usuario['estadisticas']['partidas_jugadas'] += 1
        else:
            datos_usuario['reinicios'] += 1
            if datos_usuario['reinicios'] > 3:
                print("¡MÁXIMO DE REINICIOS!")
                return False, 0
            print(f"Reiniciando nivel... ({datos_usuario['reinicios']}/3)")
            vidas_nivel = 3
            ganadas = 0
            errores_niv = 0
            puntaje_niv = 0

    datos_usuario['estadisticas']['errores'] += errores_niv
    datos_usuario['estadisticas']['niveles_completados'] += 1
    print(f"¡NIVEL {nivel} COMPLETADO! +{puntaje_niv} pts")
    return True, puntaje_niv


# ----------------------------------------------------------------------
#  JUEGO COMPLETO (5 niveles)
# ----------------------------------------------------------------------
def jugar_juego_completo(datos_usuario):
    datos_usuario['comodines'] = [True, True, True]
    datos_usuario['reinicios'] = 0
    puntaje_total = 0

    for nivel in range(1, 6):
        exito, puntos_nivel = jugar_nivel(nivel, datos_usuario)
        if not exito:
            return False, datos_usuario['estadisticas']
        puntaje_total += puntos_nivel

    datos_usuario['estadisticas']['puntaje'] += puntaje_total
    return True, datos_usuario['estadisticas']


# ----------------------------------------------------------------------
#  ESTADÍSTICAS
# ----------------------------------------------------------------------
def mostrar_stats(datos_usuario):
    e = datos_usuario['estadisticas']
    print("\n" + "="*40)
    print("       ESTADÍSTICAS FINALES")
    print("="*40)
    print(f"Puntaje total: {e['puntaje']}")
    print(f"Errores totales: {e['errores']}")
    print(f"Niveles completados: {e['niveles_completados']}/5")
    print(f"Partidas jugadas: {e['partidas_jugadas']}")
    print("="*40)