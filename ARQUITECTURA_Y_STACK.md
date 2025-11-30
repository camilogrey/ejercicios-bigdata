# Arquitectura, Stack y Desarrollo Moderno en Big Data

Este documento sirve como guía técnica para entender las tecnologías utilizadas en estos ejercicios y cómo encajan en el panorama del desarrollo de software y datos moderno.

## 1. Stack Tecnológico (La "Pila" de Tecnología)

El "Stack" es el conjunto de herramientas que usamos para construir una solución. En este curso, hemos seleccionado un stack estándar en la industria de Data Science y Big Data.

| Tecnología | Tipo | ¿Para qué sirve? | ¿Por qué es importante? |
| :--- | :--- | :--- | :--- |
| **Python** | Lenguaje | El cerebro de todo. | Es el lenguaje #1 en el mundo para datos e IA. |
| **Pandas** | Librería | Manipulación de datos en memoria (RAM). | El estándar para limpiar y analizar datos pequeños/medianos (< 10GB). |
| **SQLite** | Base de Datos | Almacenamiento relacional (SQL). | Permite aprender SQL sin configurar servidores complejos. |
| **Parquet** | Formato de Archivo | Almacenamiento columnar comprimido. | Es el formato estándar en Big Data. Ahorra espacio y es rapidísimo de leer. |
| **Dask** | Framework | Procesamiento paralelo/distribuido. | Permite usar Pandas en datasets que no caben en tu memoria RAM. |
| **PySpark** | Framework | Procesamiento masivo distribuido. | La herramienta más usada en grandes empresas (Netflix, Uber, bancos) para petabytes de datos. |

## 2. Especificaciones del Proyecto (Specs)

### Requisitos del Sistema
Para correr estos ejercicios en un entorno local (tu PC):
*   **OS**: Windows, macOS o Linux.
*   **Python**: Versión 3.8 o superior.
*   **RAM**: Mínimo 4GB (8GB recomendado). Dask y Spark gestionan la memoria, pero necesitan un mínimo para arrancar.

### Flujo de Datos (Data Pipeline)
El proyecto implementa un "Pipeline" (tubería) de datos clásico:

1.  **Ingesta (Ingestion)**: Descarga de datos crudos desde internet (`requests`).
2.  **Limpieza (Cleaning)**: Eliminación de errores y nulos (`pandas`).
3.  **Almacenamiento (Storage)**:
    *   *Capa Relacional*: Guardado en base de datos para consultas transaccionales (`SQLite`).
    *   *Capa Analítica (Data Lake)*: Guardado en archivos optimizados (`Parquet`).
4.  **Procesamiento (Processing)**: Consultas pesadas y agregaciones (`Dask`, `Spark`).

## 3. Arquitectura de Datos Moderna

Lo que estamos construyendo a pequeña escala refleja la arquitectura de grandes empresas:

### ETL vs ELT
*   **ETL (Extract, Transform, Load)**: Lo que hacemos en el Ejercicio 2. Extraemos datos, los transformamos (limpiamos) y los cargamos en su destino final.
*   **Data Lake**: El uso de archivos `Parquet` simula un "Lago de Datos", donde guardamos información estructurada lista para ser consumida por herramientas de Big Data.

### ¿Por qué Parquet y no CSV?
En el desarrollo moderno, **CSV** es solo para intercambio simple. **Parquet** es superior porque:
*   **Columnar**: Si solo necesitas la columna "precio", Parquet lee solo esa columna. CSV tiene que leer todo el archivo fila por fila.
*   **Tipado**: Parquet sabe que una fecha es una fecha. En CSV todo es texto hasta que lo conviertes.

## 4. Prácticas de Desarrollo Moderno

Estos ejercicios también te enseñan cómo trabajan los desarrolladores profesionales:

*   **Entornos Virtuales (`venv`)**:
    *   *Problema*: Instalar librerías en todo el sistema causa conflictos (ej. Proyecto A necesita Pandas 1.0 y Proyecto B necesita Pandas 2.0).
    *   *Solución*: Cada proyecto tiene su propia "caja" aislada con sus propias versiones.

*   **Gestión de Dependencias (`requirements.txt`)**:
    *   Un archivo de texto que lista exactamente qué librerías necesita el proyecto. Permite que cualquier persona en el mundo replique tu entorno con un solo comando (`pip install -r ...`).

*   **Código Modular**:
    *   En lugar de un script gigante de 1000 líneas, dividimos el problema en scripts pequeños y especializados (`descargar`, `limpiar`, `analizar`). Esto hace el código más fácil de leer, probar y mantener.
