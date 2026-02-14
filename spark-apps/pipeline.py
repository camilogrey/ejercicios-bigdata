"""
spark-apps.py - ETL y Análisis de Clustering para dataset QoG
Objetivo: Analizar 20 países específicos del año 2019 usando K-Means
"""
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, when, lit, log
from pyspark.sql.types import DoubleType
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib

matplotlib.use('Agg')  # ¡IMPORTANTE! Para servidor sin display
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# 1. LISTA DE 20 PAÍSES ESPECÍFICOS (del enunciado)
PAISES_ESTUDIO = [
    # América
    "Canada", "Uruguay", "Haiti", "Chile", "Cuba",
    # Europa
    "Norway", "Poland", "Moldova", "Netherlands", "Belarus",
    # Asia
    "Singapore", "Kuwait", "Japan", "Viet Nam", "India",
    # África
    "Botswana", "Rwanda", "South Africa", "Ethiopia", "Mauritius"
]

# 2. VARIABLES PARA EL MODELO (5 variables finales)
VARIABLES_MODELO = [
    'vdem_polyarchy',  # Calidad democrática
    'ti_cpi',  # Índice de percepción de corrupción (Transparency International)
    'wdi_expedu',  # Gasto en educación (% del PIB)
    'wdi_gdpcapcon2015',  # PIB per cápita (para transformación logarítmica)
    'vdem_libdem'  # Democracia liberal (para calcular Liberal_gap)
]

# 3. AÑO DE ESTUDIO
ANIO_ESTUDIO = 2019

# 4. CONFIGURACIÓN DE BASE DE DATOS (¡CORREGIDO! usa 'postgres' no 'localhost')
POSTGRES_CONFIG = {
    'host': 'postgres',  # ¡CORRECCIÓN! Nombre del servicio en docker-compose
    'port': 5432,
    'database': 'qog_db',
    'user': 'spark_user',
    'password': 'spark_pass',
    'table_raw': 'qog_raw',
    'table_processed': 'qog_processed',
    'table_results': 'clustering_results'
}

# 5. RUTAS PARA GUARDAR ARCHIVOS EN CONTENEDOR
OUTPUT_PATH = "/opt/spark-apps/"


# ============================================================================
# FUNCIÓN PRINCIPAL - PIPELINE ETL
# ============================================================================

def crear_spark_session():
    """Crea y configura la SparkSession"""
    spark = SparkSession.builder \
        .appName("QoG_Clustering_Analysis") \
        .master("spark://spark-master:7077") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    print("✓ SparkSession creada exitosamente")
    return spark



def cargar_datos(spark, filepath):
    """Carga el dataset QoG desde CSV"""
    print(f"\n📂 Cargando dataset desde: {filepath}")

    # Leer CSV con inferencia de schema
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("encoding", "UTF-8") \
        .csv(filepath)

    print(f"✓ Dataset cargado: {df.count()} filas, {len(df.columns)} columnas")

    # Mostrar esquema para debugging
    print("Esquema del dataset:")
    df.printSchema()

    return df


def filtrar_datos(df):
    """Filtra los 20 países específicos para el año 2019"""
    print(f"\n🔍 Filtrando datos para {len(PAISES_ESTUDIO)} países en {ANIO_ESTUDIO}")

    # Asegurar que la columna de año sea numérica
    df = df.withColumn("year", col("year").cast("int"))

    # Filtrar por año y países
    df_filtrado = df.filter(
        (col("year") == ANIO_ESTUDIO) &
        (col("cname").isin(PAISES_ESTUDIO))
    )

    # Seleccionar columnas relevantes
    columnas_necesarias = ['cname', 'ccodealp', 'year'] + VARIABLES_MODELO
    columnas_disponibles = [c for c in columnas_necesarias if c in df.columns]
    df_filtrado = df_filtrado.select(columnas_disponibles)

    print(f"✓ Datos filtrados: {df_filtrado.count()} países encontrados")
    print(f"  Columnas seleccionadas: {columnas_disponibles}")

    # Mostrar países encontrados
    if df_filtrado.count() > 0:
        paises_encontrados = df_filtrado.select("cname").distinct().collect()
        print(f"  Países encontrados: {[row.cname for row in paises_encontrados]}")
    else:
        print("  ⚠️  ¡ADVERTENCIA! No se encontraron datos para los países seleccionados")
        # Mostrar países disponibles para debugging
        paises_disponibles = df.filter(col("year") == ANIO_ESTUDIO).select("cname").distinct().limit(10).collect()
        print(f"  Algunos países disponibles en {ANIO_ESTUDIO}: {[row.cname for row in paises_disponibles]}")

    return df_filtrado


def ingenieria_variables(df):
    """Crea variables derivadas para el análisis"""
    print("\n⚙️  Aplicando ingeniería de variables...")

    # Verificar que las columnas necesarias existan
    columnas_requeridas = ['vdem_polyarchy', 'vdem_libdem', 'wdi_gdpcapcon2015']
    columnas_faltantes = [c for c in columnas_requeridas if c not in df.columns]

    if columnas_faltantes:
        print(f"  ⚠️  Columnas faltantes: {columnas_faltantes}")
        print(f"  Columnas disponibles: {df.columns}")
        raise ValueError(f"Columnas requeridas faltantes: {columnas_faltantes}")

    # 1. Calcular Liberal_gap = (vdem_polyarchy - vdem_libdem)
    df = df.withColumn(
        "Liberal_gap",
        col("vdem_polyarchy") - col("vdem_libdem")
    )

    # 2. Transformación logarítmica del PIB (agregar 1 para evitar log(0))
    df = df.withColumn(
        "wdi_gdpcapcon2015_log",
        log(col("wdi_gdpcapcon2015") + 1)
    )

    # 3. Reemplazar valores null
    df = df.fillna(0, subset=["Liberal_gap", "ti_cpi", "wdi_expedu"])

    # 4. Seleccionar variables finales para el modelo
    variables_finales = [
        'cname', 'ccodealp', 'year',
        'vdem_polyarchy',
        'ti_cpi',
        'wdi_expedu',
        'wdi_gdpcapcon2015_log',
        'Liberal_gap'
    ]

    df_final = df.select(variables_finales)

    # 5. Eliminar filas con valores nulos en variables críticas
    df_final = df_final.dropna(
        subset=['vdem_polyarchy', 'ti_cpi', 'wdi_gdpcapcon2015_log']
    )

    print("✓ Variables derivadas creadas:")
    print(f"  - Liberal_gap = vdem_polyarchy - vdem_libdem")
    print(f"  - PIB transformado logarítmicamente (log(PIB+1))")
    print(f"  - Datos finales: {df_final.count()} filas, {len(df_final.columns)} columnas")

    # Mostrar estadísticas descriptivas
    print("  Estadísticas descriptivas:")
    df_final.select('vdem_polyarchy', 'ti_cpi', 'wdi_gdpcapcon2015_log').describe().show()

    return df_final


def guardar_postgres(df, table_name):
    """Guarda DataFrame de Spark en PostgreSQL"""
    print(f"\n💾 Guardando datos en PostgreSQL ({table_name})...")

    # Convertir a Pandas para facilitar la carga en PostgreSQL
    pandas_df = df.toPandas()

    # Crear conexión a PostgreSQL
    connection_str = (
        f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}"
        f"@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}"
        f"/{POSTGRES_CONFIG['database']}"
    )

    engine = create_engine(connection_str)

    # Verificar conexión primero
    try:
        with engine.connect() as conn:
            print(f"  ✅ Conexión a PostgreSQL exitosa en {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}")
    except Exception as e:
        print(f"  ❌ Error conectando a PostgreSQL: {e}")
        print(f"  Cadena de conexión: {connection_str.replace(POSTGRES_CONFIG['password'], '*****')}")
        raise

    # Guardar en PostgreSQL
    pandas_df.to_sql(
        table_name,
        engine,
        if_exists='replace',
        index=False
    )

    print(f"✓ Datos guardados en tabla '{table_name}' ({len(pandas_df)} filas)")
    return pandas_df


# ============================================================================
# ANÁLISIS DE CLUSTERING (BLOQUE C)
# ============================================================================

def preparar_datos_ml(pandas_df):
    """Prepara datos para Machine Learning"""
    print("\n🤖 Preparando datos para análisis de clustering...")

    # 1. Variables para el modelo (excluyendo identificadores)
    variables_ml = [
        'vdem_polyarchy',
        'ti_cpi',
        'wdi_expedu',
        'wdi_gdpcapcon2015_log',
        'Liberal_gap'
    ]

    # Verificar que tenemos datos suficientes
    if len(pandas_df) < 3:
        raise ValueError(f"Insuficientes datos para clustering. Solo {len(pandas_df)} muestras disponibles.")

    # 2. Extraer matriz de características
    X = pandas_df[variables_ml].values

    # 3. Normalizar con StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(f"✓ Datos preparados: {X_scaled.shape[0]} muestras, {X_scaled.shape[1]} características")
    return X_scaled, variables_ml, pandas_df


def metodo_del_codo(X_scaled, max_k=8):
    """Aplica el método del codo para determinar K óptimo y genera gráfico INTERACTIVO con Plotly"""
    print("\n📈 Aplicando método del codo...")

    inertias = []
    K_range = range(1, min(max_k, len(X_scaled)) + 1)

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

    # Crear figura con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(K_range),
        y=inertias,
        mode='lines+markers',
        marker=dict(size=10, color='blue'),
        line=dict(width=2, color='blue'),
        name='Inercia'
    ))

    fig.update_layout(
        title='Método del Codo para Determinar K Óptimo',
        xaxis_title='Número de Clusters (K)',
        yaxis_title='Inercia',
        hovermode='x',
        template='plotly_white',
        width=800,
        height=500
    )

    # Guardar versión ESTÁTICA (PNG) - con matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(K_range, inertias, 'bo-')
    plt.xlabel('Número de Clusters (K)')
    plt.ylabel('Inercia')
    plt.title('Método del Codo para Determinar K Óptimo')
    plt.grid(True, alpha=0.3)
    output_file_png = os.path.join(OUTPUT_PATH, 'elbow_method.png')
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico estático guardado como '{output_file_png}'")

    # Guardar versión INTERACTIVA (HTML) con Plotly
    output_file_html = os.path.join(OUTPUT_PATH, 'elbow_method_interactivo.html')
    fig.write_html(output_file_html)
    print(f"✓ Gráfico INTERACTIVO guardado como '{output_file_html}'")

    # Sugerir K óptimo
    if len(inertias) > 3:
        diffs = np.diff(inertias)
        if len(diffs) > 2:
            diffs_ratios = diffs[1:] / diffs[:-1]
            k_optimo = np.argmin(diffs_ratios) + 2
            k_optimo = max(2, min(k_optimo, len(X_scaled) // 2))
        else:
            k_optimo = 2
    else:
        k_optimo = 2

    print(f"  K óptimo sugerido: {k_optimo}")
    return k_optimo, inertias


def aplicar_kmeans(X_scaled, n_clusters):
    """Aplica algoritmo K-Means"""
    print(f"\n🎯 Aplicando K-Means con K={n_clusters}...")

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    print(f"✓ K-Means completado - {n_clusters} clusters creados")
    print(f"  Inercia: {kmeans.inertia_:.2f}")

    return kmeans, clusters


def aplicar_pca_y_visualizar(X_scaled, clusters, pandas_df, kmeans):
    """Aplica PCA y crea visualización 2D INTERACTIVA con Plotly"""
    print("\n📊 Aplicando PCA y creando visualización...")

    # 1. Aplicar PCA para reducir a 2 dimensiones
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # 2. Crear DataFrame para visualización
    viz_df = pandas_df.copy()
    viz_df['cluster'] = clusters
    viz_df['PC1'] = X_pca[:, 0]
    viz_df['PC2'] = X_pca[:, 1]
    viz_df['cluster_str'] = 'Cluster ' + viz_df['cluster'].astype(str)

    # Calcular varianza explicada
    var_exp = pca.explained_variance_ratio_ * 100

    # 3. Crear gráfico con Plotly
    fig = px.scatter(
        viz_df,
        x='PC1',
        y='PC2',
        color='cluster_str',
        text='cname',
        hover_data={
            'cname': True,
            'cluster': True,
            'PC1': ':.3f',
            'PC2': ':.3f',
            'vdem_polyarchy': ':.3f',
            'ti_cpi': ':.1f',
            'wdi_gdpcapcon2015_log': ':.2f',
            'Liberal_gap': ':.3f'
        },
        title=f'Clustering de Países (K={len(np.unique(clusters))})<br>PCA de 5 variables a 2 dimensiones',
        labels={
            'PC1': f'PC1 ({var_exp[0]:.1f}% varianza)',
            'PC2': f'PC2 ({var_exp[1]:.1f}% varianza)',
            'cluster_str': 'Cluster',
            'cname': 'País'
        }
    )

    # Personalizar el gráfico
    fig.update_traces(
        textposition='top center',
        marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey'))
    )

    fig.update_layout(
        hovermode='closest',
        template='plotly_white',
        width=900,
        height=700,
        showlegend=True,
        title_x=0.5
    )

    # Añadir anotación con varianza total
    fig.add_annotation(
        xref='paper', yref='paper',
        x=0.5, y=-0.15,
        text=f'Varianza explicada total: {pca.explained_variance_ratio_.sum()*100:.1f}%',
        showarrow=False,
        font=dict(size=12, color='gray')
    )

    # Guardar versión ESTÁTICA (PNG) - con matplotlib
    plt.figure(figsize=(14, 10))
    scatter = plt.scatter(
        X_pca[:, 0], X_pca[:, 1],
        c=clusters, cmap='viridis', s=200, alpha=0.8,
        edgecolors='black', linewidth=1
    )
    for i, row in viz_df.iterrows():
        plt.annotate(row['cname'], (row['PC1'], row['PC2']),
                    fontsize=9, ha='center', va='center', fontweight='bold')
    plt.xlabel(f'PC1 ({var_exp[0]:.1f}%)', fontsize=12)
    plt.ylabel(f'PC2 ({var_exp[1]:.1f}%)', fontsize=12)
    plt.title(f'Clustering de Países (K={len(np.unique(clusters))})', fontsize=14)
    plt.colorbar(scatter, label='Cluster')
    plt.grid(True, alpha=0.3)
    plt.figtext(0.5, 0.01, f'Varianza total: {pca.explained_variance_ratio_.sum()*100:.1f}%',
                ha='center', fontsize=10, style='italic')

    output_file_png = os.path.join(OUTPUT_PATH, 'clustering_pca.png')
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico estático guardado como: {output_file_png}")

    # Guardar versión INTERACTIVA (HTML) con Plotly
    output_file_html = os.path.join(OUTPUT_PATH, 'clustering_pca_interactivo.html')
    fig.write_html(output_file_html)
    print(f"✓ Gráfico INTERACTIVO guardado como: {output_file_html}")

    print(f"  Varianza explicada: PC1={var_exp[0]:.1f}%, PC2={var_exp[1]:.1f}%, "
          f"Total={pca.explained_variance_ratio_.sum()*100:.1f}%")

    return viz_df, X_pca, pca


def analizar_clusters(viz_df, variables_ml):
    """Analiza y describe los clusters encontrados"""
    print("\n🔍 Analizando características de cada cluster...")

    # Calcular promedios por cluster
    cluster_stats = viz_df.groupby('cluster')[variables_ml].mean()

    # Añadir conteo de países
    cluster_stats['n_paises'] = viz_df.groupby('cluster').size()
    cluster_stats['paises'] = viz_df.groupby('cluster')['cname'].apply(list)

    print("\n📊 ESTADÍSTICAS POR CLUSTER:")
    print("=" * 80)

    for cluster_id in sorted(cluster_stats.index):
        stats = cluster_stats.loc[cluster_id]

        print(f"\nCLUSTER {cluster_id} ({stats['n_paises']} países):")
        print(f"Países: {', '.join(stats['paises'])}")
        print("-" * 40)

        # Interpretar características
        if stats['vdem_polyarchy'] > 0.7:
            demo_level = "Democracia alta"
        elif stats['vdem_polyarchy'] > 0.4:
            demo_level = "Democracia media"
        else:
            demo_level = "Democracia baja"

        if stats['ti_cpi'] > 70:
            corrup_level = "Baja corrupción"
        elif stats['ti_cpi'] > 40:
            corrup_level = "Corrupción media"
        else:
            corrup_level = "Alta corrupción"

        print(f"• {demo_level} (vdem_polyarchy: {stats['vdem_polyarchy']:.3f})")
        print(f"• {corrup_level} (ti_cpi: {stats['ti_cpi']:.1f})")
        print(f"• PIB per cápita (log): {stats['wdi_gdpcapcon2015_log']:.2f}")
        print(f"• Gasto en educación: {stats['wdi_expedu']:.2f}% del PIB")
        print(f"• Liberal gap: {stats['Liberal_gap']:.3f}")

    print("\n" + "=" * 80)

    # Guardar estadísticas en CSV
    output_file = os.path.join(OUTPUT_PATH, 'cluster_statistics.csv')
    cluster_stats.to_csv(output_file)
    print(f"✓ Estadísticas guardadas en '{output_file}'")

    return cluster_stats


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todo el spark-apps"""
    print("=" * 80)
    print("🚀 INICIANDO PIPELINE ETL + ANÁLISIS DE CLUSTERING")
    print("=" * 80)

    try:
        # ====================================================================
        # BLOQUE B: PIPELINE ETL
        # ====================================================================
        print("\n" + "=" * 80)
        print("📦 BLOQUE B: PIPELINE ETL")
        print("=" * 80)

        # 1. Crear SparkSession
        spark = crear_spark_session()

        # 2. Cargar datos
        filepath = "/opt/data/qog.csv"  # Ruta dentro del contenedor
        df_raw = cargar_datos(spark, filepath)

        # 3. Filtrar datos
        df_filtrado = filtrar_datos(df_raw)

        if df_filtrado.count() == 0:
            print("\n❌ No se encontraron datos para los países seleccionados.")
            print("   Verifica que el archivo qog.csv tenga los países correctos.")
            spark.stop()
            return

        # 4. Ingeniería de variables
        df_final = ingenieria_variables(df_filtrado)

        # 5. Guardar en PostgreSQL
        pandas_df = guardar_postgres(df_final, POSTGRES_CONFIG['table_processed'])

        # ====================================================================
        # BLOQUE C: ANÁLISIS DE CLUSTERING
        # ====================================================================
        print("\n" + "=" * 80)
        print("🔬 BLOQUE C: ANÁLISIS DE CLUSTERING")
        print("=" * 80)

        # 6. Preparar datos para ML
        X_scaled, variables_ml, pandas_df = preparar_datos_ml(pandas_df)

        # 7. Método del codo
        k_optimo, inertias = metodo_del_codo(X_scaled, max_k=min(8, len(pandas_df)))
        print(f"\n💡 K seleccionado: {k_optimo}")

        # 8. Aplicar K-Means
        kmeans, clusters = aplicar_kmeans(X_scaled, n_clusters=k_optimo)

        # 9. PCA y visualización
        viz_df, X_pca, pca = aplicar_pca_y_visualizar(X_scaled, clusters, pandas_df, kmeans)

        # 10. Analizar clusters
        cluster_stats = analizar_clusters(viz_df, variables_ml)

        # 11. Guardar resultados finales
        results_file = os.path.join(OUTPUT_PATH, 'clustering_results.csv')
        viz_df.to_csv(results_file, index=False)
        print(f"✓ Resultados guardados en '{results_file}'")

        # Guardar en PostgreSQL
        spark_df_results = spark.createDataFrame(viz_df)
        guardar_postgres(spark_df_results, POSTGRES_CONFIG['table_results'])

        # ====================================================================
        # RESULTADOS FINALES
        # ====================================================================
        print("\n" + "=" * 80)
        print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
        print("=" * 80)

        print(f"\n📈 RESULTADOS:")
        print(f"• Países analizados: {len(pandas_df)}")
        print(f"• Clusters identificados: {len(np.unique(clusters))}")
        print(f"• Varianza explicada por PCA: {pca.explained_variance_ratio_.sum():.1%}")
        print(f"• Archivos generados en {OUTPUT_PATH}:")
        print(f"  1. elbow_method.png - Método del codo")
        print(f"  2. clustering_pca.png - Visualización 2D de clusters")
        print(f"  3. clustering_results.csv - Resultados completos")
        print(f"  4. cluster_statistics.csv - Estadísticas por cluster")

        print(f"\n🗄️  Datos guardados en PostgreSQL ({POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}):")
        print(f"  • Tabla '{POSTGRES_CONFIG['table_processed']}': Datos procesados")
        print(f"  • Tabla '{POSTGRES_CONFIG['table_results']}': Resultados clustering")

        # Detener Spark
        spark.stop()
        print("\n🎉 ¡Análisis completado! Revisa los archivos generados.")

    except Exception as e:
        print(f"\n❌ ERROR en el spark-apps: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    main()