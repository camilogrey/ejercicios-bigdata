# Infraestructura Docker - Proyecto QoG Clustering

## Servicios Configurados

### PostgreSQL
- **Imagen:** postgres:16-alpine
- **Puerto:** 5432
- **Base de datos:** qog_db
- **Usuario:** spark_user
- **Contraseña:** spark_pass

### Spark Master
- **Imagen:** apache/spark:3.5.4-python3
- **Puerto UI:** 8080
- **Puerto comunicación:** 7077
- **URL:** spark://spark-master:7077

### Spark Worker
- **Imagen:** apache/spark:3.5.4-python3
- **Cores:** 2
- **Memoria:** 2g
- **Conectado a:** spark://spark-master:7077

## Dependencias Instaladas
- pandas, numpy, scikit-learn
- matplotlib, seaborn
- sqlalchemy, psycopg2-binary

![img.png](img.png)
![img_1.png](img_1.png)
  ![img_2.png](img_2.png)
  ![img_3.png](img_3.png)

## Docker en mis palabras
- Docker es una plataforma que permite administrar contenedores, los cuales empaquetan componentes aislados capaces de interactuar entre sí, facilitando la creación de arquitecturas como las de Apache Spark mediante nodos Master y Workers. Estos contenedores se coordinan según su número y la capacidad asignada de memoria e hilos, donde el Spark Master orquestas el trabajo de los Workers que llevan consigo todas las librerías necesarias para la transformación de datos. Gracias a que incluyen sus propias dependencias y requisitos (como archivos requirements.txt), estos entornos son totalmente portables y ejecutables en cualquier sistema operativo o infraestructura on-premise. Internamente, cada contenedor se basa en una imagen que incluye la copia de Apache Spark, sus límites de hardware, instrucciones de instalación y las rutas de comunicación o volúmenes que definen su área de trabajo. 


