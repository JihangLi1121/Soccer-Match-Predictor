# ⚽ Soccer Match Predictor

A full-stack machine learning application that predicts the outcomes of soccer matches using historical statistics, head-to-head records, and 2024/25 season data. Built with Python, scikit-learn, and a lightweight web frontend.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Data Pipeline](#data-pipeline)
- [Machine Learning Models](#machine-learning-models)
- [Web Interface](#web-interface)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Development Process](#development-process)
- [Disclaimer](#disclaimer)

---

## Overview

Soccer Match Predictor scrapes live and historical match data from sources like FBref, Sofascore, and Transfermarkt via the **ScraperFC** library, engineers features from team form, head-to-head records, and season calendars, and feeds them into trained ML classifiers to predict win/draw/loss probabilities for upcoming matches. Results are surfaced through a browser-based web interface.

---

## Features

- **Automated data scraping** from FBref, Sofascore, and other sources using ScraperFC
- **Head-to-head (H2H) analysis** across historical matchups between teams
- **2024/25 season calendar integration** for fixture scheduling and form calculation
- **Multiple ML models** trained and compared for prediction accuracy
- **Interactive web frontend** to query upcoming matches and view predictions
- **CI/CD pipeline** via GitHub Actions for automated testing and validation
- **Agile development** tracked with Scrum documentation across sprints

---

## Project Structure

```
Soccer-Match-Predictor/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD pipelines
├── 2425_Calendars/         # 2024/25 season fixture calendars by league
├── H2H_Stats/              # Head-to-head historical match statistics
├── Models/                 # Trained ML model files and training notebooks
├── ScraperFC/              # Data scraping scripts built on the ScraperFC library
├── Scrum_Documents/        # Sprint plans, backlogs, and retrospectives
├── data/                   # Raw and processed datasets (CSV/JSON)
├── web/                    # Frontend: HTML, CSS, JavaScript
├── .gitignore
├── README.md
└── pyguide.pdf             # Python style guide reference
```

---

## Data Pipeline

### 1. Scraping
Data is collected using [ScraperFC](https://github.com/oseymour/ScraperFC), a Python library that pulls structured football data from:

- **FBref** — season-level team and player stats (passing, shooting, defense, etc.)
- **Sofascore** — live scores, match events, and team ratings
- **Transfermarkt / Capology** — squad values and player wage data

> ⚠️ FBref enforces a rate limit of ~10 requests per minute. The scraper includes wait times between requests to stay compliant. Always review the [Sports Reference Terms of Service](https://www.sports-reference.com/data_use.shtml) before scraping.

### 2. Feature Engineering
Raw scraped data is cleaned and transformed into model-ready features:

- **Rolling form** — average stats over the last N matches per team
- **Home/Away splits** — separate performance metrics for home and away fixtures
- **H2H records** — win rate, average goals, and recent results between two sides
- **Season calendar features** — days since last match, fixture congestion, travel distance proxies

### 3. Dataset
Processed data is saved to the `data/` directory as CSVs, split into:

- `train.csv` — historical seasons used for model training
- `test.csv` — holdout set for evaluation
- `upcoming.csv` — current season fixtures for live predictions

---

## Machine Learning Models

Multiple classifiers are trained and compared in the `Models/` directory. Predictions are three-class: **Home Win**, **Draw**, or **Away Win**.

| Model | Notes |
|---|---|
| Logistic Regression | Baseline linear classifier |
| Random Forest | Ensemble of decision trees; robust to noisy features |
| Gradient Boosting | Sequential boosting; typically highest accuracy |
| XGBoost | Optimized gradient boosting with regularization |

### Evaluation Metrics
- Accuracy on held-out test set
- Log-loss (for probabilistic calibration)
- Confusion matrix across Win/Draw/Loss classes

### Training
Model training is done in Jupyter Notebooks inside `Models/`. Trained model artifacts are serialized with `joblib` or `pickle` and loaded by the web backend at inference time.

---

## Web Interface

The `web/` directory contains a browser-based frontend that allows users to:

1. Select a home team and away team from a dropdown
2. Submit a prediction request
3. View win/draw/loss probabilities for the selected matchup

The frontend communicates with a lightweight Python backend (Flask or similar) that loads the trained model and returns a JSON prediction response.

**Stack:**
- HTML / CSS / JavaScript (frontend)
- Python backend serving model predictions
- Chart.js or similar for probability visualization

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/JihangLi1121/Soccer-Match-Predictor.git
cd Soccer-Match-Predictor
pip install -r requirements.txt
```

> If a `requirements.txt` is not present, install core dependencies manually:
> ```bash
> pip install scraperfc scikit-learn pandas numpy jupyter flask
> ```

### Scraping Fresh Data

```bash
cd ScraperFC
python scrape.py  # Adjust league/season parameters inside the script
```

Scraped data will be saved to the `data/` directory.

### Training Models

Open and run the notebooks in `Models/` sequentially:

```bash
jupyter notebook Models/
```

### Running the Web App

```bash
cd web
python app.py  # or: flask run
```

Then open `http://localhost:5000` in your browser.

---

## Usage

1. Launch the web app (`python app.py`)
2. Navigate to `http://localhost:5000`
3. Select a **Home Team** and **Away Team** from the dropdowns
4. Click **Predict**
5. View the probability breakdown for Home Win / Draw / Away Win

---

## Development Process

This project was developed using **Scrum** methodology. Sprint plans, backlogs, and retrospective documents are stored in `Scrum_Documents/`. The team tracked tasks across multiple sprints covering:

- Sprint 1: Data pipeline design and initial scraping
- Sprint 2: Feature engineering and dataset construction
- Sprint 3: Model training, evaluation, and comparison
- Sprint 4: Web frontend integration and CI/CD setup

CI/CD is handled via **GitHub Actions** (`.github/workflows/`) to run automated tests on every push.

---

## Disclaimer

This project is built for **educational and research purposes only**. Predictions are probabilistic estimates based on historical data and do not guarantee future outcomes. This tool should never be used for professional betting, gambling, or any commercial application.

Please respect the terms of service of all data sources used in this project, including FBref, Sofascore, and Transfermarkt.

---

## Acknowledgements

- [ScraperFC](https://github.com/oseymour/ScraperFC) by Owen Seymour — the backbone of the data pipeline
- [FBref](https://fbref.com) — primary source of match and player statistics
- [scikit-learn](https://scikit-learn.org) — model training and evaluation
