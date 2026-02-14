# RESULTADOS Análisis de Clustering K-Means (2019): Desarrollo, Democracia y Corrupción

## 1. Objeto de Estudio
* **Objetivo:** Realizar un análisis de Clustering (K-Means) para el año 2019 sobre una muestra de 20 países.
* **Pregunta de Investigación:** ¿Cómo se agrupan los países globalmente al cruzar desarrollo económico, calidad democrática y corrupción? ¿Existen perfiles híbridos?

---

## 2. Configuración del Dataset
* **Países de estudio:**
    * **América:** Canada, Uruguay, Haiti, Chile, Cuba.
    * **Europa:** Norway, Poland, Moldova, Netherlands, Belarus.
    * **Asia:** Singapore, Kuwait, Japan, Viet Nam, India.
    * **África:** Botswana, Rwanda, South Africa, Ethiopia, Mauritius.

* **Variables analizadas:**
    1.  `vdem_polyarchy`: Índice de Democracia Electoral.
    2.  `ti_cpi`: Índice de Percepción de la Corrupción.
    3.  `wdi_expedu`: Gasto público en educación (% del PIB).
    4.  `wdi_gdpcapcon2015_log`: Logaritmo del PIB per cápita (precios constantes 2015).
    5.  `Liberal_gap`: Variable derivada (`vdem_polyarchy` - `vdem_libdem`). Mide la carencia de protecciones constitucionales.
    6.  `vdem_libdem`: Democracia Liberal (usada para el cálculo de la brecha).

![img_4.png](img_4.png)
![img_5.png](img_5.png)
![img_6.png](img_6.png)
![img_7.png](img_7.png)

## 3. Interpretación de Resultados

### Método del Codo
* **K=2 óptimo:** Se observa una caída drástica en la inercia de K=1 a K=2.
* **Cohesión:** Esta división maximiza la similitud interna sin sobreajustar el modelo.

### Perfiles de los Clusters
* **Cluster 1 (Amarillo) - Desarrollo e Instituciones Sólidas:**
    * **Perfil:** Altos índices democráticos (0.71) y baja corrupción (67.78).
    * **Economía:** PIB per cápita logarítmico superior (10.12).
    * **Coherencia:** `Liberal_gap` bajo (0.07), indicando instituciones liberales fuertes.
* **Cluster 0 (Morado) - Retos Estructurales:**
    * **Perfil:** Menor desempeño democrático (0.38) y mayor corrupción (42.33).
    * **Economía:** Desarrollo económico inferior (8.05).
    * **Debilidad:** `Liberal_gap` más alto (0.13), reflejando fragilidad en libertades civiles.

### Análisis PCA (Varianza explicada: 77.5%)
* **Eje PC1 (58.7%):** Eje Institucional-Económico (ej. Norway/Canada vs. Haiti/Ethiopia).
* **Eje PC2 (18.8%):** Diferenciador por gasto educativo y brecha liberal.

---

## 4. Identificación de Perfiles Híbridos y Atípicos
* **Singapore y Japan:** Ubicados en Cluster 1. Singapore destaca por compensar su menor democracia (0.41) con una eficiencia económica y CPI excelentes.
* **Cuba:** Caso atípico en Cluster 0. Su altísimo gasto en educación (9.05%) lo separa del resto de países con bajos niveles democráticos.
* **Poland:** Zona de transición. Presenta el `Liberal_gap` más alto (0.18), evidenciando tensiones en su calidad institucional.

---

## 5. Conclusión General
* La riqueza y la democracia suelen converger (Cluster 1).
* El análisis PCA revela matices importantes: países que priorizan eficiencia sobre liberalización (Singapore) o inversión social sobre libertades políticas (Cuba).