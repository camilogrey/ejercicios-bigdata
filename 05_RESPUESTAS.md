1. ¿Por qué usar Docker Compose para este proyecto?
Imagínate que tienes que instalar PostgreSQL, Spark, configurar redes, puertos, versiones... en tu ordenador personal. Cada vez que cambias de ordenador o alguien más quiere probar tu proyecto, tienes que repetir todo el proceso y seguro que algo falla. Con Docker Compose, todo queda definido en un archivo de texto.
En mi caso, además, trabajo con Windows. Si hubiera instalado Spark directamente en Windows, habría tenido mil problemas de compatibilidad, variables de entorno, rutas con espacios, permisos... Un dolor de cabeza. En cambio, con Docker, Spark corre en un entorno Linux dentro de mi Windows, pero aislado y controlado. Sin emabrgo es este caso fue aislado en la undad D a trves de un SSD.
cuando terminas el proyecto, simplemente haces docker-compose down y tu ordenador queda limpio. No tienes que desinstalar servicios, limpiar el registro de Windows ni nada raro. si mañana quiero mostrarle mi proyecto a un amigo o al profesor, le paso el docker-compose.yml y el pipeline.py, él ejecuta docker-compose up -d y en 5 minutos tiene el mismo entorno que yo. Eso es reproducible
Docker Compose es como tener una caja con todo lo necesario para que el proyecto funcione en cualquier sitio.
2. ¿Cómo funciona la comunicación entre Spark Master y Worker?
Spark tiene una arquitectura manager-worker El Spark Master es como el jefe de obra: coordina, reparte el trabajo y vigila que todo vaya bien. El Spark Worker es el que realmente hace el trabajo pesado, como los obreros.
Se comunican a través de dos puertos principales:
•	Puerto 7077: Es el canal de comunicación interna. El Worker le dice al Master "estoy vivo, tengo 2 cores y 2GB de RAM disponibles", y el Master le responde "pues toma estos datos y procesalos".
•	Puerto 8080: Es la interfaz web del Master. Tú abres http://localhost:8080 y ves en tiempo real qué workers están conectados, cuánta memoria tienen, qué trabajos están ejecutando. Es como las cámaras de seguridad de la obra.
Cuando el Worker arranca, lo primero que hace es conectarse al Master usando la dirección spark://spark-master:7077. En nuestro docker-compose.yml, pusimos depends_on para que el Worker espere a que el Master esté listo. Pero aún así, a veces el Worker se conecta antes de que el Master termine de iniciar, y hay que esperar un poco.
Lo mejor es cuando ejecutas el pipeline y ves en los logs cosas como "Successfully registered with master". Ahí sabes que la comunicación funciona y que Spark está feliz.
El Worker también tiene su propio puerto web (8081) donde puedes ver sus métricas individuales. Es como si cada obrero tuviera su propia cámara.
3. ¿Por qué aplicar PCA antes de visualizar clustering?
si ya tengo los clusters, ¿por qué complicarme con el PCA?". Pero tiene su explicación.
Resulta que nuestro análisis usa 5 variables: vdem_polyarchy, ti_cpi, wdi_expedu, el log del PIB, y Liberal_gap. Eso significa que cada país es un punto en un espacio de 5 dimensiones. Sin embargo como no podemos visualizar más de 3 dimensiones y las 3 dimensiones ya nos cuestan. ¿Cómo dibujas un punto en 5D?
El PCA (Análisis de Componentes Principales) lo que hace es reducir dimensiones pero intentando perder la menor información posible. Es como cuando tomas una foto de un objeto 3D y la pasas a 2D: pierdes profundidad, pero sigues reconociendo el objeto.
En ese caso, pasamos de 5 variables a 2 componentes principales. En el gráfico que genera el pipeline, pone algo como "PC1 explica un % de la varianza, PC2 otro % de la varianza” Eso significa que con solo esos dos ejes, estamos capturando el 75% de la información original, entre mayor porcentaje de la info capturemos mayor la precisi{on del modelo.
Luego puedes ver los países en un plano 2D, cada uno con su color de cluster, y ves claramente qué países se parecen. Sin PCA, tendríamos que imaginar u espacio de 5 dimensiones
Eso sí, hay que interpretar con cuidado. A veces el PCA puede separar cosas que no son tan distintas en la realidad, o mezclar cosas que sí lo son. Por eso es importante mirar también los números y las variables que tengan asociación entre s{i.
4. ¿Cuál fue el mayor desafío técnico y cómo lo superaste?
Respuesta:
El tema de los permisos para subir archivos a Docker. Me pasó algo muy raro: podía subir el pipeline.py sin problema, pero cuando intentaba subir el archivo de datos (qog.csv), Docker me decía que no tenía permisos. Era como si el contenedor discriminara entre tipos de archivo.
El escenario: Tenía mi carpeta D:\db_docker\data\ con el qog.csv. Usaba el comando docker cp para copiar archivos al contenedor. El pipeline.py se copiaba perfecto, pero el CSV daba error de permisos. Y lo peor es que el CSV era más pequeño que el script, así que no era tema de tamaño.
El error exacto:
text
GetFileAttributesEx D:\db_docker\data\qog.csv: Permission denied
Lo que intenté sin éxito:
•	Ejecutar PowerShell como administrador
•	Dar permisos completos a la carpeta con icacls
•	Mover el CSV a diferentes ubicaciones
•	Cambiar el nombre del archivo
•	Usar rutas absolutas con barras invertidas y barras normales
Nada funcionaba.
La solución: Resulta que el problema no era tan grave como pensaba. Después de dar muchas vueltas, lo que realmente solucionó el problema fueron dos cosas muy simples:
1.	Compartir la unidad en Docker Desktop: En la configuración de Docker Desktop, hay una opción en Settings → Resources → File Sharing. Ahí tienes que asegurarte de que la unidad donde está tu proyecto (en mi caso D:\) esté agregada a la lista de unidades compartidas. Si no está, Docker no puede acceder a los archivos de esa unidad, aunque tú los veas en el explorador de Windows.
2.	Usar rutas con barras normales en lugar de barras invertidas: En PowerShell, en lugar de escribir la ruta como D:\db_docker\data\qog.csv, hay que escribirla con barras normales estilo Linux: D:/db_docker/data/qog.csv. Esto parece una tontería, pero PowerShell interpreta las barras invertidas de manera especial y a veces se lía.
¿Qué aprendí? Que Docker en Windows tiene su propia lógica para manejar permisos y rutas. No es que el disco D:\ fuera malo o que el SSD tuviera problemas. Simplemente hay que decirle explícitamente a Docker Desktop: "oye, esta unidad está autorizada para que los contenedores la vean". Es como cuando en el móvil le das permisos a una app para acceder a tus fotos.
Desde entonces, cada vez que empiezo un proyecto nuevo en Docker:
1.	Abro Docker Desktop y voy a Settings → Resources → File Sharing
2.	Verifico que la unidad donde voy a trabajar esté en la lista
3.	Si no está, la agrego manualmente
4.	Aplico los cambios y reinicio Docker
