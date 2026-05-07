# Los Datos detrás del Balón — Análisis de Jugadores de Fútbol

Análisis estadístico multivariante del rendimiento de futbolistas de la temporada 2022-2023 en las 5 grandes ligas europeas (Premier League, La Liga, Bundesliga, Serie A, Ligue 1).

📄 Memoria completa: `docs/Proyecto_Los_Datos_detras_del_Balon.pdf`

Proyecto desarrollado en la asignatura **Métodos y Diseño de Programas I (MDP I)** del Grado en Ciencia de Datos de la Universitat Politècnica de València (UPV).

---

## Estructura del Proyecto

```
├── data/
│   ├── 2022-2023_Football_Player_Stats_original.xlsx    # Dataset original de Kaggle
│   ├── 2022-2023_Football_Player_Stats.xlsx             # Dataset tras limpieza
│   └── nombres_valores.xlsx                             # Valores de mercado (Transfermarkt)
├── scripts/
│   └── besoccer_scraping.py                             # Scraping de valores de mercado
├── notebooks/
│   └── Proyecto.Rmd                                     # Análisis completo en R
├── docs/
│   └── Proyecto_Los_Datos_detras_del_Balon.pdf          # Memoria del proyecto
└── README.md
```

---

## Descripción General

A partir de un dataset de **2.689 jugadores** (filtrado a ~1.920 tras limpieza), el proyecto aplica técnicas de análisis multivariante para:

1. **Segmentar jugadores por estilo de juego** mediante PCA y Clustering
2. **Predecir el número de goles** de un jugador a partir de sus estadísticas (PLS Regression)
3. **Clasificar el valor de mercado** (Alto / Medio / Bajo) mediante Análisis Discriminante Lineal

---

## Metodología

### 1. Preprocesado y Limpieza

- Filtrado de jugadores con < 5 partidos o < 200 minutos (no representativos)
- Eliminación de porteros (sin variables relevantes para el análisis ofensivo/defensivo)
- Deduplicación de jugadores con traspasos a mitad de temporada
- Reagrupación de posiciones en 6 categorías: DF, CAR, MF, MCO, FW
- Adición del **valor de mercado** obtenido mediante scraping de Transfermarkt (sept. 2022)

### 2. Análisis de Componentes Principales (PCA)

- **4 componentes principales** retenidas (~50% de varianza explicada)
- **Dim 1-2**: Separan claramente las posiciones de los jugadores (defensivos vs ofensivos)
- **Dim 3-4**: Correlacionadas con el valor de mercado
- Validación con **T² de Hotelling** (28 jugadores atípicos al 99%, incluyendo De Bruyne, Kroos, Mbappé) y **SCR** (distancia al modelo)
- Los atípicos son jugadores excepcionales, no errores → se mantienen en el análisis

### 3. Clustering

Se compararon múltiples métodos para segmentar jugadores por estilo de juego:

| Método | Clusters | Resultado |
|---|---|---|
| Ward (jerárquico) | 4 | Buena separación pero clusters desbalanceados |
| Media (jerárquico) | 5 | Descartado — 1.792 jugadores en un solo cluster |
| **K-Means** | **3** | **Mejor equilibrio y mayor interpretabilidad** |
| K-Medoids (PAM) | 3 | Similar a K-Means, menor silhouette |

**Los 3 clusters identificados por K-Means:**

- **Cluster 1 — Defensivos**: Altos en despejes, bloqueos, duelos aéreos. Bajo valor de mercado medio
- **Cluster 2 — Mixtos/Centrocampistas**: Equilibrio entre acciones ofensivas y defensivas. Valor de mercado medio
- **Cluster 3 — Ofensivos**: Altos en goles, tiros, regates, toques en área rival. Mayor valor de mercado medio

Hopkins statistic: 0.79–0.81 → tendencia de agrupamiento confirmada.

### 4. Análisis Discriminante Lineal (LDA)

Clasificación de jugadores en 3 niveles de valor de mercado (Alto / Medio / Bajo):

| Métrica | Entrenamiento | Test |
|---|---|---|
| **Accuracy** | 97.36% | 96.66% |
| **Kappa** | 0.926 | 0.905 |

Los jugadores de valor alto destacan en acciones ofensivas (goles, asistencias, disparos, toques en área rival, regates). Los de valor bajo se asocian a roles defensivos con menor visibilidad. La separación en el eje LD1 es muy clara entre los tres grupos.

### 5. Regresión PLS — Predicción de Goles

Modelo PLS con 3 componentes latentes para predecir goles a partir de estadísticas individuales:

| Métrica | Valor |
|---|---|
| R²Y | 0.658 |
| Q² (validación cruzada) | 0.642 |
| RMSE | 1.35 goles |

Las variables más influyentes en la predicción de goles: tiros a puerta (SoT), goles por tiro (G/Sh), acciones que terminan en tiro (SCA), toques en el área rival (TouAttPen).

---

## Fuentes de Datos

- **[Kaggle — 2022/2023 Football Player Stats](https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats)** (basado en datos de FBref)
- **Valores de mercado**: Transfermarkt (septiembre 2022), obtenidos mediante scraping

---

## Tecnologías

**R** — FactoMineR · factoextra · dplyr · corrplot · cluster · NbClust · MASS (LDA) · ropls (PLS) · caret · randomForest · ggplot2 · viridis

**Python** — Scraping de valores de mercado (requests, pandas)

---

## Uso

Abre `notebooks/Proyecto.Rmd` en RStudio y haz clic en **Knit** para generar el informe completo.

```r
install.packages(c("readxl", "dplyr", "FactoMineR", "factoextra", "corrplot",
                   "gridExtra", "stringr", "writexl", "stringdist",
                   "cluster", "ggsci", "randomForest", "caret", "knitr",
                   "ggplot2", "viridis", "MASS", "NbClust", "clValid"))

if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("ropls")
```

---

## Equipo

Aunque hubiese un responsable de cada tarea, todos los miembros contribuimos por igual y ayudamos en todas las partes del proyecto.

| Miembro | Contribución |
|---|---|
| **Jorge Acín Zurita** | Análisis discriminante, regresión PLS, visualización, scraping |
| Germán Ríos-Capapé Gómez | Análisis discriminante, regresión PLS, visualización, scraping |
| Mihai Cristian Mihalache Farcas | Limpieza, PCA, Clustering |
| Robert Torres Mingarro | Análisis discriminante, regresión PLS, visualización, scraping |
| Rubén Tormo Piles | Limpieza, PCA, Clustering |

---

Proyecto académico — Grado en Ciencia de Datos, Universitat Politècnica de València (UPV).

[![LinkedIn](https://img.shields.io/badge/LinkedIn-jorgeacin-blue?logo=linkedin)](https://linkedin.com/in/jorgeacin)
[![GitHub](https://img.shields.io/badge/GitHub-JorgeAcin-black?logo=github)](https://github.com/JorgeAcin)
