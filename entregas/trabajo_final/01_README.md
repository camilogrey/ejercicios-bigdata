# Análisis de Clustering de Países - Dataset QoG 2019

## 📋 INFORMACIÓN DEL AUTOR

| Campo | Dato                                                            |
|-------|-----------------------------------------------------------------|
| **Nombre** | Camilo García Rey                                               |
| **Fecha** | 10 de febrero de 2026                                           |
| **Asignatura** | Infraestructura de Procesamiento de Datos                       |
| **Proyecto** | Bloque A (30%) + Bloque B (25%) + Bloque C (25%) + Bloque D (20%) |

## 🎯 PREGUNTA DE INVESTIGACIÓN

**¿Cómo se agrupan los países globalmente al cruzar desarrollo económico, calidad democrática y corrupción? ¿Existen perfiles híbridos (ej. países ricos autocráticos o democracias pobres)?**

### Hipótesis inicial:
- Deberían formarse clusters que agrupen países con características similares
- Posibles perfiles híbridos: países con alto PIB pero baja democracia (ej. Singapur, Kuwait)
- Países con alta democracia pero bajo PIB (ej. algunos países de Europa del Este)

## 🌍 CONFIGURACIÓN DEL DATASET

### Año de estudio: **2019**

### Países analizados (20 países de 4 continentes):

| Continente | Países |
|------------|--------|
| **América** | Canada, Uruguay, Haiti, Chile, Cuba |
| **Europa** | Norway, Poland, Moldova, Netherlands, Belarus |
| **Asia** | Singapore, Kuwait, Japan, Viet Nam, India |
| **África** | Botswana, Rwanda, South Africa, Ethiopia, Mauritius |

### Variables seleccionadas:

| Variable | Descripción |
|----------|-------------|
| `vdem_polyarchy` | Índice de democracia electoral (0-1, más alto = más democrático) |
| `ti_cpi` | Índice de percepción de corrupción (0-100, más alto = menos corrupción) |
| `wdi_expedu` | Gasto en educación como % del PIB |
| `wdi_gdpcapcon2015` | PIB per cápita (dólares constantes 2015) |
| `vdem_libdem` | Índice de democracia liberal (para cálculo de brecha) |

## 🏗️ INFRAESTRUCTURA TECNOLÓGICA

### Arquitectura del sistema:
![img_8.png](img_8.png)


### Componentes:

| Componente | Especificación |
|------------|----------------|
| **Sistema Operativo** | Windows (con Docker Desktop) |
| **IDE** | PyCharm con Python 3.14 (local) / Python 3.8.10 (contenedor) |
| **Orquestación** | Docker Compose |
| **Procesamiento** | Apache Spark 3.5.4 (modo cluster) |
| **Base de datos** | PostgreSQL 16 Alpine |
| **Análisis** | scikit-learn (K-Means, PCA) |

## 📊 METODOLOGÍA DE ANÁLISIS

### Fase 1: Infraestructura (Bloque A)
1. Configuración de docker-compose.yml con 3 servicios
2. Named volumes para persistencia de datos PostgreSQL
3. Health checks para verificar disponibilidad
4. Instalación automática de dependencias Python en contenedores Spark

### Fase 2: ETL con PySpark (Bloque B)
1. Carga de dataset QoG desde CSV
2. Filtrado de países específicos para año 2019
3. Ingeniería de variables:
   - `Liberal_gap = vdem_polyarchy - vdem_libdem`
   - `wdi_gdpcapcon2015_log = log(PIB + 1)`
4. Almacenamiento en PostgreSQL (tabla `qog_processed`)

### Fase 3: Análisis de Clustering (Bloque C)
1. Normalización con `StandardScaler`
2. Optimización de K mediante método del codo
3. Aplicación de K-Means con K óptimo
4. Reducción dimensional con PCA a 2 componentes
5. Visualización 2D de clusters con etiquetas de países
6. Análisis de perfiles por cluster

## 🔧 DESAFÍOS TÉCNICOS ENCONTRADOS

### Problemas resueltos durante el desarrollo:

| Problema | Solución |
|----------|----------|
| Permisos PostgreSQL en Windows | Uso de named volumes en lugar de bind mounts |
| Instalación de dependencias en Spark | Ejecución como root temporal + `exec su spark` |
| Error de sintaxis en pipeline.py | Corrección de comillas faltantes y barras invertidas |
| Conexión PostgreSQL desde Spark | Cambio de host: `localhost` → `postgres` |
| Versiones incompatibles Python | Ajuste de requirements para Python 3.8 |

## 📈 RESULTADOS ESPERADOS

El pipeline genera:

1. **Método del codo** (`elbow_method.png`): Gráfico para determinar K óptimo
2. **Visualización PCA** (`clustering_pca.png`): Clusters en espacio 2D
3. **Tabla PostgreSQL** `clustering_results`: Resultados completos
4. **Estadísticas por cluster** (`cluster_statistics.csv`): Promedios por grupo

## 🚀 CÓMO EJECUTAR EL PROYECTO

### Prerrequisitos:
- Docker Desktop instalado y funcionando
- Archivo `qog.csv` en carpeta `data/`
- Git (opcional)

### Pasos de ejecución:

```bash
# 1. Clonar/descargar el proyecto
cd D:\db_docker

# 2. Levantar infraestructura
docker-compose up -d

# 3. Esperar 30 segundos para inicialización
timeout 30

# 4. Verificar estado
docker-compose ps

# 5. Ejecutar pipeline
docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-apps/pipeline.py

# 6. Copiar resultados
docker cp spark-master:/opt/spark-apps/elbow_method.png .
docker cp spark-master:/opt/spark-apps/clustering_pca.png .

D:\bd_docker\
├── data\
│   └── qog.csv                    # Dataset original
├── spark-apps\
│   └── pipeline.py                 # Script principal ETL + clustering
├── resultados_finales\             # Gráficos y CSV generados
│   ├── elbow_method.png
│   ├── clustering_pca.png
│   ├── clustering_results.csv
│   └── cluster_statistics.csv
├── docker-compose.yml              # Orquestación de servicios
├── requirements.txt                # Dependencias Python
├── .gitignore                      # Archivos ignorados por git
├── 01_README.md                    # Este archivo
├── 02_INFRAESTRUCTURA.md           # Documentación Docker
├── 03_RESULTADOS.md                # Análisis y gráficos
├── 04_REFLEXION_IA.md              # Momentos clave y prompts
├── 05_RESPUESTAS.md                # Preguntas de comprensión
└── PROMPTS.md                      # Historial de prompts IA

📊 TECNOLOGÍAS UTILIZADAS
Tecnología	Versión	Propósito
Docker Desktop	20.10+	Contenedores
Docker Compose	3.8	Orquestación
Apache Spark	3.5.4	Procesamiento distribuido
PostgreSQL	16 Alpine	Almacenamiento
Python	3.8 (contenedor)	Lenguaje principal
PySpark	3.5.4	API Spark para Python
pandas	1.5.3	Manipulación de datos
scikit-learn	1.3.2	Clustering y PCA
matplotlib	3.7.4	Visualización
seaborn	0.13.0	Estilo de gráficos


👨‍💻 NOTAS DEL DESARROLLADOR
Este proyecto fue desarrollado en Windows con Docker Desktop, enfrentando desafíos típicos de permisos y compatibilidad entre sistemas. La solución implementada utiliza named volumes para persistencia y ejecución como root temporal para instalación de dependencias.

Principales aprendizajes:

Los bind mounts en Windows tienen limitaciones de permisos

Spark en contenedores requiere manejo cuidadoso de usuarios

La comunicación entre servicios Docker usa nombres de servicio, no localhost

Las versiones de Python en contenedores oficiales son fijas

📧 CONTACTO
Para cualquier consulta sobre este proyecto:

Nombre: Camilo García Rey

Email: camilogrey@gmail.com

GitHub: https://github.com/camilogrey