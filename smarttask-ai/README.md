# SmartTask AI — Microservice Machine Learning

Microservice Python **FastAPI** pour prédictions et recommandations logistiques SmartTask.

## Architecture IA SmartTask

| Composant | Rôle |
|-----------|------|
| **Angular** | Interface Manager |
| **Spring Boot** (:9090) | Logique métier + sécurité JWT |
| **SmartTask AI** (:8000) | Prédictions ML / scoring explicable |
| **PostgreSQL** | Données métier (via Spring Boot uniquement) |

```
Manager → Angular → Spring Boot → Python AI → ML → Spring Boot → Angular
```

> Angular ne communique **jamais** directement avec Python.

## Prérequis

- Python 3.11+
- pip / venv

## Installation

```bash
cd smarttask-ai
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env
```

## Lancement

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger : http://localhost:8000/docs
- Health : http://localhost:8000/api/ai/health

## Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/ai/health` | Santé du service |
| GET | `/api/ai/model/status` | État des modèles |
| GET | `/api/ai/metrics` | Métriques runtime |
| POST | `/api/ai/predict/delay` | Risque de retard (ML — modèle requis) |
| POST | `/api/ai/predict/delivery-time` | Temps de livraison (ML — modèle requis) |
| POST | `/api/ai/prioritize/task` | Priorisation (scoring explicable) |
| POST | `/api/ai/recommend/driver` | Recommandation chauffeur (scoring explicable) |
| POST | `/api/ai/detect/anomaly` | Détection d'anomalies |

## Modèles ML

Les modèles sont chargés **au démarrage** depuis `app/models/` :

- `delay_model.pkl` — classification retard (0/1)
- `delivery_time_model.pkl` — régression temps de livraison
- `priority_model.pkl` — (futur)

### Entraînement (Phases 4–6)

```bash
# Tout en une commande
python -m app.ml.train_all

# Ou étape par étape
python -m app.ml.generate_dataset --samples 3000
python -m app.ml.train_delay
python -m app.ml.train_delivery_time
```

**Dataset :** `data/raw/smarttask_delivery_dataset.csv` — **SYNTHETIC_DEV** (prototypage uniquement).

**Derniers résultats (synthétique 3000 lignes) :**

| Modèle | Algorithme retenu | Métrique principale |
|--------|-------------------|---------------------|
| Retard | Logistic Regression | F1 ≈ 0.98, ROC-AUC ≈ 0.99 |
| Temps livraison | XGBoost | MAE ≈ 6.3 min, R² ≈ 0.96 |

Métriques détaillées : `app/models/model_metadata.json`

Tant qu'ils ne sont pas entraînés, les endpoints ML retournent **503**.

## Dataset

- Données réelles : insuffisantes en développement → dataset synthétique documenté (Phase 4)
- Fichier prévu : `data/raw/smarttask_delivery_dataset.csv`

## Tests

```bash
pytest -v
```

## Docker

```bash
docker build -t smarttask-ai .
docker run -p 8000:8000 smarttask-ai
```

## Intégration Spring Boot

Spring Boot appelle ce service via `AI_SERVICE_URL=http://localhost:8000` (Phase 11).

## Limites actuelles

- Recommandation chauffeur et priorisation : **scoring explicable** (pas encore ML)
- Prédiction retard / temps : nécessite entraînement des modèles
- Pas d'accès direct PostgreSQL depuis Python

## Version

1.0.0
