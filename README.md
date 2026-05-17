# 🔐 PasswordGenerator

**PasswordGenerator** es una herramienta generadora de contraseñas mediante el uso de mecanismos **criptográficos robustos**.

El objetivo principal de esta herramienta es proporcionar una forma **rápida**, **flexible** y **fiable** de generar contraseñas con distintos niveles de complejidad, adaptadas tanto a usuarios individuales como a entornos técnicos más exigentes.

---
## 1️⃣ Características:

- 🖥️ Modo interactivo y modo CLI.
- ⚙️ Validaciones robustas de entrada.
- 🧩 4 niveles de complejidad configurables.
- 🔒 Generación de contraseñas seguras usando `secrets`.
- 📊 Cálculo de entropía en bits.
- 📋 Copia automática al portapapeles.
- 💾 Exportación a archivo.

---
## 2️⃣ Requisitos Previos:

PasswdGen está diseñado para funcionar en sistemas Linux/Unix.

> ### 📋pyperclip:
> La funcionalidad de copia automática al portapapeles utiliza **pyperclip** [^1]<br>
> En Linux, personalmente, recomiendo forzar pyperclip a usar **xclip** [^2]
> 
> Para ello, simplemente descomenta la siguiente línea de **`passwdgen.py`**:
>```bash
># pyperclip.set_clipboard("xclip")
>```
>
> Puedes verificar si **xclip** está instalado con **`which xclip`**, o en su defecto, instalarlo ejecutando el siguiente comando:
>```bash
>sudo apt install xclip
>```

>### 🚀 pipx:
>Realizaremos la instalación de PasswdGen mediante **pipx** [^3]
>
>Puedes verificar si **pipx** está instalado ejecutando **`which pipx`**, o en su defecto, instalarlo ejecutando los siguientes comandos:
>```bash
>sudo apt install pipx
>```
>```bash
>pipx ensurepath
>```
>
>Ejecutar **`pipx ensurepath`** después de la instalación, es necesario para añadir el directorio de ejecutables de pipx a la variable de entorno PATH, permitiendo a la terminal reconocer y ejecutar las aplicaciones instaladas desde cualquier ubicación
>
>El **reinicio de la terminal** es indispensable para que la shell recargue los archivos de configuración actualizados y aplique estos cambios

---
## 3️⃣ Instalación:

⚪ Clona el repositorio y accede a él:
```bash
git clone https://github.com/adzibo/PasswordGenerator.git
cd PasswordGenerator
```
⚪ Instala la herramienta PasswdGen ejecutando el siguiente comando:
```bash
pipx install .
```

---
## 4️⃣ Uso:

### 🖥️ Modo Interactivo:

Ejecuta el comando `passwdgen` y el programa te guiará paso a paso.

### ⌨️ Modo CLI:
  
Las opciones disponibles son las siguientes:

| **Flag**          | **Descripción**                 |
| ----------------- | ------------------------------- |
| -l, --longitud    | Longitud de la contraseña       |
| -c, --complejidad | Nivel de complejidad (1-4)      |
| -n, --numero      | Número de contraseñas a generar |
| --no-clipboard    | No copiar al portapapeles       |
| -o, --output      | Guardar en archivo              |

Veamos unos ejemplos usando el modo CLI:

⚪ Generar una contraseña:
```bash
passwdgen -l 20 -c 4
```
⚪ Generar diez contraseñas:
```bash
passwdgen -l 20 -c 4 -n 10
```
⚪ Generar veinte contraseñas y guardarlas en un archivo (sin copiar al portapapeles):
```bash
passwdgen -l 20 -c 4 -n 20 -o password.txt --no-clipboard
```

---
## 5️⃣ Entropía:

La entropía es una medida de la **fortaleza teórica de una contraseña**, expresada en bits.

La fórmula utilizada es:<br>
$$bits = longitud × log2(pool)$$
>**$longitud$** → número de caracteres de la contraseña<br>
>**$pool$** → conjunto de caracteres posibles (por ejemplo: letras, números, símbolos)

La entropía representa cuántas combinaciones posibles existen. Cuanto mayor sea el número de combinaciones, más difícil será romper la contraseña mediante ataques de fuerza bruta.
>🔴 ≤ 40 bits → Débil<br>
>🟡 40–60 bits → Aceptable<br>
>🟢 60–100 bits → Fuerte<br>
>🟣 100 bits → Muy fuerte

## 6️⃣ Decisiones técnicas y fundamentos de seguridad:

La función `generar_password(longitud, nivel)` crea contraseñas aleatorias según el nivel de seguridad.<br>
En el nivel 1 usa solo números; en el nivel 2, letras (asegurando mayúsculas y minúsculas); en el nivel 3 añade números; y en el nivel 4 incluye también símbolos. En los niveles más altos se garantiza que haya al menos un carácter de cada tipo y luego se mezclan para evitar patrones.

A la hora de generar contraseñas seguras, no basta con que sean aleatorias, deben ser **criptográficamente impredecibles**. En Python, el módulo `random` **no es seguro para este propósito**, ya que está diseñado para simulaciones y puede ser predecible si un atacante conoce el estado interno del generador.

Es más seguro usar `secrets.SystemRandom().shuffle(password)` porque utiliza fuentes de aleatoriedad del sistema operativo mucho más difíciles de predecir. Además, con el uso del generador `shuffle`, aseguro que el orden final de los caracteres también sea impredecible, aumentando la seguridad de la contraseña generada.

[^1]: **Pyperclip** es una biblioteca de Python que proporciona funciones multiplataforma para copiar y pegar texto en el portapapeles.
[^2]: **xclip** es una utilidad de línea de comandos para sistemas basados en el **X Window System** que permite acceder y manipular los portapapeles gráficos desde la terminal. Se usa comúnmente para copiar y pegar texto o datos entre aplicaciones gráficas y sesiones de consola en entornos Linux y UNIX.
[^3]: **pipx** es una herramienta de línea de comandos del ecosistema de Python que permite instalar y ejecutar aplicaciones Python en entornos virtuales aislados. Desarrollado bajo la Python Packaging Authority, facilita el uso de herramientas de consola sin interferir con las dependencias del sistema o de otros proyectos.
