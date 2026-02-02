# Modulo 06: Analisis de Datos de Panel

> **Estado:** Disponible

---

## Descripcion General

Aprenderemos econometria de datos de panel: la combinacion de datos de corte transversal
(paises, individuos) con series temporales (anios). Trabajaremos con modelos de Efectos Fijos,
Efectos Aleatorios y Two-Way Fixed Effects aplicados a problemas reales de ciencias sociales.

**Nivel:** Avanzado
**Tecnologias:** Python, linearmodels, pandas, Altair
**Prerequisitos:** Estadistica basica, regresion lineal

---

## Objetivos de Aprendizaje

- Comprender la estructura de datos de panel (unidad x tiempo)
- Distinguir entre Pooled OLS, Efectos Fijos y Efectos Aleatorios
- Aplicar el Test de Hausman para elegir entre FE y RE
- Implementar Two-Way Fixed Effects (efectos de unidad + tiempo)
- Interpretar Odds Ratios en modelos logisticos
- Calcular efectos marginales en modelos no lineales

---

## Contenido del Modulo

El modulo completo esta en:

```
ejercicios/06_analisis_datos_de_panel/
├── 01_analisis_guns.py              # Panel: leyes de armas y criminalidad
├── 02_analisis_fatality.py          # TWFE: impuesto cerveza vs mortalidad
├── 03_dashboard_educativo.py        # Dashboard interactivo 4 pestanas
├── conceptos_visuales_panel.py      # Visualizaciones conceptuales
├── GUIA_PANEL_DATA.md               # Guia teorica completa
├── grafico_panel_guns.png           # Resultado del analisis
└── requirements.txt                 # linearmodels, altair, etc.
```

---

## Scripts y Analisis

### 01 - Analisis Guns (Leyes de Armas)

Efecto de las leyes de portacion de armas sobre las tasas de criminalidad en EE.UU.
Modelo: Panel OLS con Efectos Fijos por estado.

**Dataset:** Guns (Stock & Watson)
**Metodologia:** Panel OLS con Fixed Effects

### 02 - Analisis Fatality (Mortalidad en Trafico)

Efecto del impuesto a la cerveza sobre la mortalidad por accidentes de trafico.
Modelo: Two-Way Fixed Effects (estado + anio).

**Dataset:** AER Fatalities
**Metodologia:** Two-Way FE (PanelOLS con EntityEffects + TimeEffects)

### 03 - Dashboard Educativo Interactivo

Dashboard con 4 pestanas interactivas para entender visualmente los conceptos:

1. **Pooled OLS:** Slider de heterogeneidad que muestra la Paradoja de Simpson
2. **FE vs RE:** Explicacion y tabla de decision del Test de Hausman
3. **Odds Ratios:** Sliders para explorar probabilidad vs odds vs odds ratio
4. **Efectos Marginales:** Comparacion Lin-Lin, Log-Lin, Log-Log con graficos

---

## Teoria: Conceptos Clave

### Que son los datos de panel?

Datos que combinan **corte transversal** (N unidades) con **serie temporal** (T periodos):

```
| pais | anio | democracia | pib_pc |
|------|------|------------|--------|
| ESP  | 2000 | 0.85       | 24000  |
| ESP  | 2001 | 0.86       | 24500  |
| FRA  | 2000 | 0.88       | 28000  |
| FRA  | 2001 | 0.89       | 28500  |
```

### Pooled OLS vs Fixed Effects vs Random Effects

| Modelo | Supuesto | Cuando usarlo |
|--------|----------|---------------|
| **Pooled OLS** | No hay heterogeneidad individual | Rara vez apropiado |
| **Fixed Effects** | Heterogeneidad correlacionada con X | Ciencias sociales (regla general) |
| **Random Effects** | Heterogeneidad NO correlacionada con X | Encuestas aleatorias |

### Test de Hausman

Decide entre FE y RE:

- **H0:** RE es consistente y eficiente (preferir RE)
- **H1:** Solo FE es consistente (preferir FE)
- Si p-valor < 0.05: usar **Fixed Effects**

---

## Dashboard Interactivo

Puedes explorar los resultados del analisis de panel en el dashboard:

[Ver Dashboard Panel Data - QoG](../dashboards/06_analisis_panel_qog.md){ .md-button .md-button--primary }

El dashboard incluye 5 pestanas: Asia Central, Seguridad Hidrica, Terrorismo, Maghreb y PCA+K-Means.

---

## Recursos

### Documentacion
- [linearmodels Documentation](https://bashtage.github.io/linearmodels/)
- [Altair Documentation](https://altair-viz.github.io/)

### Referencias Teoricas
- Wooldridge, J. M. (2010). Econometric Analysis of Cross Section and Panel Data (2nd ed.). MIT Press.
- Stock, J. H., & Watson, M. W. (2019). Introduction to Econometrics (4th ed.). Pearson.

---

**Curso:** Big Data con Python - De Cero a Produccion
**Profesor:** Juan Marcelo Gutierrez Miranda | @TodoEconometria
**Hash ID:** 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
**Metodologia:** Ejercicios progresivos con datos reales y herramientas profesionales

**Referencias academicas:**

- Wooldridge, J. M. (2010). Econometric Analysis of Cross Section and Panel Data (2nd ed.). MIT Press.
- Stock, J. H., & Watson, M. W. (2019). Introduction to Econometrics (4th ed.). Pearson.
- Baltagi, B. H. (2021). Econometric Analysis of Panel Data (6th ed.). Springer.
