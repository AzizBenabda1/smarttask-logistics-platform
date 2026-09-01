# SmartLogix - Rapport PFE (version editable Markdown)

> Version Markdown du rapport. Pour Word : ouvrir dans Word ou `pandoc Rapport_PFE_SmartLogix.md -o Rapport_PFE_SmartLogix.docx`
> PDF genere automatiquement : `python generate_rapport_pfe.py`

**Titre :** SmartLogix - Conception et developpement d'une plateforme intelligente de gestion logistique

**Auteur :** [A completer] | **Encadrant :** [A completer] | **Etablissement :** [A completer]

**Technologies :** Java 17, Spring Boot 4.1, Angular 16, PostgreSQL, Python FastAPI, scikit-learn, XGBoost, JWT, Flyway

---

## Resume executif

SmartLogix est une plateforme logistique multi-acteurs (Admin, Manager, Operator, Driver, Client) avec integration IA : predictions ML, chaine automation 7 etapes, chatbot Copilot, optimisation itineraire et alertes chauffeur.

Architecture : Angular (4200) -> Spring Boot (9090) -> PostgreSQL + Python FastAPI (8000).

**Chiffres cles :** 97 endpoints REST, 11 entites JPA, 10 migrations Flyway, 49 composants Angular, 11 endpoints Python IA.

**Metriques ML (dataset synthetique 3000 lignes) :** retard F1=0.982, ETA MAE=6.3 min, R2=0.96.

---

## Chapitre 1 - Contexte general

### Problematique

Comment concevoir une plateforme multi-acteurs integrant l'IA pour automatiser les livraisons urgentes, predire les retards et assister les utilisateurs ?

### Solution

| Probleme | Solution SmartLogix |
|----------|---------------------|
| Commandes manuelles | Workflow Operator + types produit |
| Assignation | IA + automation express |
| Retards | Prediction ML + alertes proactives |
| Suivi | SSE temps reel |
| Assistance | Chatbot Copilot |

---

## Chapitre 4 - Architecture

```
Utilisateur -> Angular 4200 -> Spring Boot 9090 -> PostgreSQL
                                      |
                                      v
                              Python FastAPI 8000
```

---

## Chapitre 8 - Backend (extrait)

13 controllers, 97 endpoints. Voir `rapport_data.py` pour catalogue complet.

Comptes test :
- admin@smarttask.com / Admin123!
- manager@smarttask.com / Manager123!
- operator1@smarttask.com / Operator123!
- driver1@smarttask.com / Driver123!
- client1@smarttask.com / Client123!

---

## Chapitre 10 - IA

- **delay_model** : Logistic Regression, F1=0.982
- **delivery_time_model** : XGBoost, MAE=6.32 min
- **Automation** : 7 etapes (READ_ORDER -> LOG_COMPLETE)
- **Route chauffeur** : POST /api/ai/optimize/route

Generer modeles : `python -m app.ml.train_all` dans smarttask-ai/

---

## Limites et perspectives

- Dataset synthetique, .pkl non versionnes, Docker partiel (IA seulement)
- Perspectives : CI/CD, docker-compose, donnees reelles ML, app mobile

---

*Document genere depuis le code source reel du projet SmartTask. Ne pas presenter les fonctionnalites futures comme implementees.*
