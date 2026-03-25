## ERRORES PRINCIPALES ENCONTRADOS

### 1. PostgreSQL no iniciaba en Windows
* **Error:** `qog-postgres | chmod: /var/lib/postgresql/data: Operation not permitted`.
* **Problema:** Los *bind mounts* de Windows a Linux presentan conflictos de permisos NTFS vs Linux.
* **Solución:** Utilizar **named volumes** gestionados por Docker.
* **Código correcto (YAML):**
    ```yaml
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ```
* **Aprendizaje:** En Windows, los named volumes evitan problemas de compatibilidad de sistemas de archivos.

### 2. Dependencias Python no se instalaban
* **Error:** `[Errno 13] Permission denied: '/home/spark'`.
* **Problema:** El usuario `spark` no tiene permisos de escritura para instalar paquetes en el contenedor.
* **Solución:** Instalar como `root` y ejecutar el servicio como usuario `spark`.
* **Código correcto (YAML):**
    ```yaml
    spark-master:
      user: root
      command: >
        bash -c "pip install dependencias... && exec su spark -c 'spark-class Master'"
    ```
* **Aprendizaje:** Se requiere privilegios de root temporales para configurar el entorno antes de volver al usuario seguro.

### 3. Sintaxis Python en pipeline.py
* **Error:** `SyntaxError: invalid syntax` en la línea del `.master()`.
* **Problemas:**
    * Falta de comillas en la URL de Spark.
    * Falta de barras invertidas (`\`) para continuar líneas.
    * Configuraciones de memoria ausentes.
* **Solución (Python):**
    ```python
    def crear_spark_session():
        spark = SparkSession.builder \
            .appName("QoG_Clustering_Analysis") \
            .master("spark://spark-master:7077") \
            .config("spark.executor.memory", "2g") \
            .config("spark.driver.memory", "2g") \
            .getOrCreate()
    ```
* **Aprendizaje:** Los comentarios al final de `\` rompen la sintaxis; la indentación en SparkSession es crítica.

### 4. Spark Master UI no accesible
* **Error:** `curl -I http://localhost:8080` (Can't reach page).
* **Causas:** Puertos ocupados en Windows (IIS/otros) o el servicio aún iniciando.
* **Solución:**
    * Revisar logs: `docker-compose logs spark-master`.
    * Cambiar mapeo de puertos: `"18080:8080"`.
* **Aprendizaje:** El estado "Up" de un contenedor no garantiza que la aplicación interna esté lista.

### 5. Desfase de versiones Python
* **Error:** Contenedor usa Python 3.8.10 mientras el local usa 3.14.
* **Problema:** Incompatibilidad de paquetes (ej. pandas 2.x requiere versiones de Python más nuevas).
* **Solución:** Fijar versiones en `requirements.txt` compatibles con Ubuntu 20.04 (Python 3.8):
    * `pandas==1.5.3`
    * `numpy==1.24.4`
* **Aprendizaje:** Siempre alinear el desarrollo local con la versión de la imagen base de Docker.

### 6. Conexión entre servicios
* **Error:** `Connection refused to postgres:5432`.
* **Problema:** Intentar usar `localhost` en lugar del nombre del servicio en la red de Docker.
* **Solución (Python):**
    ```python
    POSTGRES_CONFIG = {'host': 'postgres'} # Nombre definido en docker-compose
    ```
* **Aprendizaje:** En Docker, el DNS interno resuelve los nombres de los servicios automáticamente.

---

## 🎓 APRENDIZAJES CLAVE

### Técnicos
* **Infraestructura:** Named volumes > Bind mounts en Windows.
* **Seguridad:** Gestión de usuarios root vs no-root en Spark.
* **Redes:** Comunicación entre contenedores vía Service Name.
* **YAML:** La indentación es estrictamente sensible.

### Metodológicos
* **Debugging:** Priorizar `docker-compose logs` sobre el estado del proceso.
* **Integración:** Probar componentes de forma incremental (primero DB, luego Spark, luego Scripts).
* **Documentación:** Registrar el error y la solución evita ciclos de reparación repetitivos.

---

## 🔧 TABLA DE SOLUCIONES RÁPIDAS

| Problema | Síntoma | Solución |
| :--- | :--- | :--- |
| Permisos Windows | "Operation not permitted" | Usar **named volumes** |
| Dependencias Spark | "Permission denied" | Instalar como **root**, ejecutar como **spark** |
| Comunicación | "Connection refused" | Usar **nombres de servicio**, no localhost |
| Puertos ocupados | UI no accesible | Cambiar a **18080** |
| Versiones Python | Error de paquetes | Usar versiones para **Python 3.8** |

---

## 💡 CONSEJOS PARA FUTUROS PROYECTOS
* **Empezar simple:** Crear un archivo Compose mínimo y escalar.
* **Logs en vivo:** Usar `docker-compose logs -f` durante el desarrollo.
* **Health checks:** Implementar verificaciones de salud para asegurar que la DB esté lista antes que Spark.
* **Límites de recursos:** Configurar CPU/RAM en Docker Desktop para evitar bloqueos en Windows.

Prompt 1: Creación inicial del docker-compose.yml
text
"Escribe un docker-compose.yml que levante un mini-cluster con:
- PostgreSQL (base de datos)
- Spark Master (coordinador)
- Spark Worker (nodo de procesamiento)
Requisitos:
- PostgreSQL: imagen postgres:16-alpine, puerto 5432, healthcheck
- Spark: imagen apache/spark:3.5.4-python3 (no bitnami)
- Master: puertos 7077 (comunicación), 8080 (UI web), 4040 (apps)
- Worker: conectado al Master, al menos 1 nodo
- Considera que estoy en Windows, problemas de permisos con Docker"
Respuesta/Solución:
Se proporcionó docker-compose.yml inicial con 3 servicios, pero surgieron problemas de permisos en Windows.

Prompt 2: Error de permisos PostgreSQL
text
"Error al iniciar PostgreSQL en Windows:
'chmod: /var/lib/postgresql/data: Operation not permitted'
'initdb: error: could not change permissions of directory'

¿Cómo solucionar esto en Docker para Windows? El docker-compose.yml actual tiene:
volumes:
  - ./postgres-data:/var/lib/postgresql/data"
Respuesta/Solución:

text
PROBLEMA: Bind mounts en Windows tienen conflictos de permisos NTFS vs Linux.
SOLUCIÓN: Cambiar a named volumes:

# MAL (bind mount)
volumes:
  - ./postgres-data:/var/lib/postgresql/data

# BIEN (named volume)  
volumes:
  - postgres_data:/var/lib/postgresql/data

Y añadir al final:
volumes:
  postgres_data:
Prompt 3: Configuración de red y dependencias
text
"Actualiza este docker-compose.yml para:
1. Instalar automáticamente dependencias Python en los contenedores Spark
2. Asegurar que Spark Worker espere a que Master esté listo
3. Manejar problemas de permisos en Windows
Dependencias necesarias: pandas, numpy, scikit-learn, matplotlib, seaborn, sqlalchemy, psycopg2-binary"
Respuesta/Solución:

yaml
spark-master:
  image: apache/spark:3.5.4-python3
  user: root  # Temporal para instalación
  command: >
    bash -c "
    # Instalar dependencias como root
    pip install --no-cache-dir pandas numpy scikit-learn matplotlib seaborn sqlalchemy psycopg2-binary &&
    # Cambiar a usuario spark y ejecutar
    exec su spark -c '/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master -h spark-master'
    "
📋 BLOQUE B: PIPELINE ETL
Prompt 4: Creación del pipeline.py completo
text
"Escribe un pipeline.py para PySpark que:
1. Cargue dataset QoG desde CSV
2. Filtre 20 países específicos para 2019
3. Cree variables derivadas: Liberal_gap = (vdem_polyarchy - vdem_libdem)
4. Aplique transformación logarítmica al PIB
5. Guarde resultados en PostgreSQL
6. Realice clustering K-Means con método del codo
7. Aplique PCA para visualización 2D

Países: Canada, Uruguay, Haiti, Chile, Cuba, Norway, Poland, Moldova, Netherlands, Belarus, Singapore, Kuwait, Japan, Viet Nam, India, Botswana, Rwanda, South Africa, Ethiopia, Mauritius

Variables: vdem_polyarchy, ti_cpi, wdi_expedu, wdi_gdpcapcon2015, vdem_libdem

Año: 2019"
Respuesta/Solución:
Se proporcionó pipeline.py completo de ~400 líneas con todas las funciones ETL + clustering + visualización.

Prompt 5: Error de conexión PostgreSQL desde Spark
text
"En mi pipeline.py tengo error de conexión a PostgreSQL. Configuración actual:
POSTGRES_CONFIG = {'host': 'localhost', 'port': 5432, ...}

Los contenedores están en Docker Compose:
- postgres (servicio PostgreSQL)
- spark-master (servicio Spark)

¿Debo usar 'localhost' o 'postgres' como host? ¿Cómo configurar la conexión correctamente?"
Respuesta/Solución:

text
DENTRO de la red Docker, los servicios se comunican por NOMBRE de servicio, no 'localhost'.

# MAL
POSTGRES_CONFIG = {'host': 'localhost', ...}

# BIEN
POSTGRES_CONFIG = {'host': 'postgres', ...}  # Nombre del servicio en docker-compose
Prompt 6: Manejo de rutas en contenedores
text
"Mi pipeline.py no encuentra el archivo qog.csv. Rutas:
- En Windows: D:\db_docker\data\qog.csv
- En contenedor Spark: montado como volumen ./data:/opt/data

¿Cuál debe ser la ruta en el código Python dentro del contenedor?
Actualmente uso: filepath = 'D:/db_docker/data/qog.csv' pero no funciona."
Respuesta/Solución:

text
La ruta debe ser la INTERNA del contenedor, no la de Windows.

# MAL (ruta Windows)
filepath = "D:/db_docker/data/qog.csv"

# BIEN (ruta dentro del contenedor)
filepath = "/opt/data/qog.csv"
📋 BLOQUE C: ERRORES DE SINTAXIS Y DEPENDENCIAS
Prompt 7: Error de sintaxis en SparkSession
text
"Error en pipeline.py:
  File "/opt/spark-apps/pipeline.py", line 74
    .master(spark://spark-master:7077) 
                     ^
SyntaxError: invalid syntax

Código actual:
def crear_spark_session():
    spark = SparkSession.builder \
        .appName("QoG_Clustering_Analysis") \
        .master(spark://spark-master:7077) 
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

¿Cuál es el error y cómo corregirlo?"
Respuesta/Solución:

text
ERRORES IDENTIFICADOS:
1. Faltan comillas: master(spark://...) → master("spark://...")
2. Falta barra invertida al final de línea 74
3. Falta línea: .config("spark.executor.memory", "2g")

CÓDIGO CORREGIDO:
def crear_spark_session():
    spark = SparkSession.builder \
        .appName("QoG_Clustering_Analysis") \
        .master("spark://spark-master:7077") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
Prompt 8: Instalación de dependencias en contenedor
text
"Error al ejecutar pipeline en contenedor Spark:
ModuleNotFoundError: No module named 'pandas'

¿Cómo instalar dependencias en el contenedor apache/spark:3.5.4-python3?
Ya tengo requirements.txt local pero el contenedor no las tiene.

Opciones consideradas:
1. Modificar docker-compose.yml para instalar al iniciar
2. Crear Dockerfile personalizado
3. Instalar manualmente después del inicio