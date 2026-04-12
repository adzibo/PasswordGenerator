#!/usr/bin/env python3

# ===========================================================================
# IMPORTACIÓN DE BIBLIOTECA ESTÁNDAR
# ===========================================================================
import argparse
import sys
import secrets
import string
import math

# ===========================================================================
# IMPORTACIÓN OPCIONAL DE PYPERCLIP
# ===========================================================================
try:
    """
    Se importa de forma no bloqueante. Si pyperclip no está instalado, la herramienta sigue funcionando.
    El error solo se notifica si el usuario intenta usar el portapapeles sin desactivado con --no-clipboard.
    """
    import pyperclip
    _PYPERCLIP_DISPONIBLE = True

except ModuleNotFoundError:
    _PYPERCLIP_DISPONIBLE = False

# ===========================================================================
# CONSTANTES DE CONFIGURACIÓN
# ===========================================================================
LONGITUD_MIN = 8     # Mínimo de caracteres considerado seguro.
LONGITUD_MAX = 5000  # Límite superior para evitar contraseñas inmanejables.

NIVEL_MIN = 1   # Nivel de complejidad más bajo disponible.
NIVEL_MAX = 4   # Nivel de complejidad más alto disponible.

NUM_PASSWD_MIN = 1       # Mínimo de contraseñas a generar en modo batch.
NUM_PASSWD_MAX = 100000  # Máximo de contraseñas a generar en modo batch.

__version__ = "1.0.0"   # Metadata


# ===========================================================================
# BANNER
# ===========================================================================
def banner():
    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║       ██████╗  █████╗ ███████╗███████╗██╗    ██╗██████╗       ║
    ║       ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗      ║
    ║       ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║  ██║      ║
    ║       ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║  ██║      ║
    ║       ██║     ██║  ██║███████║███████║╚███╔███╔╝██████╔╝      ║
    ║       ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═════╝       ║
    ║                    ██████╗ ███████╗███╗   ██╗                 ║
    ║                   ██╔════╝ ██╔════╝████╗  ██║                 ║
    ║                   ██║  ███╗█████╗  ██╔██╗ ██║                 ║
    ║                   ██║   ██║██╔══╝  ██║╚██╗██║                 ║
    ║                   ╚██████╔╝███████╗██║ ╚████║                 ║
    ║                    ╚═════╝ ╚══════╝╚═╝  ╚═══╝                 ║
    ╚═══════════════════════════════════════════════════════════════╝
    ┌───────────────────────────────────────────────────────────────┐
    │               NIVELES DE COMPLEJIDAD DISPONIBLES              │
    ├──────┬──────────────────┬─────────────────────────────────────┤
    │  Nº  │  Nivel           │  Caracteres utilizados              │
    ├──────┼──────────────────┼─────────────────────────────────────┤
    │  1   │  Bajo            │  Solo dígitos (0-9)                 │
    │  2   │  Medio           │  Letras (A-Z, a-z)                  │
    │  3   │  Alto            │  Letras + dígitos                   │
    │  4   │  Muy Alto        │  Letras + dígitos + símbolos        │
    └──────┴──────────────────┴─────────────────────────────────────┘
    """)


# ===========================================================================
# ENTRADA DE DATOS (MODO INTERACTIVO)
# ===========================================================================
def obtener_longitud():
    """
    Solicita al usuario de forma interactiva la longitud deseada para la
    contraseña y valida que el valor esté dentro del rango permitido.

    Reglas de validación:
      - Mínimo: LONGITUD_MIN caracteres (requisito mínimo de seguridad).
      - Máximo: LONGITUD_MAX caracteres (límite de usabilidad).
    """
    while True:
        try:
            longitud = int(input(f"\n⚪ Inserte el número de caracteres ({LONGITUD_MIN} - {LONGITUD_MAX}): "))

            if longitud < LONGITUD_MIN:
                print("\t[⚠️] Para que una contraseña se pueda considerar 'segura', "
                      f"debe ser igual o superior a los {LONGITUD_MIN} caracteres.")
            elif longitud > LONGITUD_MAX:
                print(f"\t[❌] La longitud no puede superar los {LONGITUD_MAX} caracteres.")
            else:
                return longitud

        except ValueError:
            # ValueError se lanza cuando int() recibe una cadena no numérica.
            print("\t[❌] Introduce un número entero válido.")

        except Exception as e:
            print(f"\t[❌] Se ha producido un error de tipo '{e}'.")


def obtener_nivel_complejidad():
    """
    Solicita al usuario de forma interactiva el nivel de complejidad (1-4)
    y valida que el valor esté dentro del rango permitido.

    Niveles disponibles:
      1 → Solo dígitos.
      2 → Solo letras (mayúsculas y minúsculas).
      3 → Letras y dígitos (alfanumérico).
      4 → Letras, dígitos y caracteres especiales/puntuación.
    """
    while True:
        try:
            nivel = int(input(f"\n⚪ Inserte el nivel de complejidad ({NIVEL_MIN} - {NIVEL_MAX}): "))

            if nivel < NIVEL_MIN:
                print(f"\t[❌] El valor mínimo es {NIVEL_MIN}.")
            elif nivel > NIVEL_MAX:
                print(f"\t[❌] El valor máximo es {NIVEL_MAX}.")
            else:
                return nivel

        except ValueError:
            print("\t[❌] Introduce un número entero válido.")

        except Exception as e:
            print(f"\t[❌] La complejidad insertada, ha provocado un error de tipo '{e}'.")


# ===========================================================================
# GENERACIÓN DE CONTRASEÑA
# ===========================================================================
def generar_password(longitud, nivel):
    # ====================================================
    # Nivel 1: Solo Números
    # Pool: "0123456789" → 10 caracteres posibles.
    # ====================================================
    if nivel == 1:
        caracteres = string.digits
        password = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        return password, caracteres

    # ====================================================
    # Nivel 2: Solo Letras
    # Pool: a-z + A-Z → 52 caracteres posibles.
    # Garantiza al menos 1 minúscula y 1 mayúscula.
    # ====================================================
    elif nivel == 2:
        caracteres = string.ascii_letters
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase)
        ]

        password += [secrets.choice(caracteres) for _ in range(longitud - 2)]
        secrets.SystemRandom().shuffle(password)
        return ''.join(password), caracteres

    # ====================================================
    # Nivel 3: Letras y Números
    # Pool: a-z + A-Z + 0-9 → 62 caracteres posibles.
    # Garantiza al menos 1 minúscula, 1 mayúscula y 1 dígito.
    # ====================================================
    elif nivel == 3:
        caracteres = string.ascii_letters + string.digits
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits)
        ]

        password += [secrets.choice(caracteres) for _ in range(longitud - 3)]
        secrets.SystemRandom().shuffle(password)
        return ''.join(password), caracteres

    # ====================================================
    # Nivel 4: Letras, Números y Signos
    # Pool: a-z + A-Z + 0-9 + puntuación → ~94 caracteres posibles.
    # Garantiza al menos 1 minúscula, 1 mayúscula, 1 dígito y 1 símbolo.
    # ====================================================
    elif nivel == 4:
        caracteres = string.ascii_letters + string.digits + string.punctuation
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(string.punctuation)
        ]

        password += [secrets.choice(caracteres) for _ in range(longitud - 4)]
        secrets.SystemRandom().shuffle(password)
        return ''.join(password), caracteres


# ===========================================================================
# CÁLCULO DE ENTROPÍA
# ===========================================================================
def calcular_entropia(longitud, pool_size):
    """
    Estima la entropía de la contraseña en bits y devuelve una cadena
    descriptiva con la valoración cualitativa de su fortaleza.

    Fórmula empleada:
        H = longitud × log₂(pool_size)

    Donde:
      H          → Entropía en bits.
      longitud   → Número de caracteres de la contraseña.
      pool_size  → Tamaño del alfabeto (número de caracteres posibles).

    La entropía mide cuánta información aleatoria contiene la contraseña:
    a mayor entropía, más difícil resulta de adivinar por fuerza bruta.
    """
    bits = round(longitud * math.log2(pool_size), 2)

    if bits <= 40:
        nivel_texto = "Débil"
    elif 40 < bits <= 60:
        nivel_texto = "Aceptable"
    elif 60 < bits <= 100:
        nivel_texto = "Fuerte"
    else:
        nivel_texto = "Muy Fuerte"

    return f"\t🔒 Entropía estimada (aprox.): {bits} bits -> {nivel_texto}\n"


# ===========================================================================
# GESTIÓN DEL PORTAPAPELES
# ===========================================================================
def copiar_al_portapapeles(passwd_to_copy):
    """
    Intenta copiar el texto proporcionado al portapapeles del sistema.

    Centraliza la lógica del portapapeles en un único lugar, evitando
    duplicar el bloque try/except en cada punto del código donde se
    necesita esta funcionalidad.

    pyperclip detecta automáticamente el backend disponible:
      - Linux  : xclip o xsel (deben estar instalados en el sistema).
      - macOS  : pbcopy (incluido por defecto en el sistema).
      - Windows: win32clipboard (incluido por defecto en el sistema).

    En Linux, personalmente recomiendo forzar pyperclip a usar xclip.
    Para ello, simplemente descomenta la línea 'pyperclip.set_clipboard("xclip")'.
    """
    try:
        # pyperclip.set_clipboard("xclip")
        pyperclip.copy(passwd_to_copy)
        return True

    except Exception as e:
        print(f"\t[⚠️] No se pudo copiar al portapapeles. Se ha producido un error de tipo: {e}.\n")
        return False


# ===========================================================================
# GESTIÓN DE ARGUMENTOS CLI
# ===========================================================================
def parse_args():
    """
    Define y parsea los argumentos de línea de comandos disponibles.

    Argumentos soportados:
      -l / --longitud    : Longitud de la contraseña (int).
      -c / --complejidad : Nivel de complejidad 1-4 (int).
      -n / --numero      : Número de contraseñas a generar (int, defecto 1).
      --no-clipboard     : Flag; si presente, no copia al portapapeles.
      -o / --output      : Ruta del archivo donde guardar las contraseñas.
      -v / --version     : Muestra la versión actual y termina.

    La presencia de -l, -c, -n, -o o --no-clipboard activa el "modo CLI"
    en main(), evitando que se lance la interfaz interactiva.
    """
    parser = argparse.ArgumentParser(
        prog="passwdgen",
        description="Generador de contraseñas seguras."
    )

    parser.add_argument(
        "-l", "--longitud",
        type=int,
        help=f"Longitud de la contraseña ({LONGITUD_MIN} - {LONGITUD_MAX} caracteres)."
    )

    parser.add_argument(
        "-c", "--complejidad",
        type=int,
        help=f"Nivel de complejidad ({NIVEL_MIN} - {NIVEL_MAX})."
    )

    parser.add_argument(
        "-n", "--numero",
        type=int,
        default=1,
        help=f"Número de contraseñas a generar (defecto: 1, máx: {NUM_PASSWD_MAX})."
    )

    parser.add_argument(
        "--no-clipboard",
        action="store_true",  # Flag booleano; True si está presente en el comando.
        help="No copiar la contraseña al portapapeles."
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        metavar="ARCHIVO",
        help="Ruta del archivo donde guardar las contraseñas generadas."
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    return parser.parse_args()


# ===========================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ===========================================================================
def main():
    """
    Función principal que orquesta el flujo completo de la herramienta.

    Detecta automáticamente en qué modo debe operar:

    · Modo CLI        : Se activa cuando el usuario pasa al menos uno de
                        los argumentos -l, -c, -n, -o o --no-clipboard.
                        Realiza validaciones, genera las contraseñas y
                        gestiona la salida (portapapeles y/o archivo).

    · Modo interactivo: Se activa cuando no se pasa ningún argumento.
                        Muestra el banner y guía al usuario con prompts.

    En ambos modos, la generación se delega a `generar_password()` y la
    entropía se calcula con `calcular_entropia()`.
    """

    args = parse_args()

    # ====================================================
    # DETECTAR MODO
    # ====================================================
    modo_cli = any([
        args.longitud is not None,
        args.complejidad is not None,
        args.numero != 1,
        args.output is not None,
        args.no_clipboard
    ])

    # ====================================================
    # MODO CLI
    # ====================================================
    if modo_cli:
        longitud = args.longitud
        nivel = args.complejidad
        num_passwd = args.numero

        # ================================================
        # VALIDACIONES DE ENTRADA
        # ================================================
        if (longitud is None) or (nivel is None):
            print("\n\t[❌] En modo CLI debes especificar -l (longitud) y -c (complejidad).\n")
            sys.exit(1)

        # Listamos todos los errores que se puedan producir:
        errores = []

        if (longitud < LONGITUD_MIN) or (longitud > LONGITUD_MAX):
            errores.append(f"[❌] La longitud debe estar entre {LONGITUD_MIN} y {LONGITUD_MAX} caracteres.")

        if (nivel < NIVEL_MIN) or (nivel > NIVEL_MAX):
            errores.append(f"[❌] El nivel debe ser un valor entre {NIVEL_MIN} y {NIVEL_MAX}.")

        if (num_passwd < NUM_PASSWD_MIN) or (num_passwd > NUM_PASSWD_MAX):
            errores.append(f"[❌] El numero de contraseñas debe estar entre {NUM_PASSWD_MIN} y {NUM_PASSWD_MAX}.")

        if (not _PYPERCLIP_DISPONIBLE) and (not args.no_clipboard):
            errores.append(f"[❌] Modulo no encontrado."
                           f"\n\tComprueba que pyperclip esté instalado o usa las flags '--no-clipboard, -o' "
                           f"\n\tpara exportar la contraseña a un archivo sin copiar al portapapeles.")

        # Si se producen errores, se muestran todos juntos:
        if errores:
            for error in errores:
                print(f"\n\t{error}")
            print()
            sys.exit(1)

        # ================================================
        # GENERACIÓN DE CONTRASEÑA ÚNICA
        # ================================================
        if num_passwd == 1:
            # Generamos la contraseña:
            try:
                password, pool = generar_password(longitud, nivel)
                print("\n\t✅ Contraseña generada correctamente.\n")

            except Exception as e:
                print(f"\t[❌] Contraseña No Generada. Error de tipo: {e}.")
                sys.exit(1)

            # Calculamos la entropía y la printamos:
            print(calcular_entropia(longitud, len(pool)))

            # Si se cumple la condición, copiamos la contraseña generada al portapapeles:
            if not args.no_clipboard:
                if copiar_al_portapapeles(password):
                    print("\t📋 Contraseña copiada al portapapeles.\n")

            # Si se cumple la condición, guardamos la contraseña generada en el archivo:
            if args.output:
                try:
                    with open(args.output, "w") as f:
                        f.write(f"{password}")
                    print(f"\t💾 Contraseña guardada en el archivo: {args.output}.\n")

                except Exception as e:
                    print(f"\t[❌] No se pudo guardar el archivo. Error de tipo: {e}.\n")

        # ================================================
        # GENERACIÓN DE VARIAS CONTRASEÑAS
        # ================================================
        else:
            passwords = []
            pools = []
            portapapeles = ""

            # Generamos las contraseñas:
            try:
                for _ in range(num_passwd):
                    passwd, pool = generar_password(longitud, nivel)
                    passwords.append(passwd)
                    pools.append(pool)
                print("\n\t✅ Contraseñas generadas correctamente.\n")

            except Exception as e:
                print(f"\t[❌] Contraseñas No Generadas. Error de tipo: {e}.")
                sys.exit(1)

            # Calculamos la entropía de la primera contraseña para dar una estimación general:
            print(calcular_entropia(longitud, len(pools[0])))

            # Si se cumple la condición, copiamos las contraseñas generadas al portapapeles:
            if not args.no_clipboard:
                for password in passwords:
                    portapapeles += f"{password}\n"

                if copiar_al_portapapeles(portapapeles):
                    print("\t📋 Contraseñas copiadas al portapapeles.\n")

            # Si se cumple la condición, guardamos las contraseñas generadas en el archivo:
            if args.output:
                try:
                    with open(args.output, "w") as f:
                        for password in passwords:
                            f.write(f"{password}\n")
                    print(f"\t💾 Contraseñas guardadas en el archivo: {args.output}.\n")

                except Exception as e:
                    print(f"\t[❌] No se pudo guardar el archivo. Error de tipo: {e}.\n")

    # ====================================================
    # MODO INTERACTIVO
    # ====================================================
    else:
        # Comprobamos que pyperclip esté disponible:
        if not _PYPERCLIP_DISPONIBLE:
            print(f"\n[❌] Modulo no encontrado."
                  f"\n[⚠️] Ejecuta 'pip install pyperclip' para instalarlo.\n")
            sys.exit(1)

        # Mostramos el banner:
        banner()

        # Obtenemos datos de longitud y nivel de complejidad:
        longitud = obtener_longitud()
        nivel = obtener_nivel_complejidad()

        # Generamos la contraseña:
        try:
            passwd, pool = generar_password(longitud, nivel)
            print("\n\t✅ Contraseña generada correctamente.\n")

        except Exception as e:
            print(f"\t[❌] Contraseña No Generada. Error de tipo: {e}.")
            sys.exit(1)

        # Calculamos la entropía y la printamos:
        print(calcular_entropia(longitud, len(pool)))

        # Copiamos la contraseña al portapapeles:
        if copiar_al_portapapeles(passwd):
            print("\t📋 Contraseña copiada al portapapeles.\n")


if __name__ == '__main__':
    main()
