# Ejercicios Prácticos de Big Data con Python

> **Para estudiantes**: Este es tu espacio de aprendizaje. Aquí aprenderás Big Data desde cero, trabajando con datos reales y herramientas profesionales.

## Bienvenida

¡Felicidades por comenzar tu viaje en el mundo del Big Data! Este repositorio contiene ejercicios prácticos diseñados para que aprendas haciendo. No necesitas experiencia previa en programación ni en Git/GitHub.

## ¿Qué aprenderás?

- **Python para Datos**: Manipulación de datos con Pandas
- **Bases de Datos**: SQL con SQLite
- **Big Data**: Procesamiento con Dask y Apache Spark
- **Formatos Modernos**: Trabajo con archivos Parquet
- **Git & GitHub**: Control de versiones (¡tu primera vez!)
- **IA como Asistente**: Uso de herramientas de IA para programar

## Antes de Empezar

### Paso 1: Haz un Fork de este Repositorio

Un **fork** es tu copia personal de este proyecto donde trabajarás sin afectar el original.

1. Haz clic en el botón **Fork** (arriba a la derecha en GitHub)
2. Selecciona tu cuenta personal
3. ¡Listo! Ahora tienes tu propia copia

### Paso 2: Lee las Guías

Este repositorio incluye guías paso a paso para ayudarte:

- **[GUIA_GIT_GITHUB.md](./GUIA_GIT_GITHUB.md)**: Todo sobre Git y GitHub (¡empieza aquí!)
- **[GUIA_IA_ASISTENTE.md](./GUIA_IA_ASISTENTE.md)**: Cómo usar IA para aprender y programar
- **[LEEME.md](./LEEME.md)**: Instrucciones técnicas de los ejercicios
- **[ARQUITECTURA_Y_STACK.md](./ARQUITECTURA_Y_STACK.md)**: Conceptos avanzados (opcional)

### Paso 3: Prepara tu Entorno

Necesitarás:
- **Python 3.8+** instalado ([Descargar aquí](https://www.python.org/downloads/))
- **Git** instalado ([Descargar aquí](https://git-scm.com/downloads))
- Un editor de código (recomendamos [VS Code](https://code.visualstudio.com/) o PyCharm)

## Estructura del Proyecto

```
ejercicios_bigdata/
├── README.md                    # Este archivo
├── GUIA_GIT_GITHUB.md           # Guía de Git para principiantes
├── GUIA_IA_ASISTENTE.md         # Guía para usar IA
├── LEEME.md                     # Instrucciones de ejercicios
├── ARQUITECTURA_Y_STACK.md      # Conceptos técnicos
├── requirements.txt             # Librerías Python necesarias
├── PROGRESO.md                  # Tu checklist de avance
├── datos/                       # Tus datos descargados (no se suben a GitHub)
│   └── descargar_datos.py       # Script para descargar datos
└── ejercicios/                  # Aquí trabajarás
    ├── 01_cargar_sqlite.py      # Ejercicio 1: Bases de datos
    ├── 02_limpieza_datos.py     # Ejercicio 2: Limpieza de datos
    ├── 03_parquet_dask.py       # Ejercicio 3: Big Data con Dask
    └── 04_pyspark_query.py      # Ejercicio 4: Apache Spark
```

## Cómo Trabajar en este Proyecto

### 1. Clona TU fork a tu computadora

```bash
# Reemplaza "TU_USUARIO" con tu nombre de usuario de GitHub
git clone https://github.com/TU_USUARIO/ejercicios_bigdata.git
cd ejercicios_bigdata
```

### 2. Crea un entorno virtual de Python

```bash
# Crear el entorno
python -m venv .venv

# Activar el entorno
# En Windows:
.venv\Scripts\activate
# En Mac/Linux:
source .venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Descarga los datos

```bash
python datos/descargar_datos.py
```

### 5. Comienza con el Ejercicio 1

```bash
python ejercicios/01_cargar_sqlite.py
```

## Seguimiento de tu Progreso

1. Abre el archivo [PROGRESO.md](./PROGRESO.md)
2. Marca ✅ cada ejercicio que completes
3. Haz commit de tus cambios regularmente
4. Sube (push) tus commits a GitHub

Tu profesor podrá ver tu progreso en tu fork.

## Cómo Pedir Ayuda

### Opción 1: Usa IA como Asistente
Lee la [GUIA_IA_ASISTENTE.md](./GUIA_IA_ASISTENTE.md) para aprender a pedir ayuda a herramientas como:
- Claude Code
- GitHub Copilot
- ChatGPT

### Opción 2: Abre un Issue
Si tienes problemas:
1. Ve a la pestaña "Issues" en tu fork
2. Crea un nuevo issue describiendo el problema
3. Comparte el enlace con tu profesor

### Opción 3: Pregunta a tu Profesor
Comparte el enlace de tu fork con tu profesor para que vea tu código.

## Reglas de Oro

1. **No tengas miedo de equivocarte**: Los errores son parte del aprendizaje
2. **Haz commits frecuentes**: Guarda tu progreso regularmente
3. **Lee los comentarios del código**: Ahí está la explicación
4. **Usa la IA con criterio**: Úsala para entender, no solo para copiar
5. **Pide ayuda cuando la necesites**: Nadie nace sabiendo

## Recursos Adicionales

- [Documentación oficial de Python](https://docs.python.org/es/)
- [Documentación de Pandas](https://pandas.pydata.org/docs/)
- [Tutorial interactivo de Git](https://learngitbranching.js.org/?locale=es_ES)
- [Curso gratuito de Big Data (YouTube)](https://www.youtube.com/results?search_query=big+data+python+tutorial+español)

## Licencia

Este material es de uso educativo. Siéntete libre de aprender y compartir.

---

**¡Éxito en tu aprendizaje!** Recuerda: todos los profesionales fueron principiantes alguna vez.
