# The Data Behind the Ball — Football Player Analytics

Multivariate statistical analysis of football player performance in the 2022-2023 season across Europe's Big 5 leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1).

📄 [Full Report: Los Datos detrás del Balón (Spanish)](./docs/Proyecto_Los_Datos_detras_del_Balon.pdf)

Project developed for the course **Métodos y Diseño de Programas I (MDP I)** in the Bachelor's Degree in Data Science at the Universitat Politècnica de València (UPV).

---

## Project Structure

```
├── data/
│   ├── 2022-2023_Football_Player_Stats_original.xlsx    # Original Kaggle dataset
│   ├── 2022-2023_Football_Player_Stats.xlsx             # Cleaned dataset
│   └── nombres_valores.xlsx                             # Market values (Transfermarkt)
├── scripts/
│   └── besoccer_scraping.py                             # Early scraping attempt (BeSoccer), not used in the final dataset
├── notebooks/
│   └── Proyecto.Rmd                                     # Full analysis in R
├── docs/
│   └── Proyecto_Los_Datos_detras_del_Balon.pdf          # Project report
└── README.md
```

---

## Overview

Starting from a dataset of **2,689 players** (filtered to ~1,920 after cleaning), the project applies multivariate analysis techniques to:

1. **Segment players by playing style** using PCA and Clustering
2. **Predict a player's number of goals** from their statistics (PLS Regression)
3. **Classify market value** (High / Medium / Low) using Linear Discriminant Analysis

---

## Methodology

### 1. Preprocessing and Cleaning

- Removed players with < 5 matches or < 200 minutes (not representative)
- Removed goalkeepers (no relevant variables for the offensive/defensive analysis)
- Deduplicated players transferred mid-season
- Regrouped positions into 5 categories: DF, CAR, MF, MCO, FW
- Added **market value** from Transfermarkt (Sept. 2022), collected manually with AI assistance to speed up the process

### 2. Principal Component Analysis (PCA)

- **4 principal components** retained
- **Dim 1-2**: Clearly separate players by position (defensive vs offensive)
- **Dim 3-4**: Correlated with market value
- Validation with **Hotelling's T²** (28 outliers at 99%, including De Bruyne, Kroos, Mbappé) and **SCR** (distance to the model)
- Outliers are exceptional players, not errors → kept in the analysis

### 3. Clustering

Several methods were compared to segment players by playing style:

| Method | Clusters | Result |
|---|---|---|
| Ward (hierarchical) | 4 | Good separation but unbalanced clusters |
| Average (hierarchical) | 5 | Discarded — 1,792 players in a single cluster |
| **K-Means** | **3** | **Best balance and highest interpretability** |
| K-Medoids (PAM) | 4 | Lower silhouette than K-Means |

**The 3 clusters identified by K-Means:**

- **Cluster 1 — Defensive**: High in clearances, blocks, aerial duels. Lowest average market value
- **Cluster 2 — Mixed/Midfielders**: Balance between offensive and defensive actions. Medium market value
- **Cluster 3 — Offensive**: High in goals, shots, dribbles, touches in the opponent's box. Highest average market value

Hopkins statistic: 0.79–0.81 → clustering tendency confirmed.

### 4. Linear Discriminant Analysis (LDA)

Classification of players into 3 market value levels (High / Medium / Low):

| Metric | Training | Test |
|---|---|---|
| **Accuracy** | 97.36% | 96.66% |
| **Kappa** | 0.926 | 0.905 |

High-value players stand out in offensive actions (goals, assists, shots, touches in the opponent's box, dribbles). Low-value players are associated with less visible defensive roles. Separation along the LD1 axis is very clear between the three groups.

### 5. PLS Regression — Goal Prediction

PLS model with 3 latent components to predict goals from individual statistics:

| Metric | Value |
|---|---|
| R²Y | 0.658 |
| Q² (cross-validation) | 0.642 |
| RMSE | 1.35 goals |

Offensive variables (shots, shot-creating actions, touches in the opponent's box) are the most influential in predicting goals. The RMSE is computed on the training data and represents ~91% of the mean goals per player, so the model captures general trends but its individual-level precision is limited.

---

## Data Sources

- **[Kaggle — 2022/2023 Football Player Stats](https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats)** (based on FBref data)
- **Market values**: Transfermarkt (September 2022), collected manually with AI assistance

---

## Technologies

**R** — FactoMineR · factoextra · dplyr · corrplot · cluster · NbClust · MASS (LDA) · ropls (PLS) · caret · ggplot2 · viridis

**Python** — Early market-value scraping attempt (Selenium, BeautifulSoup), not used in the final dataset

---

## Usage

Open `notebooks/Proyecto.Rmd` in RStudio and click **Knit** to generate the full report.

> **Note:** the notebook reads the Excel files by name only, so set the working directory to `data/` (or copy the Excel files next to the `.Rmd`) before knitting.

```r
install.packages(c("readxl", "dplyr", "FactoMineR", "factoextra", "corrplot",
                   "gridExtra", "stringr", "writexl", "stringdist",
                   "cluster", "ggsci", "caret", "knitr",
                   "ggplot2", "viridis", "MASS", "NbClust", "clValid"))

if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("ropls")
```

---

## Team

Although each task had a lead, all members contributed equally and helped across every part of the project.

| Member | Contribution |
|---|---|
| **Jorge Acín Zurita** | Discriminant analysis, PLS regression, visualization, market value data collection |
| Germán Ríos-Capapé Gómez | Discriminant analysis, PLS regression, visualization, market value data collection |
| Mihai Cristian Mihalache Farcas | Cleaning, PCA, Clustering |
| Robert Torres Mingarro | Discriminant analysis, PLS regression, visualization, market value data collection |
| Rubén Tormo Piles | Cleaning, PCA, Clustering |

---

Academic project — Bachelor's Degree in Data Science, Universitat Politècnica de València (UPV).

[![LinkedIn](https://img.shields.io/badge/LinkedIn-jorgeacin-blue?logo=linkedin)](https://linkedin.com/in/jorgeacin)
[![GitHub](https://img.shields.io/badge/GitHub-JorgeAcin-black?logo=github)](https://github.com/JorgeAcin)
