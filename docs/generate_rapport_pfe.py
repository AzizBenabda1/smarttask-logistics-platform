# -*- coding: utf-8 -*-
"""
Generateur Rapport PFE SmartLogix - 50+ pages
Base UNIQUEMENT sur le code source reel (SmartTask).
Sortie ASCII pour compatibilite fpdf2 / Helvetica.
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from rapport_data import (
    PROJECT, CODE_NAME, ENDPOINTS, PYTHON_ENDPOINTS,
    ANGULAR_ROUTES, ENTITIES, USE_CASES,
)

OUT_DIR = os.path.dirname(__file__)
OUT_PDF = os.path.join(OUT_DIR, "Rapport_PFE_SmartLogix.pdf")
OUT_RESUME = os.path.join(OUT_DIR, "Resume_Executif_SmartLogix.pdf")
DIAGRAM_DIR = os.path.join(OUT_DIR, "diagrammes")


class RapportPFE(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(15, 15, 15)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"{PROJECT} - Rapport PFE | Page {self.page_no()}", align="C")

    def h1(self, num, title):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(15, 60, 110)
        self.cell(0, 10, f"CHAPITRE {num} - {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(15, 60, 110)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(5)

    def h2(self, title):
        if self.get_y() > 258:
            self.add_page()
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def h3(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def p(self, text):
        if self.get_y() > 265:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(35, 35, 35)
        self.multi_cell(0, 5.2, text)
        self.ln(1.5)

    def bullet(self, text):
        if self.get_y() > 265:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(35, 35, 35)
        self.multi_cell(0, 5.2, f"  - {text}")

    def fig(self, caption, lines):
        self.h3(caption)
        self.set_font("Courier", "", 7.5)
        self.set_fill_color(248, 250, 252)
        self.set_text_color(20, 20, 20)
        for line in lines.strip().split("\n"):
            if self.get_y() > 275:
                self.add_page()
            self.cell(0, 4.2, line[:115], new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.ln(3)

    def table(self, headers, rows, widths=None):
        if not widths:
            w = 180 / len(headers)
            widths = [w] * len(headers)
        if self.get_y() > 248:
            self.add_page()
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(15, 60, 110)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(widths[i], 6, str(h)[:45], border=1, fill=True)
        self.ln()
        self.set_font("Helvetica", "", 7.5)
        fill = False
        for row in rows:
            if self.get_y() > 275:
                self.add_page()
            if fill:
                self.set_fill_color(240, 244, 248)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_text_color(30, 30, 30)
            for i, cell in enumerate(row):
                self.cell(widths[i], 5.5, str(cell)[:58], border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(2)


def cover(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(15, 60, 110)
    pdf.ln(35)
    pdf.cell(0, 12, PROJECT, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "Conception et developpement d'une plateforme", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, "intelligente de gestion logistique", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(15)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 7, "Rapport de Projet de Fin d'Etudes (PFE)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(20)
    for k, v in [
        ("Auteur", "[A completer]"),
        ("Formation", "[A completer]"),
        ("Etablissement", "[A completer]"),
        ("Encadrant", "[A completer]"),
        ("Annee universitaire", "2025-2026"),
        ("Nom technique depot", CODE_NAME),
    ]:
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, f"{k} : {v}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(12)
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(0, 5.5,
        "Technologies : Java 17, Spring Boot 4.1, Angular 16, PostgreSQL, Python FastAPI, "
        "scikit-learn, XGBoost, JWT, Flyway", align="C")
    pdf.ln(8)
    pdf.cell(0, 7, f"Date : {date.today().strftime('%d/%m/%Y')}", align="C")


def toc_page(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Table des matieres", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    items = [
        "Remerciements et resume executif",
        "Cartographie du projet",
        "Chapitre 1 - Contexte general du projet",
        "Chapitre 2 - Analyse des besoins",
        "Chapitre 3 - Methodologie de developpement",
        "Chapitre 4 - Architecture du systeme",
        "Chapitre 5 - Diagrammes UML (cas d'utilisation)",
        "Chapitre 6 - Diagramme de classes",
        "Chapitre 7 - Base de donnees",
        "Chapitre 8 - Backend Spring Boot",
        "Chapitre 9 - Frontend Angular",
        "Chapitre 10 - Intelligence artificielle et Machine Learning",
        "Chapitre 11 - Diagrammes de sequence",
        "Chapitre 12 - Outils et technologies",
        "Chapitre 13 - Tests",
        "Chapitre 14 - Securite",
        "Chapitre 15 - Docker et DevOps",
        "Chapitre 16 - Deploiement",
        "Chapitre 17 - Scenario global de fonctionnement",
        "Chapitre 18 - Difficultes et solutions",
        "Chapitre 19 - Choix technologiques",
        "Chapitre 20 - Limites et perspectives",
        "Chapitre 21 - Conclusion",
        "Annexes",
    ]
    pdf.set_font("Helvetica", "", 11)
    for i, item in enumerate(items, 1):
        pdf.cell(0, 6.5, f"{i}. {item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def list_figures_tables(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Liste des figures", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    figs = [
        "Figure 4.1 - Architecture generale du systeme",
        "Figure 4.2 - Architecture logique en couches",
        "Figure 4.3 - Architecture physique (ports et services)",
        "Figure 5.1 - Diagramme de cas d'utilisation global",
        "Figure 6.1 - Diagramme de classes metier",
        "Figure 7.1 - Modele entite-relation (ERD)",
        "Figure 10.1 - Architecture du service IA",
        "Figure 10.2 - Flux prediction Machine Learning",
        "Figure 11.1 - Sequence authentification JWT",
        "Figure 11.2 - Sequence creation commande + automation",
        "Figure 11.3 - Sequence prediction IA",
        "Figure 11.4 - Sequence optimisation itineraire chauffeur",
        "Figure 11.5 - Sequence chatbot Copilot",
        "Figure 16.1 - Schema de deploiement possible",
    ]
    pdf.set_font("Helvetica", "", 10)
    for f in figs:
        pdf.cell(0, 5.5, f, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Liste des tableaux", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    tabs = [
        "Tableau 1.1 - Critique de l'existant",
        "Tableau 1.2 - Problemes et solutions SmartLogix",
        "Tableau 2.1 - Acteurs du systeme",
        "Tableau 2.2 - Besoins non fonctionnels",
        "Tableau 3.1 - Phases de developpement",
        "Tableau 7.1 - Tables PostgreSQL (Flyway V1-V10)",
        "Tableau 8.1 - Technologies backend",
        "Tableau 8.2 - Controllers REST (13 controllers, 97 endpoints)",
        "Tableau 8.3 - Catalogue complet des API REST",
        "Tableau 9.1 - Routes Angular par role",
        "Tableau 10.1 - Variables du dataset ML",
        "Tableau 10.2 - Comparaison modeles ML",
        "Tableau 10.3 - Chaine automation 7 etapes",
        "Tableau 10.4 - Endpoints Python FastAPI",
        "Tableau 12.1 - Stack technologique complete",
        "Tableau 13.1 - Strategie de tests",
        "Tableau 18.1 - Difficultes rencontrees",
        "Annexe - Comptes de test et types produit",
    ]
    pdf.set_font("Helvetica", "", 10)
    for t in tabs:
        pdf.cell(0, 5.5, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def cartographie(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "CARTOGRAPHIE DU PROJET (verification code source)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    pdf.table(
        ["Composant", "Nombre", "Detail"],
        [
            ["Controllers REST Java", "13", f"{len(ENDPOINTS)} endpoints documentes"],
            ["Services Java", "21+", "automation, chat, ai, driver, metier"],
            ["Entities JPA", "11", "User, Task, Order, ProductType..."],
            ["Repositories", "11", "Spring Data JPA"],
            ["Migrations Flyway", "10", "V1 a V10"],
            ["Composants Angular", "49", "6 roles + shared + chat widget"],
            ["Services Angular", "11", "HTTP vers API Spring Boot"],
            ["Endpoints Python IA", "11", "FastAPI /api/ai/*"],
            ["Tests Java", "7 fichiers", "20 methodes @Test"],
            ["Tests Python", "2 modules", "14 tests pytest"],
            ["Tests Angular", "1 spec", "app.component.spec.ts"],
        ],
        [45, 25, 110],
    )
    pdf.p(
        f"Note : le titre du rapport est {PROJECT}. Le depot source utilise le nom technique "
        f"{CODE_NAME}. Les deux designent le meme projet."
    )


def chapitre_1(pdf):
    pdf.h1("1", "CONTEXTE GENERAL DU PROJET")
    pdf.h2("1.1 Introduction")
    pdf.p(
        f"{PROJECT} est une plateforme web de gestion logistique destinee aux entreprises de "
        "livraison et de transport. Elle digitalise le cycle complet : prise de commande, "
        "preparation, assignation chauffeur, execution de la livraison, confirmation client, "
        "gestion des incidents et tableaux de bord par role."
    )
    pdf.p(
        "Le projet s'inscrit dans une demarche de modernisation des systemes d'information "
        "logistiques, en integrant une architecture distribuee et des capacites d'intelligence "
        "artificielle pour l'aide a la decision et l'automatisation."
    )
    pdf.h2("1.2 Contexte du projet")
    pdf.p(
        "Domaine : logistique du dernier kilometre (last-mile delivery). Contexte academique : "
        "Projet de Fin d'Etudes (PFE) en genie informatique. Le secteur connait une croissance "
        "des livraisons express, imposant reactivite, tracabilite et coordination multi-acteurs."
    )
    pdf.bullet("Besoin de centraliser commandes, taches et livraisons")
    pdf.bullet("Necessite d'automatiser les decisions pour les urgences HIGH/CRITICAL")
    pdf.bullet("Integration IA pour prediction, recommandation et assistance")
    pdf.h2("1.3 Problematique")
    pdf.p(
        "Comment concevoir une plateforme multi-acteurs integrant l'intelligence artificielle "
        "pour automatiser les livraisons urgentes, predire les retards, optimiser les "
        "itineraires chauffeur et assister les utilisateurs via un copilote conversationnel, "
        "tout en garantissant securite, tracabilite et experience utilisateur par role ?"
    )
    pdf.h2("1.5 Critique de l'existant")
    pdf.table(
        ["Probleme", "Consequence", "Limitation"],
        [
            ["Traitement manuel commandes", "Lenteur, erreurs", "Pas de workflow"],
            ["Assignation chauffeur intuitive", "Sous-optimal", "Pas de scoring"],
            ["Retards non anticipes", "Insatisfaction", "Reactif seulement"],
            ["Suivi fragmente", "Manque visibilite", "Communication difficile"],
            ["Saisie libre produits", "Donnees incoherentes", "Pas de standard"],
            ["Pas d'assistant centralise", "Charge support", "FAQ statiques"],
        ],
        [55, 55, 70],
    )
    pdf.h2("1.6 Solution proposee")
    pdf.table(
        ["Probleme", "Solution SmartLogix"],
        [
            ["Commandes manuelles", "Workflow Operator + catalogue types produit"],
            ["Assignation", "IA recommandation + automation express"],
            ["Retards", "Prediction ML + alertes proactives chauffeur"],
            ["Suivi", "SSE temps reel + notifications"],
            ["Typage produits", "6 types + option Autre"],
            ["Assistance", "Chatbot SmartTask Copilot par role"],
            ["Urgences", "Chaine automation 7 etapes auto HIGH/CRITICAL"],
        ],
        [70, 110],
    )
    pdf.h2("1.7 Objectifs du projet")
    pdf.h3("Objectifs fonctionnels")
    pdf.bullet("Gerer 5 roles : Admin, Manager, Operator, Driver, Client")
    pdf.bullet("Cycle commande -> tache -> livraison -> avis client")
    pdf.bullet("Incidents, notifications, analytics manager, export CSV")
    pdf.bullet("Types de produits standardises avec saisie libre optionnelle")
    pdf.h3("Objectifs techniques")
    pdf.bullet("Architecture 3 tiers : Angular + Spring Boot + Python FastAPI")
    pdf.bullet("API REST securisee JWT, migrations Flyway, validation Bean Validation")
    pdf.bullet("Microservice IA decouple via WebClient HTTP")
    pdf.h3("Objectifs lies a l'IA")
    pdf.bullet("Prediction retard (classification) et ETA (regression)")
    pdf.bullet("Recommandation chauffeur, priorisation taches")
    pdf.bullet("Automation express, optimisation route, alertes proactives")
    pdf.bullet("Chatbot contextuel avec historique persistant")
    pdf.h3("Objectifs lies a la securite")
    pdf.bullet("Authentification JWT stateless, mots de passe BCrypt")
    pdf.bullet("Controle d'acces base sur les roles (RBAC)")
    pdf.h3("Objectifs lies au DevOps")
    pdf.bullet("Dockerfile pour service IA (partiel)")
    pdf.p("Fonctionnalite prevue / future amelioration : CI/CD complet, docker-compose stack, Kubernetes.")
    pdf.h2("1.8 Valeur ajoutee")
    pdf.p(
        "SmartLogix combine gestion metier complete et IA operationnelle : predictions, "
        "automation autonome, copilote conversationnel et optimisation itineraire. "
        "L'architecture microservices permet d'evoluer le module IA independamment du backend."
    )
    pdf.h2("1.9 Organisation du rapport")
    pdf.p(
        "Le rapport presente successivement l'analyse des besoins, l'architecture, les "
        "diagrammes UML, la base de donnees, le backend, le frontend, l'IA en profondeur, "
        "les tests, la securite, le deploiement et les perspectives."
    )


def chapitre_2(pdf):
    pdf.h1("2", "ANALYSE DES BESOINS")
    pdf.h2("2.1 Identification des acteurs")
    pdf.table(
        ["Acteur", "Description", "Responsabilites"],
        [
            ["ADMIN", "Administrateur systeme", "CRUD utilisateurs, roles, activation"],
            ["MANAGER", "Superviseur logistique", "Taches, chauffeurs, IA, analytics, automation"],
            ["OPERATOR", "Operateur entrepot", "Commandes, validation, preparation, incidents"],
            ["DRIVER", "Chauffeur livreur", "Missions, livraison, GPS, itineraire IA, alertes"],
            ["CLIENT", "Client final", "Suivi livraison SSE, confirmation, avis"],
        ],
        [30, 55, 95],
    )
    pdf.h2("2.2 Besoins fonctionnels (implementes dans le code)")
    for f in [
        "Authentification JWT (register, login, logout, me)",
        "Gestion utilisateurs complete (Admin)",
        "Gestion commandes avec types produit et option Autre (Operator)",
        "Workflow commande : PENDING -> VERIFIED -> READY -> IN_DELIVERY -> DELIVERED -> RECEIVED",
        "Gestion taches et assignation chauffeur (Manager)",
        "Cycle mission chauffeur : accept, start, delivery, complete, proof",
        "Suivi livraison SSE temps reel (Client)",
        "Incidents multi-acteurs avec traitement manager",
        "Avis clients (rating 1-5, commentaire, unique par tache)",
        "Notifications par utilisateur avec marquage lu",
        "Analytics manager + export CSV",
        "Predictions IA : retard, ETA, priorite, chauffeur, anomalie",
        "Chaine automation Livraison Express (7 etapes)",
        "Chatbot SmartTask Copilot avec historique",
        "Optimisation itineraire chauffeur via IA",
        "Alertes IA proactives chauffeur (scheduler 5 min)",
    ]:
        pdf.bullet(f)
    pdf.h2("2.3 Besoins non fonctionnels")
    pdf.table(
        ["NFR", "Implementation observee"],
        [
            ["Securite", "JWT, BCrypt, RBAC @PreAuthorize, CORS"],
            ["Performance", "Index BDD V6, pagination, open-in-view=false"],
            ["Maintenabilite", "Couches Controller/Service/Repository/DTO"],
            ["Evoluabilite", "Microservice IA separe, events async"],
            ["Disponibilite IA", "Fallback rule-based si Python indisponible"],
            ["Testabilite", "JUnit, pytest, profil test H2"],
            ["Ergonomie", "Interfaces par role, chat widget, feedback visuel"],
        ],
        [45, 135],
    )
    pdf.h2("2.4 Contraintes")
    pdf.bullet("Techniques : 3 services a demarrer (Spring, Angular, Python)")
    pdf.bullet("Logicielles : PostgreSQL requis, modeles .pkl a generer localement")
    pdf.bullet("Securite : secret JWT a changer en production")
    pdf.bullet("Materielles : Information non identifiee dans les fichiers fournis.")
    pdf.bullet("Temporelles : Information non identifiee dans les fichiers fournis.")


def chapitre_3(pdf):
    pdf.h1("3", "METHODOLOGIE DE DEVELOPPEMENT")
    pdf.h2("3.1 Methodologie adoptee")
    pdf.p(
        "Developpement iteratif et incremental, organise en phases fonctionnelles successives. "
        "Chaque phase livre un increment testable. Outils : Git, Gradle, npm, Flyway, Swagger."
    )
    pdf.h2("3.2 Organisation du travail")
    pdf.bullet("Backlog fonctionnel par module (auth, metier, IA, automation)")
    pdf.bullet("Integration continue manuelle : build Gradle + ng build + pytest")
    pdf.bullet("Tests unitaires et tests manuels via Swagger/Postman")
    pdf.h2("3.3 Planification")
    pdf.table(
        ["Phase", "Objectif", "Livrables"],
        [
            ["P1", "Auth + users + 5 roles", "JWT, guards Angular"],
            ["P2", "Metier logistique", "Orders, Tasks, Drivers, Notifications"],
            ["P3", "Frontend multi-role", "49 composants, routing lazy"],
            ["P4", "Microservice IA", "FastAPI, train ML, .pkl"],
            ["P5", "Integration IA", "WebClient, page Manager IA"],
            ["P6", "Chatbot Copilot", "V8 chat_messages, widget"],
            ["P7", "Automation express", "V9 automation_logs, 7 etapes"],
            ["P8", "Types produit", "V10 product_types, formulaire Operator"],
            ["P9", "IA Chauffeur", "Route optimize + alertes scheduler"],
        ],
        [20, 70, 90],
    )


def chapitre_4(pdf):
    pdf.h1("4", "ARCHITECTURE DU SYSTEME")
    pdf.fig("Figure 4.1 - Architecture generale", """
Utilisateur (Navigateur Web)
        |
        v
   Angular 16 SPA (port 4200)
        | HTTP REST + JWT Bearer
        v
 Spring Boot 4.1 API (port 9090)
   Controllers | Services | Security | JPA | Events
        |                              |
        | JDBC                         | WebClient HTTP
        v                              v
  PostgreSQL smarttask_db         Python FastAPI (port 8000)
  (port 5432)                     ML Models (.pkl) + Chatbot
    """)
    pdf.h2("4.2 Architecture logique")
    pdf.p(
        "Couche presentation (Angular) | Couche API REST (Controllers) | "
        "Couche metier (Services) | Couche persistance (Repositories/JPA) | "
        "Couche IA (Python microservice) | Couche securite transversale (JWT, RBAC)."
    )
    pdf.fig("Figure 4.2 - Architecture logique en couches", """
+----------------------------------------------------------+
| PRESENTATION : Components Angular, Guards, Interceptors   |
+----------------------------------------------------------+
| API REST : 13 Controllers, DTO, Validation, Swagger       |
+----------------------------------------------------------+
| METIER : Services, Events, Automation, Chat, AI facade    |
+----------------------------------------------------------+
| PERSISTANCE : JPA Entities, Repositories, Flyway          |
+----------------------------------------------------------+
| IA : FastAPI PredictionService, RouteOptimization, Chat  |
+----------------------------------------------------------+
| SECURITE : JwtFilter, SecurityConfig, BCrypt              |
+----------------------------------------------------------+
    """)
    pdf.h2("4.3 Architecture physique")
    pdf.table(
        ["Composant", "Port", "Technologie", "Deploiement"],
        [
            ["Frontend", "4200", "Angular dev server", "Static build possible"],
            ["Backend", "9090", "Spring Boot embedded Tomcat", "JAR executable"],
            ["IA", "8000", "Uvicorn + FastAPI", "Dockerfile present"],
            ["BDD", "5432", "PostgreSQL", "Service externe"],
        ],
        [35, 22, 58, 65],
    )
    pdf.h2("4.4 Architecture applicative backend")
    pdf.p(
        "Pattern en couches avec inversion de controle Spring : Controller recoit requetes HTTP, "
        "delegue au Service pour la logique metier, qui utilise Repository pour la persistance. "
        "DTO separent le modele API du modele JPA. GlobalExceptionHandler centralise les erreurs."
    )
    pdf.h2("4.5 Architecture microservices")
    pdf.p(
        "Le projet adopte une architecture distribuee legere : le backend Spring Boot est le "
        "orchestrateur central ; le microservice Python IA est stateless et communique uniquement "
        "via HTTP REST JSON. Le frontend ne contacte jamais Python directement."
    )


def chapitre_5(pdf):
    pdf.h1("5", "DIAGRAMMES UML - CAS D'UTILISATION")
    pdf.fig("Figure 5.1 - Cas d'utilisation global", """
                    +------------------+
                    |    SmartLogix    |
                    +------------------+
     +--------+     | S'authentifier   |     +---------+
     | Admin  |-----| Gerer utilisat.  |-----| Manager |
     +--------+     | Gerer commandes  |     +---------+
     +----------+   | Gerer taches     |   +----------+
     | Operator |---| Executer livr.   |---|  Driver  |
     +----------+   | Suivre livraison |   +----------+
     +--------+     | Utiliser IA      |     +--------+
     | Client |-----| Chatbot Copilot  |-----|Systeme |
     +--------+     | Automation       |     |   IA   |
                    +------------------+     +--------+
    """)
    pdf.h2("5.2 Cas d'utilisation par acteur")
    pdf.table(
        ["Acteur", "Cas d'utilisation", "Interdit"],
        [
            ["ADMIN", "CRUD users, roles, status", "Gestion commandes/taches"],
            ["MANAGER", "Dashboard, taches, IA, automation, analytics", "Creer commandes"],
            ["OPERATOR", "Commandes, verify, prepare, incidents", "Assigner chauffeurs"],
            ["DRIVER", "Missions, livraison, route IA, alertes", "Gerer autres chauffeurs"],
            ["CLIENT", "Suivi SSE, confirm, avis", "Acces manager/operator"],
        ],
        [30, 90, 60],
    )
    pdf.h2("5.3 Descriptions textuelles des cas d'utilisation")
    for uc in USE_CASES:
        pdf.h3(f"CU : {uc['name']}")
        pdf.p(f"Acteur : {uc['actor']} | Precondition : {uc['pre']}")
        pdf.p(f"Declencheur : {uc['trigger']}")
        pdf.p(f"Scenario nominal : {uc['nominal']}")
        pdf.p(f"Scenarios alternatifs : {uc['alt']}")
        pdf.p(f"Postcondition : {uc['post']}")
        pdf.ln(1)


def chapitre_6(pdf):
    pdf.h1("6", "DIAGRAMME DE CLASSES")
    pdf.fig("Figure 6.1 - Diagramme de classes metier", """
User 1---* Task (client)     User 1---* Task (driver)
User 1---1 DriverProfile    Order *---1 ProductType
Order 1---0..1 Task         Task 1---* TaskHistory
Task 1---* Notification     User 1---* ChatMessage
AutomationLog (runId, step) Incident *---0..1 Task
Review 1---1 Task (unique)  User 1---* Review
    """)
    pdf.h2("6.2 Description des classes importantes")
    for cls, fields in ENTITIES.items():
        pdf.h3(f"Classe {cls}")
        pdf.table(["Attribut", "Type", "Contrainte"], fields, [55, 45, 80])
        pdf.ln(1)
    pdf.h2("6.3 Services backend cles")
    pdf.table(
        ["Classe", "Package", "Responsabilite"],
        [
            ("ExpressDeliveryAutomationService", "service.automation", "Chaine 7 etapes"),
            ("AIService", "service", "Facade appels Python"),
            ("SmartTaskAIClient", "client", "WebClient HTTP FastAPI"),
            ("CompositeAIRecommendationService", "service.ai", "Python + fallback regles"),
            ("DriverRouteOptimizationService", "service.driver", "Ordre optimal missions"),
            ("DriverProactiveAlertService", "service.driver", "Alertes scheduler"),
            ("ChatService", "service.chat", "Orchestration chatbot"),
            ("AutomationEventListener", "event", "Declenchement auto HIGH/CRITICAL"),
            ("SecurityConfig", "config", "JWT filter chain, CORS, RBAC"),
        ],
        [55, 45, 80],
    )


def chapitre_7(pdf):
    pdf.h1("7", "BASE DE DONNEES")
    pdf.p("SGBD : PostgreSQL | ORM : Hibernate/JPA | ddl-auto : validate | Migrations : Flyway V1-V10")
    pdf.table(
        ["Table", "Description", "Migration"],
        [
            ["users", "Comptes 5 roles", "V1"],
            ["driver_profiles", "Profil chauffeur 1-1 User", "V2"],
            ["tasks", "Missions livraison", "V2, V3, V7"],
            ["task_history", "Audit actions taches", "V2"],
            ["notifications", "Alertes utilisateur", "V2"],
            ["orders", "Commandes clients", "V3, V10"],
            ["incidents", "Signalements", "V3"],
            ["reviews", "Avis post-livraison", "V3"],
            ["chat_messages", "Historique chatbot", "V8"],
            ["automation_logs", "Journal chaine IA", "V9"],
            ["product_types", "Catalogue 6 types", "V10"],
        ],
        [40, 80, 30],
    )
    pdf.h2("7.3 Relations JPA")
    pdf.bullet("User 1-N Task (client_id, driver_id, created_by)")
    pdf.bullet("User 1-1 DriverProfile")
    pdf.bullet("Order N-1 ProductType, N-1 User (client, operator)")
    pdf.bullet("Task N-1 Order, 1-N TaskHistory, 1-N Notification")
    pdf.bullet("Review 1-1 Task (contrainte unique task_id)")
    pdf.h2("7.4 Persistance JPA")
    pdf.p(
        "Entities annotees @Entity, relations @ManyToOne/@OneToOne/@OneToMany. "
        "Repositories Spring Data JPA avec methodes derivees et @Query si necessaire. "
        "Flyway gere le schema ; Hibernate valide uniquement (pas de auto-ddl)."
    )
    pdf.h2("7.5 Workflows de statuts")
    pdf.p("OrderStatus : PENDING -> VERIFIED -> PREPARING -> READY -> IN_DELIVERY -> DELIVERED -> RECEIVED")
    pdf.p("TaskStatus : PENDING/PREPARED -> ASSIGNED -> ACCEPTED -> IN_PROGRESS -> IN_DELIVERY -> COMPLETED")


def chapitre_8(pdf):
    pdf.h1("8", "BACKEND SPRING BOOT")
    pdf.h2("8.1 Technologies")
    pdf.table(
        ["Technologie", "Version", "Usage"],
        [
            ["Java", "17", "Langage backend"],
            ["Spring Boot", "4.1.0", "Framework applicatif"],
            ["Spring Security", "6.x", "JWT, RBAC"],
            ["Spring Data JPA", "-", "ORM Hibernate"],
            ["Flyway", "-", "Migrations SQL"],
            ["PostgreSQL Driver", "-", "Connexion BDD"],
            ["WebFlux WebClient", "-", "Client HTTP Python"],
            ["jjwt", "0.12.6", "Generation/validation JWT"],
            ["SpringDoc OpenAPI", "3.0.1", "Documentation Swagger"],
            ["Lombok", "-", "Reduction boilerplate"],
            ["Gradle", "-", "Build et dependances"],
        ],
        [45, 30, 105],
    )
    pdf.h2("8.2 Structure du projet")
    pdf.fig("Arborescence backend (packages principaux)", """
src/main/java/tn/esprit/smarttask/
  controller/     (13 controllers REST)
  service/        (metier + automation + chat + ai + driver)
  repository/     (11 interfaces JPA)
  entity/         (11 entites + enums)
  dto/            (requetes/reponses API)
  security/       (JWT filter, UserDetails)
  config/         (Security, CORS, Swagger, properties)
  client/         (SmartTaskAIClient WebClient)
  event/          (OrderCreatedEvent, listener async)
  exception/      (GlobalExceptionHandler)
src/main/resources/
  application.properties
  db/migration/   (V1 a V10)
    """)
    pdf.h2("8.3 Controllers REST")
    pdf.table(
        ["Controller", "Base path", "Endpoints", "Role"],
        [
            ["AuthenticationController", "/api/auth", "4", "Public/Auth"],
            ["UserController", "/api/users", "10", "ADMIN/Auth"],
            ["ManagerController", "/api/manager", "14", "MANAGER"],
            ["ManagerAIController", "/api/manager/ai", "8", "MANAGER"],
            ["TaskController", "/api/tasks", "10", "MANAGER"],
            ["OperatorController", "/api/operator", "12", "OPERATOR"],
            ["DriverController", "/api/driver", "15", "DRIVER"],
            ["ClientController", "/api/client", "10", "CLIENT"],
            ["AutomationController", "/api/automation", "4", "MGR/OP"],
            ["ProductTypeController", "/api/product-types", "1", "Auth"],
            ["ChatController", "/api/chat", "3", "Auth"],
        ],
        [50, 45, 22, 33],
    )
    pdf.h2("8.3.1 Catalogue complet des API REST")
    rows = [(m, path, role, desc) for m, path, role, desc in ENDPOINTS]
    pdf.table(["Methode", "Endpoint", "Securite", "Description"], rows, [18, 62, 22, 78])
    pdf.h2("8.11 Securite backend")
    pdf.p(
        "SecurityFilterChain configure les regles URL. JwtAuthenticationFilter extrait le token "
        "Bearer, valide signature et expiration, charge UserDetails. @PreAuthorize sur methodes "
        "sensibles. Mots de passe hashes BCryptPasswordEncoder."
    )
    pdf.fig("Listing 8.1 - Chaine automation (7 etapes)", """
@Transactional(noRollbackFor = AIServiceUnavailableException.class)
public ExpressChainResultResponse execute(Long orderId) {
  step1 READ_ORDER -> step2 AUTO_VERIFY -> step3 CREATE_TASK
  step4 AI_PRIORITIZE -> step5 AI_ASSIGN_DRIVER (score >= 70%)
  step6 ESTIMATE_AND_NOTIFY -> step7 LOG_COMPLETE
}
    """)


def chapitre_9(pdf):
    pdf.h1("9", "FRONTEND ANGULAR")
    pdf.h2("9.1 Architecture Angular")
    pdf.p(
        "Angular 16 avec composants standalone, lazy loading par role, RxJS pour flux asynchrones. "
        "Structure : core/ (auth, services, models), features/ (pages par role), shared/ (chat, navbar)."
    )
    pdf.h2("9.2 Routes Angular")
    rows = [(r, c, role) for r, c, role in ANGULAR_ROUTES]
    pdf.table(["Route", "Component", "Role requis"], rows, [55, 75, 30])
    pdf.h2("9.4 Services Angular")
    for s in [
        "AuthService : login/logout, JWT localStorage",
        "UserService : profil, gestion users (admin)",
        "TaskService : CRUD taches manager",
        "ManagerService : dashboard, analytics, incidents",
        "OperatorService : commandes, preparation",
        "DriverService : missions, route optimise, alertes",
        "ClientService : commandes, SSE livraison, avis",
        "AiService : predictions via backend (pas Python direct)",
        "ChatService : init, message, historique",
        "AutomationService : status, logs, lancer chaine",
        "ProductTypeService : liste types produit",
    ]:
        pdf.bullet(s)
    pdf.h2("9.6 Guards et Interceptors")
    pdf.bullet("authGuard : verifie presence token JWT")
    pdf.bullet("roleGuard : verifie role dans route.data.roles")
    pdf.bullet("jwt.interceptor : ajoute header Authorization Bearer")
    pdf.h2("9.8 Flux authentification frontend")
    pdf.fig("Flux Angular -> JWT", """
LoginComponent -> AuthService.login() -> POST /api/auth/login
<- JWT token -> localStorage.setItem('token')
Route protegee -> authGuard OK -> jwt.interceptor ajoute Bearer
-> requetes API securisees -> dashboard selon role
    """)
    pdf.h2("9.9 Pages principales par role")
    pdf.table(
        ["Role", "Pages cles"],
        [
            ["Manager", "Dashboard KPIs, Taches, Carte, IA, Automation, Analytics"],
            ["Operator", "Commandes, Create (types produit), Pending, Tracking"],
            ["Driver", "Missions, Route optimise IA, Performance, Alertes"],
            ["Client", "Commandes, Delivery SSE, Reviews, Notifications"],
            ["Admin", "Users CRUD, Dashboard"],
        ],
        [30, 150],
    )


def chapitre_10(pdf):
    pdf.h1("10", "INTELLIGENCE ARTIFICIELLE ET MACHINE LEARNING")
    pdf.h2("10.1 Problematique IA")
    pdf.p(
        "L'IA repond a des problemes predictifs et decisionnels : anticiper les retards, estimer "
        "les temps de livraison, recommander le meilleur chauffeur, prioriser les taches urgentes, "
        "optimiser les itineraires et assister les utilisateurs."
    )
    pdf.h2("10.2 Donnees")
    pdf.p("Dataset : smarttask-ai/data/raw/smarttask_delivery_dataset.csv")
    pdf.p("Origine : SYNTHETIC_DEV | Echantillons : 3000 | Colonnes : features + cibles delayed et actual_delivery_time")
    pdf.table(
        ["Variable", "Type", "Signification"],
        [
            ["distance_km", "float", "Distance estimee km"],
            ["deadline_minutes", "int", "Minutes restantes deadline"],
            ["priority_score", "int", "Score priorite encode"],
            ["hour, day_of_week", "int", "Contexte temporel"],
            ["driver_current_tasks", "int", "Charge chauffeur"],
            ["driver_delay_rate", "float", "Taux retard historique"],
            ["traffic_score", "float", "Indice trafic"],
            ["delayed", "0/1", "Cible classification"],
            ["actual_delivery_time", "int", "Cible regression (minutes)"],
        ],
        [45, 25, 110],
    )
    pdf.h2("10.3 Pretraitement")
    pdf.bullet("1. Importation CSV via pandas")
    pdf.bullet("2. Nettoyage valeurs manquantes")
    pdf.bullet("3. Encodage variables categorielles (priority, traffic)")
    pdf.bullet("4. Separation features / cibles")
    pdf.bullet("5. Split train/test (80/20)")
    pdf.bullet("6. Standardisation pour modeles sensibles")
    pdf.h2("10.4 Exploration")
    pdf.p("Statistiques descriptives, distribution retards, correlation features. Scripts dans app/ml/.")
    pdf.h2("10.5 Modeles")
    pdf.table(
        ["Modele", "Type", "Algorithme", "Metriques test"],
        [
            ["delay_model", "Classification", "Logistic Regression", "Acc 0.965, F1 0.982, AUC 0.990"],
            ["delivery_time_model", "Regression", "XGBoost", "MAE 6.32 min, R2 0.960"],
            ["priority_model", "-", "Stub non entraine", "Regles fallback"],
            ["driver_recommend", "Scoring", "Rule-based v1.0.0", "Pas de .pkl"],
            ["route_optimize", "Heuristique", "TSP nearest neighbor", "Pas de .pkl"],
            ["anomaly_detect", "Statistique", "Seuils AnalyticsService", "Pas de .pkl"],
        ],
        [38, 30, 42, 70],
    )
    pdf.p("Note : fichiers .pkl non commites - generer via : python -m app.ml.train_all")
    pdf.h2("10.7 Service Python FastAPI")
    pdf.fig("Structure smarttask-ai", """
smarttask-ai/
  app/main.py           FastAPI entrypoint
  app/api/              predict, chat, route, health
  app/services/         PredictionService, RouteOptimizationService
  app/ml/               train_delay, train_delivery_time, train_all
  app/models/           .pkl + model_metadata.json
  app/data/knowledge_base.json   Chatbot
    """)
    pdf.h2("10.8 Integration Spring Boot + Python")
    pdf.p(
        "SmartTaskAIClient utilise WebClient (Spring WebFlux) pour appels HTTP synchrones "
        "vers http://localhost:8000. Format JSON request/response. Timeout configurable "
        "(app.ai.timeout-seconds=10). CompositeAIRecommendationService bascule sur "
        "RuleBasedAIRecommendationService si Python indisponible."
    )
    pdf.table(["Methode", "Endpoint Python", "Description"], PYTHON_ENDPOINTS, [18, 55, 107])
    pdf.h2("10.9 Chaine automation express")
    pdf.table(
        ["Etape", "Nom", "Action"],
        [
            ["1", "READ_ORDER", "Lire commande depuis BDD"],
            ["2", "AUTO_VERIFY", "PENDING -> VERIFIED"],
            ["3", "CREATE_TASK", "Tache PREPARED, order READY"],
            ["4", "AI_PRIORITIZE", "POST /api/ai/prioritize/task"],
            ["5", "AI_ASSIGN_DRIVER", "POST /api/ai/recommend/driver si score>=70%"],
            ["6", "ESTIMATE_AND_NOTIFY", "ETA + notifications client/chauffeur"],
            ["7", "LOG_COMPLETE", "Ecriture automation_logs"],
        ],
        [15, 45, 120],
    )
    pdf.h2("10.10 IA Chauffeur")
    pdf.bullet("Route : GET /api/driver/route/optimized -> POST /api/ai/optimize/route")
    pdf.bullet("Alertes : DriverProactiveAlertScheduler interval 300000ms (5 min)")
    pdf.bullet("Config : deadline-warning-minutes=45, delay-risk-minutes=20, dedup-minutes=30")
    pdf.h2("10.11 Chatbot SmartTask Copilot")
    pdf.p(
        "Intents regex + knowledge_base.json. Contexte role depuis ChatContextBuilderService "
        "(stats dashboard injectees). Fallback Java ChatFallbackService si Python down."
    )


def chapitre_11(pdf):
    pdf.h1("11", "DIAGRAMMES DE SEQUENCE")
    pdf.fig("Figure 11.1 - Authentification JWT", """
User -> Angular: saisir credentials
Angular -> Spring Boot: POST /api/auth/login
Spring Boot -> PostgreSQL: SELECT user, verify BCrypt
Spring Boot -> Angular: JWT token + user info
Angular -> localStorage: store token
Angular -> Spring Boot: requetes + Authorization Bearer
    """)
    pdf.fig("Figure 11.2 - Commande HIGH + Automation", """
Operator -> Angular -> Spring: POST /api/operator/orders (priority HIGH)
Spring -> PostgreSQL: INSERT order
Spring -> EventPublisher: OrderCreatedEvent
AutomationEventListener (@Async) -> ExpressDeliveryAutomationService
  -> 7 etapes (verify, task, IA, assign, notify, log)
Spring -> Angular: OrderResponse
    """)
    pdf.fig("Figure 11.3 - Prediction retard IA", """
Manager -> Angular -> Spring: POST /manager/ai/predict-delay
Spring -> AIService -> SmartTaskAIClient
WebClient -> Python: POST /api/ai/predict/delay
Python -> delay_model.pkl: predict_proba
Python -> Spring: delayProbability, riskLevel, modelVersion
Spring -> Angular: JSON affiche page Manager IA
    """)
    pdf.fig("Figure 11.4 - Route optimisee chauffeur", """
Driver -> Angular -> Spring: GET /api/driver/route/optimized
Spring -> DriverRouteOptimizationService
WebClient -> Python: POST /api/ai/optimize/route (missions GPS)
Python -> TSP heuristic: ordre optimal
Python -> Spring: orderedTaskIds, totalDistanceKm
Spring -> Angular: carte/liste reordonnee
    """)
    pdf.fig("Figure 11.5 - Chatbot Copilot", """
User -> ChatWidget -> Angular ChatService
POST /api/chat/message -> ChatService
  -> SmartTaskAIClient POST /api/ai/chat (ou fallback Java)
  -> INSERT chat_messages (USER + ASSISTANT)
<- reponse affichee widget
    """)
    pdf.h2("11.6 Gestion des erreurs")
    pdf.p(
        "GlobalExceptionHandler intercepte exceptions metier et validation. "
        "AIServiceUnavailableException : pas de rollback transaction automation. "
        "Frontend affiche messages erreur HTTP via interceptors/services."
    )


def chapitre_12_21(pdf):
    pdf.h1("12", "OUTILS ET TECHNOLOGIES")
    pdf.table(
        ["Couche", "Technologie", "Version", "Role"],
        [
            ["Backend", "Java / Spring Boot", "17 / 4.1.0", "API REST metier"],
            ["Backend", "Spring Security + JWT", "jjwt 0.12.6", "Auth stateless"],
            ["Backend", "Spring Data JPA / Flyway", "-", "ORM + migrations"],
            ["Frontend", "Angular / TypeScript", "16.2 / 5.1", "SPA multi-role"],
            ["Frontend", "RxJS", "7.8", "Programmation reactive"],
            ["BDD", "PostgreSQL", "14+", "Persistance relationnelle"],
            ["IA", "Python / FastAPI / Uvicorn", "3.11+", "Microservice ML"],
            ["IA", "scikit-learn / XGBoost / pandas", "1.5+/2.1+", "ML pipeline"],
            ["Build", "Gradle / npm", "-", "Compilation"],
            ["Doc", "SpringDoc OpenAPI", "3.0.1", "Swagger UI"],
            ["Tests", "JUnit 5 / pytest / Karma", "-", "Tests unitaires"],
        ],
        [30, 55, 28, 67],
    )

    pdf.h1("13", "TESTS")
    pdf.table(
        ["Type", "Fichier / Outil", "Contenu"],
        [
            ["Unitaire Java", "AuthenticationControllerTest", "Login register"],
            ["Unitaire Java", "ManagerAIControllerTest", "Endpoints IA manager"],
            ["Unitaire Java", "AutomationControllerTest", "Chaine automation"],
            ["Securite Java", "ManagerSecurityTest, TaskControllerSecurityTest", "RBAC"],
            ["Integration", "SmartTaskApplicationTests", "Context Spring"],
            ["Python", "test_api.py, test_chat.py", "14 tests endpoints"],
            ["Angular", "app.component.spec.ts", "Test bootstrap"],
            ["Manuel", "SmartTask-API.postman_collection.json", "Collection Postman"],
        ],
        [35, 70, 75],
    )
    pdf.p("Profil test : application-test.properties avec H2 in-memory, Flyway desactive.")

    pdf.h1("14", "SECURITE")
    pdf.bullet("JWT expiration 86400000 ms (24h), secret configurable app.jwt.secret")
    pdf.bullet("BCrypt pour hash mots de passe")
    pdf.bullet("RBAC 5 roles avec SecurityFilterChain + @PreAuthorize")
    pdf.bullet("CORS : app.cors.allowed-origins=http://localhost:4200")
    pdf.bullet("Validation @Valid sur DTO entree")
    pdf.bullet("Frontend : token localStorage, guards, interceptor Bearer")
    pdf.bullet("Endpoints publics limites : /api/auth/register, /api/auth/login, swagger")

    pdf.h1("15", "DOCKER ET DEVOPS")
    pdf.p("Present dans le depot : smarttask-ai/Dockerfile (Python 3.11-slim, port 8000).")
    pdf.p("NON present : docker-compose.yml, Jenkins, GitHub Actions, Kubernetes, SonarQube, Prometheus.")
    pdf.p("Fonctionnalite prevue / future amelioration : pipeline CI/CD complet, monitoring Grafana.")

    pdf.h1("16", "DEPLOIEMENT")
    pdf.fig("Figure 16.1 - Processus de deploiement possible", """
Development:
  PostgreSQL + gradlew bootRun + uvicorn + ng serve
Build:
  gradlew bootJar + ng build --configuration production
  python -m app.ml.train_all (generer .pkl)
Tests:
  gradlew test + pytest + ng test
Production possible:
  JAR Spring Boot (9090) + fichiers static Angular (nginx)
  + container Python IA + PostgreSQL managed
    """)
    pdf.table(
        ["Service", "Commande", "Port"],
        [
            ["PostgreSQL", "Creer BDD smarttask_db", "5432"],
            ["Backend", "gradlew bootRun", "9090"],
            ["Python IA", "uvicorn app.main:app --port 8000", "8000"],
            ["Frontend", "ng serve", "4200"],
        ],
        [35, 90, 25],
    )

    pdf.h1("17", "SCENARIO GLOBAL JURY")
    pdf.p("Scenario de demonstration complete :")
    pdf.bullet("1. Operator se connecte (operator1@smarttask.com)")
    pdf.bullet("2. Cree commande type MEDICAMENTS, priorite HIGH, adresse livraison")
    pdf.bullet("3. Automation declenchee : 7 logs SUCCESS dans automation_logs")
    pdf.bullet("4. Manager consulte page Automation et IA Analytics")
    pdf.bullet("5. Driver voit mission assignee, itineraire optimise, alertes proactives")
    pdf.bullet("6. Driver complete livraison avec preuve photo")
    pdf.bullet("7. Client suit via SSE, confirme reception, laisse avis 5 etoiles")
    pdf.bullet("8. Chatbot Copilot repond aux questions du manager")

    pdf.h1("18", "DIFFICULTES ET SOLUTIONS")
    pdf.table(
        ["Probleme", "Cause", "Solution", "Resultat"],
        [
            ["Connection refused :8000", "Python IA arrete", "Demarrer uvicorn", "IA operationnelle"],
            ["Rollback automation", "Exception IA en @Transactional", "noRollbackFor AIServiceUnavailable", "Logs partiels OK"],
            ["CORS blocked", "Origines differentes", "CorsConfiguration 4200", "Frontend accede API"],
            [".pkl absents", "Non commites git", "train_all.py", "Modeles generes"],
            ["Doublon automation", "Re-trigger manuel", "Verification statut order", "Refus si deja traite"],
        ],
        [42, 38, 45, 55],
    )

    pdf.h1("19", "CHOIX TECHNOLOGIQUES")
    pdf.h3("Spring Boot vs alternatives")
    pdf.p("Retenu pour ecosysteme entreprise, securite mature, JPA, communaute. Alternative Node.js/Django non retenue pour experience Java PFE.")
    pdf.h3("Angular vs React/Vue")
    pdf.p("Retenu pour structure modulaire, TypeScript, routing/guards natifs, adequation projets entreprise.")
    pdf.h3("PostgreSQL vs MySQL")
    pdf.p("Retenu pour robustesse, enums, contraintes, adequation JPA/Flyway.")
    pdf.h3("Python pour IA")
    pdf.p("Standard de facto ML (scikit-learn, XGBoost). Microservice decouple evite surcharge JVM.")
    pdf.h3("JWT vs sessions")
    pdf.p("Stateless adapte API REST SPA. Pas de session serveur a gerer.")

    pdf.h1("20", "LIMITES ET PERSPECTIVES")
    pdf.h3("Limites actuelles")
    pdf.bullet("Dataset ML synthetique (3000 echantillons), pas de donnees reelles")
    pdf.bullet("Modeles .pkl non versionnes dans le depot")
    pdf.bullet("Docker partiel (IA seulement)")
    pdf.bullet("Tests frontend limites (1 spec)")
    pdf.bullet("priority_model non entraine (stub)")
    pdf.h3("Perspectives")
    pdf.bullet("Chaines automation 2 et 3 (anti-retard, recovery incident) - prevues")
    pdf.bullet("docker-compose stack complete")
    pdf.bullet("CI/CD GitHub Actions, SonarQube")
    pdf.bullet("Application mobile chauffeur")
    pdf.bullet("Re-entrainement ML sur donnees production")
    pdf.bullet("Deploiement cloud (AWS/Azure)")

    pdf.h1("21", "CONCLUSION")
    pdf.p(
        f"Le projet {PROJECT} atteint ses objectifs principaux : plateforme logistique multi-acteurs "
        "complete, integration IA operationnelle (predictions, automation, chatbot, route chauffeur), "
        "architecture moderne 3 tiers avec securite JWT et persistance PostgreSQL."
    )
    pdf.p(
        "Competences acquises : conception UML, developpement full-stack, microservices, "
        "machine learning, DevOps partiel. L'IA apporte une valeur concrete via l'automation "
        "express et l'aide a la decision manager/chauffeur."
    )
    pdf.p(
        "Perspectives : industrialisation (CI/CD, Docker complet), enrichissement ML sur "
        "donnees reelles, et extension fonctionnelle (mobile, nouvelles chaines automation)."
    )


def expand_backend_detail(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE DETAILLEE - SERVICES BACKEND", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    services = [
        ("AuthService", "register, login, logout, getCurrentUser"),
        ("UserService", "CRUD users, change password, update profile, role/status"),
        ("TaskService", "CRUD tasks, assign driver, history, status/priority updates"),
        ("ManagerService", "dashboard KPIs, drivers, delays, analytics export, incidents"),
        ("OperatorService", "orders CRUD, verify, prepare task, clients list"),
        ("DriverService", "missions lifecycle, location, proof, route, performance"),
        ("ClientService", "orders, delivery tracking SSE, confirm, reviews"),
        ("IncidentService", "create/update incidents multi-acteurs"),
        ("AIService", "facade predict delay, ETA, prioritize, recommend, anomaly"),
        ("CompositeAIRecommendationService", "Python first, fallback RuleBasedAI"),
        ("RuleBasedAIRecommendationService", "regles metier si Python down"),
        ("ExpressDeliveryAutomationService", "chaine 7 etapes transactionnelle"),
        ("ChatService", "init session, send message, history persistence"),
        ("ChatContextBuilderService", "injecte stats role pour contexte IA"),
        ("ChatFallbackService", "reponses Java si Python indisponible"),
        ("DriverRouteOptimizationService", "appel Python optimize/route"),
        ("DriverProactiveAlertService", "analyse missions, notifications alerte"),
        ("ProductTypeService", "liste types actifs depuis product_types"),
        ("RealTimeEventService", "publication evenements SSE livraison"),
        ("JwtService", "generation/validation token JWT"),
        ("CustomUserDetailsService", "charge UserDetails pour Spring Security"),
    ]
    pdf.table(["Service", "Methodes / Responsabilite"], services, [55, 125])
    pdf.h2("Detail AuthService et JwtService")
    pdf.p(
        "AuthService recoit LoginRequest/RegisterRequest, delegue a UserRepository pour "
        "verification BCrypt, genere JWT via JwtService (claims: subject=email, expiration 24h). "
        "Logout cote stateless invalide token cote client uniquement."
    )
    pdf.fig("Listing - JwtAuthenticationFilter (concept)", """
1. Extraire header Authorization: Bearer <token>
2. JwtService.validateToken(token)
3. Charger UserDetails via CustomUserDetailsService
4. SecurityContextHolder.setAuthentication(...)
5. Continuer filter chain
    """)
    pdf.h2("Detail TaskService")
    pdf.p(
        "TaskService gere le cycle complet : creation depuis Order (OperatorService.prepare), "
        "assignation manuelle ou via assign-recommended (appel IA), transitions statut avec "
        "TaskHistory audit, notifications via NotificationRepository."
    )
    pdf.h2("Detail OperatorService - creation commande")
    pdf.p(
        "OrderRequest contient productTypeId et customProductType optionnel (si Autre). "
        "Validation : client existant, priorite enum, adresse obligatoire. Apres save, "
        "publication OrderCreatedEvent si priorite HIGH/CRITICAL."
    )


def expand_dto_detail(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE DETAILLEE - DTO (Data Transfer Objects)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.p(
        "Les DTO separent le contrat API du modele JPA. Validation Bean Validation (@NotNull, "
        "@Email, @Size) sur les Request. Response objects evitent exposition mot de passe."
    )
    requests = [
        "LoginRequest, RegisterRequest", "UserRequest, UpdateProfileRequest",
        "PasswordChangeRequest, RoleUpdateRequest", "OrderRequest (productTypeId, customProductType)",
        "TaskRequest, TaskStatusUpdateRequest", "PriorityUpdateRequest, StatusUpdateRequest",
        "IncidentRequest, IncidentUpdateRequest", "ReviewRequest, DeliveryConfirmRequest",
        "ProofOfDeliveryRequest (image base64)", "LocationUpdateRequest (lat/lng)",
        "ChatSendRequest", "TaskIdRequest",
        "AIDelayPredictionRequest, AIDeliveryTimePredictionRequest",
        "AITaskPrioritizationRequest, AIDriverRecommendationRequest",
        "AIChatRequest, AIRouteOptimizationRequest",
    ]
    for r in requests:
        pdf.bullet(r)
    pdf.ln(2)
    pdf.h2("Responses principales")
    responses = [
        "LoginResponse (token, user)", "UserResponse, PageResponse<T>",
        "OrderResponse, TaskResponse, TaskHistoryResponse",
        "ManagerDashboardResponse, OperatorDashboardResponse",
        "DriverDashboardResponse, ClientDashboardResponse",
        "AIDelayPredictionResponse, AIDeliveryTimePredictionResponse",
        "ExpressChainResultResponse, AutomationLogResponse",
        "ChatReplyResponse, ChatInitResponse, DeliveryTrackingResponse",
        "DriverRouteOptimizationResponse, ApiErrorResponse",
    ]
    for r in responses:
        pdf.bullet(r)


def expand_frontend_components(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE DETAILLEE - COMPOSANTS ANGULAR (49)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    components = [
        ("LoginComponent", "auth/login", "Formulaire authentification"),
        ("AccessDeniedComponent", "access-denied", "Page acces refuse"),
        ("ProfileComponent", "profile", "Profil utilisateur"),
        ("AdminDashboardComponent", "admin", "Dashboard admin"),
        ("AdminUsersComponent", "admin/users", "CRUD utilisateurs"),
        ("ManagerLayoutComponent", "manager", "Layout sidebar manager"),
        ("ManagerDashboardPageComponent", "manager/dashboard", "KPIs manager"),
        ("ManagerTasksPageComponent", "manager/tasks", "Liste/gestion taches"),
        ("ManagerPlanningPageComponent", "manager/planning", "Planning livraisons"),
        ("ManagerMapPageComponent", "manager/map", "Carte missions"),
        ("ManagerDriversPageComponent", "manager/drivers", "Liste chauffeurs"),
        ("ManagerDelaysPageComponent", "manager/delays", "Taches en retard"),
        ("ManagerIncidentsPageComponent", "manager/incidents", "Gestion incidents"),
        ("ManagerNotificationsPageComponent", "manager/notifications", "Notifications"),
        ("ManagerAnalyticsPageComponent", "manager/analytics", "Graphiques analytics"),
        ("ManagerAiPageComponent", "manager/ai", "Predictions IA manager"),
        ("ManagerAutomationPageComponent", "manager/automation", "Journal chaine IA"),
        ("ManagerSettingsPageComponent", "manager/settings", "Parametres"),
        ("OperatorLayoutComponent", "operator", "Layout operateur"),
        ("OperatorDashboardPageComponent", "operator/dashboard", "Dashboard operateur"),
        ("OperatorOrdersPageComponent", "operator/orders", "Liste commandes"),
        ("OperatorOrderCreatePageComponent", "operator/orders/create", "Formulaire + types produit"),
        ("OperatorPendingPageComponent", "operator/orders/pending", "Commandes en attente"),
        ("OperatorTasksPageComponent", "operator/tasks", "Taches preparation"),
        ("OperatorTrackingPageComponent", "operator/tasks/tracking", "Suivi preparation"),
        ("OperatorIncidentsPageComponent", "operator/incidents", "Incidents operateur"),
        ("OperatorSettingsPageComponent", "operator/settings", "Parametres"),
        ("DriverLayoutComponent", "driver", "Layout chauffeur"),
        ("DriverDashboardPageComponent", "driver/dashboard", "Dashboard + alertes IA"),
        ("DriverTasksPageComponent", "driver/tasks", "Liste missions"),
        ("DriverTaskDetailPageComponent", "driver/tasks/:id", "Detail mission"),
        ("DriverRoutePageComponent", "driver/route", "Itineraire optimise IA"),
        ("DriverIncidentsPageComponent", "driver/incidents", "Signaler incident"),
        ("DriverHistoryPageComponent", "driver/history", "Historique livraisons"),
        ("DriverPerformancePageComponent", "driver/performance", "Score performance"),
        ("DriverSettingsPageComponent", "driver/settings", "Parametres"),
        ("ClientLayoutComponent", "client", "Layout client"),
        ("ClientDashboardPageComponent", "client/dashboard", "Dashboard client"),
        ("ClientOrdersPageComponent", "client/orders", "Mes commandes"),
        ("ClientOrderDetailPageComponent", "client/orders/:id", "Detail commande"),
        ("ClientDeliveryPageComponent", "client/delivery/:id", "Suivi SSE livraison"),
        ("ClientNotificationsPageComponent", "client/notifications", "Notifications"),
        ("ClientReviewsPageComponent", "client/reviews", "Mes avis"),
        ("ClientIncidentsPageComponent", "client/incidents", "Signaler probleme"),
        ("ClientSettingsPageComponent", "client/settings", "Parametres"),
        ("ChatWidgetComponent", "shared/chat-widget", "Widget chatbot flottant"),
        ("NavbarComponent", "shared/navbar", "Barre navigation"),
        ("DashboardComponent", "shared/dashboard", "Composant dashboard generique"),
        ("AppComponent", "app", "Racine application"),
    ]
    pdf.table(["Composant", "Chemin", "Role"], components, [55, 45, 80])


def expand_ml_detail(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE DETAILLEE - PIPELINE MACHINE LEARNING", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.h2("Comparaison algorithmes - Modele retard (classification)")
    pdf.table(
        ["Algorithme", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        [
            ["Logistic Regression (retenu)", "0.965", "1.000", "0.965", "0.982", "0.990"],
            ["Random Forest", "0.990", "0.993", "0.997", "0.995", "0.959"],
            ["XGBoost", "0.993", "0.993", "1.000", "0.997", "0.967"],
        ],
        [45, 22, 22, 22, 22, 22],
    )
    pdf.p(
        "Logistic Regression retenu pour interpretabilite et performance suffisante (F1=0.982). "
        "Matrice confusion test : TN=4, FP=0, FN=21, TP=575."
    )
    pdf.h2("Comparaison algorithmes - Modele ETA (regression)")
    pdf.table(
        ["Algorithme", "MAE (min)", "RMSE (min)", "R2"],
        [
            ["Linear Regression", "7.45", "9.43", "0.945"],
            ["Random Forest", "7.14", "8.93", "0.950"],
            ["XGBoost (retenu)", "6.32", "8.02", "0.960"],
        ],
        [45, 30, 30, 30],
    )
    pdf.h2("Scripts d'entrainement")
    pdf.bullet("generate_dataset.py : genere 3000 echantillons synthetiques")
    pdf.bullet("train_delay.py : compare LR, RF, XGBoost, sauve delay_model.pkl")
    pdf.bullet("train_delivery_time.py : compare LR, RF, XGBoost, sauve delivery_time_model.pkl")
    pdf.bullet("train_priority.py : stub (non entraine)")
    pdf.bullet("train_all.py : pipeline complet + model_metadata.json")
    pdf.h2("Inference en production")
    pdf.fig("Flux inference Python", """
PredictionService.load_models() au demarrage FastAPI
POST /predict/delay:
  1. Valider DelayPredictionRequest (Pydantic)
  2. Feature engineering (priority_score, traffic_score)
  3. model.predict_proba(features)
  4. Retourner delayProbability, riskLevel, modelVersion
    """)
    pdf.h2("Evaluation et metriques")
    pdf.p(
        "Classification : accuracy, precision, recall, F1-score, ROC-AUC, matrice confusion. "
        "Regression : MAE, RMSE, R2. Split train/test 80/20 sur dataset synthetique."
    )


def expand_json_examples(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE - EXEMPLES JSON API", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.fig("Exemple POST /api/auth/login - Request", """
{
  "email": "manager@smarttask.com",
  "password": "Manager123!"
}
    """)
    pdf.fig("Exemple POST /api/auth/login - Response", """
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "id": 2, "email": "manager@smarttask.com", "role": "MANAGER" }
}
    """)
    pdf.fig("Exemple POST /api/operator/orders - Request", """
{
  "clientId": 5,
  "productTypeId": 4,
  "customProductType": null,
  "products": "Medicaments urgents",
  "quantity": 1,
  "amount": 150.00,
  "deliveryAddress": "12 Rue Example, Tunis",
  "priority": "HIGH",
  "scheduledDate": "2026-08-30",
  "scheduledTime": "14:00"
}
    """)
    pdf.fig("Exemple POST /api/manager/ai/predict-delay - Response", """
{
  "delayProbability": 0.73,
  "riskLevel": "HIGH",
  "modelVersion": "1.0.0",
  "source": "python-ml"
}
    """)
    pdf.fig("Exemple POST /api/ai/chat - Request (Python)", """
{
  "message": "Combien de livraisons en retard ?",
  "role": "MANAGER",
  "context": [{ "key": "delayed_tasks", "value": "3" }]
}
    """)


def expand_security_detail(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE DETAILLEE - SECURITE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.h2("Matrice d'acces par role")
    pdf.table(
        ["Ressource", "ADMIN", "MANAGER", "OPERATOR", "DRIVER", "CLIENT"],
        [
            ["/api/users CRUD", "OUI", "NON", "NON", "NON", "NON"],
            ["/api/manager/*", "NON", "OUI", "NON", "NON", "NON"],
            ["/api/operator/*", "NON", "NON", "OUI", "NON", "NON"],
            ["/api/driver/*", "NON", "NON", "NON", "OUI", "NON"],
            ["/api/client/*", "NON", "NON", "NON", "NON", "OUI"],
            ["/api/automation/*", "NON", "OUI", "OUI*", "NON", "NON"],
            ["/api/chat/*", "OUI", "OUI", "OUI", "OUI", "OUI"],
            ["/api/product-types", "OUI", "OUI", "OUI", "OUI", "OUI"],
        ],
        [40, 18, 22, 22, 18, 18],
    )
    pdf.p("* Operator : status et express trigger uniquement, pas logs complets.")
    pdf.h2("Bonnes pratiques implementees")
    pdf.bullet("Separation credentials : password jamais dans Response DTO")
    pdf.bullet("Validation entree : @Valid sur controllers")
    pdf.bullet("Gestion erreurs : ApiErrorResponse structure (code, message, timestamp)")
    pdf.bullet("CORS restreint a localhost:4200 en dev")
    pdf.bullet("open-in-view=false : pas de lazy loading hors transaction")
    pdf.h2("Recommandations production")
    pdf.bullet("Changer app.jwt.secret (256 bits minimum)")
    pdf.bullet("HTTPS obligatoire")
    pdf.bullet("Rate limiting sur /api/auth/login")
    pdf.p("Fonctionnalite prevue / future amelioration : refresh token, 2FA, audit log securite.")


def expand_flyway_detail(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE DETAILLEE - MIGRATIONS FLYWAY", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    migrations = [
        ("V1", "users", "id PK, first_name, last_name, email UNIQUE, password, phone, role CHECK, active, timestamps"),
        ("V2", "driver_profiles", "user_id FK UNIQUE, status, zone, current_load, performance_score"),
        ("V2", "tasks", "client_id, driver_id, created_by FK, title, status, priority, deadline, geo"),
        ("V2", "task_history", "task_id FK, performed_by FK, action, old/new status"),
        ("V2", "notifications", "user_id FK, related_task_id FK, type, title, message, read_flag"),
        ("V3", "orders", "client_id, operator_id FK, products TEXT, amount, status, priority, task_id"),
        ("V3", "incidents", "reporter_id, task_id, order_id FK, type, status, description"),
        ("V3", "reviews", "client_id, task_id FK UNIQUE, rating 1-5, comment"),
        ("V4", "orders", "Ajout statut RECEIVED dans CHECK constraint"),
        ("V5", "seed", "Commande DELIVERED test pour client1@smarttask.com"),
        ("V6", "indexes", "Composite idx tasks(status,priority), orders(status), incidents(status)"),
        ("V7", "tasks", "Colonne proof_of_delivery_image TEXT"),
        ("V8", "chat_messages", "user_id FK, role, content, session_id, intent, created_at"),
        ("V9", "automation_logs", "run_id, chain_type, order_id, task_id, step_number, step_name, status"),
        ("V10", "product_types", "6 types seeds + product_type_id FK sur orders"),
    ]
    pdf.table(["Version", "Objet", "Detail"], migrations, [18, 35, 127])


def expand_tests_detail(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE DETAILLEE - PLAN DE TESTS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.table(
        ["Test", "Entree", "Resultat attendu", "Type"],
        [
            ["Login valide", "manager@smarttask.com / Manager123!", "JWT 200", "Manuel/JUnit"],
            ["Login invalide", "email wrong / pwd wrong", "401 Unauthorized", "JUnit"],
            ["Acces ADMIN users", "Token MANAGER sur /api/users", "403 Forbidden", "Security test"],
            ["Creer commande HIGH", "OrderRequest priority HIGH", "Order + automation logs", "Manuel"],
            ["Predict delay", "taskId existant", "delayProbability 0-1", "ManagerAIControllerTest"],
            ["Automation manuelle", "POST express/{orderId}", "7 steps SUCCESS/SKIPPED", "AutomationControllerTest"],
            ["Python health", "GET /api/ai/health", "status ok", "pytest test_api"],
            ["Chat message", "POST /api/chat/message", "reply + intent", "pytest test_chat"],
            ["Route optimize", "2+ missions driver", "orderedTaskIds", "Manuel"],
            ["SSE delivery", "GET stream client", "events status updates", "Manuel"],
            ["Creer avis", "rating 5 + taskId", "Review saved unique", "Manuel"],
            ["Product types", "GET /api/product-types", "6 types actifs", "Manuel"],
        ],
        [38, 52, 55, 35],
    )
    pdf.h2("Build et compilation")
    pdf.bullet("Backend : gradlew compileJava test (Java 17)")
    pdf.bullet("Frontend : ng build --configuration production")
    pdf.bullet("Python : pytest smarttask-ai/tests/")


def expand_ux_ui(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "CHAPITRE COMPLEMENTAIRE - UX/UI", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.h2("Navigation et ergonomie")
    pdf.p(
        "Chaque role dispose d'un layout dedie (sidebar) avec routes lazy-loaded. "
        "Le ChatWidgetComponent est accessible globalement pour assistance contextuelle."
    )
    pdf.bullet("Manager : navigation 12 pages, accent sur IA et automation")
    pdf.bullet("Operator : workflow guide creation commande avec dropdown types produit")
    pdf.bullet("Driver : actions mission en un clic (accept, start, complete)")
    pdf.bullet("Client : suivi livraison visuel avec timeline et SSE")
    pdf.h2("Feedback utilisateur")
    pdf.bullet("Messages erreur HTTP affiches dans composants")
    pdf.bullet("Validation formulaires cote Angular + backend @Valid")
    pdf.bullet("Indicateurs chargement sur appels API (RxJS finalize)")
    pdf.bullet("Notifications in-app via NotificationResponse")
    pdf.h2("Design system")
    pdf.p(
        "Styles globaux dans smarttask-frontend/src/styles. Composants shared reutilisables "
        "(navbar, dashboard, chat-widget). Information non identifiee dans les fichiers "
        "fournis pour framework CSS externe (Bootstrap/Tailwind) - styles custom observes."
    )
    pdf.p(
        "Fonctionnalite prevue / future amelioration : mode sombre, internationalisation i18n, "
        "application mobile responsive native."
    )


def expand_scenario_jury(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "SCENARIO DETAILLE DE SOUTENANCE (DEMO JURY)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    steps = [
        ("Etape 1", "Demarrer PostgreSQL, Spring Boot (9090), Python IA (8000), Angular (4200)"),
        ("Etape 2", "Operator login : operator1@smarttask.com / Operator123!"),
        ("Etape 3", "Creer commande : type MEDICAMENTS, priorite HIGH, client existant"),
        ("Etape 4", "Observer logs backend : OrderCreatedEvent -> automation 7 etapes"),
        ("Etape 5", "Manager login : consulter /manager/automation -> 7 logs SUCCESS"),
        ("Etape 6", "Manager /manager/ai : predire retard sur tache creee"),
        ("Etape 7", "Driver login : voir mission assignee, page Route optimisee"),
        ("Etape 8", "Driver : accepter, demarrer, uploader preuve, completer livraison"),
        ("Etape 9", "Client login : suivi SSE /client/delivery/{id}"),
        ("Etape 10", "Client : confirmer reception, avis 5 etoiles"),
        ("Etape 11", "Tous roles : tester ChatWidget Copilot avec question metier"),
        ("Etape 12", "Swagger : demontrer documentation OpenAPI /api-docs"),
    ]
    for title, desc in steps:
        pdf.h3(title)
        pdf.p(desc)


def expand_glossary(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "GLOSSAIRE TECHNIQUE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    terms = [
        ("API REST", "Interface HTTP JSON entre frontend et backend"),
        ("JWT", "JSON Web Token - authentification stateless"),
        ("RBAC", "Role-Based Access Control - controle acces par role"),
        ("JPA", "Java Persistence API - ORM Hibernate"),
        ("ORM", "Object-Relational Mapping - mapping objet/relationnel"),
        ("DTO", "Data Transfer Object - objet transfert API"),
        ("SSE", "Server-Sent Events - flux temps reel unidirectionnel"),
        ("ML", "Machine Learning - apprentissage automatique"),
        ("FastAPI", "Framework Python API async base sur Pydantic"),
        ("WebClient", "Client HTTP reactif Spring WebFlux"),
        ("Flyway", "Outil migrations SQL versionnees"),
        ("TSP", "Traveling Salesman Problem - optimisation itineraire"),
        ("SPA", "Single Page Application - Angular"),
        ("BCrypt", "Algorithme hash mots de passe"),
        ("CORS", "Cross-Origin Resource Sharing"),
        ("CRUD", "Create Read Update Delete"),
        ("ETA", "Estimated Time of Arrival - temps estime arrivee"),
        ("ROC-AUC", "Metrique classification - aire sous courbe ROC"),
        ("F1-Score", "Moyenne harmonique precision et recall"),
        ("Microservice", "Service autonome deployable independamment"),
    ]
    pdf.table(["Terme", "Definition"], terms, [40, 140])


def expand_project_structure(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXE - ARBORESCENCE PROJET", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.fig("Structure racine ProjetPidev", """
ProjetPidev/
  Backend Smarttask/SmartTask/     Spring Boot (Gradle, Java 17)
  smarttask-frontend/              Angular 16 SPA
  smarttask-ai/                    Python FastAPI microservice IA
  docs/                            Scripts rapport + PDF generes
    """)
    pdf.fig("Structure smarttask-ai", """
smarttask-ai/
  app/main.py
  app/api/           health, predict, chat, route
  app/services/      PredictionService, RouteOptimizationService
  app/ml/            train_delay, train_delivery_time, train_all
  app/models/        .pkl + model_metadata.json
  app/data/          knowledge_base.json
  tests/             test_api.py, test_chat.py
  Dockerfile
  requirements.txt
    """)
    pdf.fig("Structure smarttask-frontend", """
smarttask-frontend/src/app/
  core/              auth, guards, interceptors, services, models
  features/
    admin/           dashboard, users
    manager/           12 pages + layout
    operator/          8 pages + layout
    driver/            8 pages + layout
    client/            8 pages + layout
    auth/              login
  shared/              chat-widget, navbar, dashboard
  app.routes.ts
    """)


def remerciements(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "REMERCIEMENTS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    pdf.p(
        "Je tiens a exprimer ma profonde gratitude a toutes les personnes qui ont contribue "
        "a la realisation de ce projet de fin d'etudes."
    )
    pdf.p(
        "Mes remerciements s'adressent en premier lieu a mon encadrant [A completer] pour "
        "son accompagnement, ses conseils et sa disponibilite tout au long du developpement "
        "de la plateforme SmartLogix."
    )
    pdf.p(
        "Je remercie egalement l'equipe pedagogique de [Etablissement - A completer] pour "
        "la formation de qualite qui m'a permis d'acquerir les competences necessaires en "
        "genie logiciel, architecture distribuee et intelligence artificielle."
    )
    pdf.p(
        "Enfin, je remercie ma famille et mes proches pour leur soutien moral et leur "
        "encouragement durant cette periode exigeante."
    )


def annexes(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "ANNEXES", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.h2("Annexe A - Comptes de test")
    pdf.table(
        ["Email", "Mot de passe", "Role"],
        [
            ["admin@smarttask.com", "Admin123!", "ADMIN"],
            ["manager@smarttask.com", "Manager123!", "MANAGER"],
            ["operator1@smarttask.com", "Operator123!", "OPERATOR"],
            ["driver1@smarttask.com", "Driver123!", "DRIVER"],
            ["client1@smarttask.com", "Client123!", "CLIENT"],
        ],
        [65, 45, 40],
    )
    pdf.h2("Annexe B - Types produit (V10)")
    pdf.table(
        ["Code", "Nom"],
        [
            ["DOCUMENTS", "Documents et courrier"],
            ["COLIS_STANDARD", "Colis standard"],
            ["COLIS_FRAGILE", "Colis fragile"],
            ["MEDICAMENTS", "Medicaments"],
            ["EQUIPEMENT", "Equipement lourd"],
            ["ALIMENTAIRE", "Produits alimentaires"],
        ],
        [50, 130],
    )
    pdf.h2("Annexe C - Configuration application.properties")
    pdf.bullet("server.port=9090")
    pdf.bullet("spring.datasource.url=jdbc:postgresql://localhost:5432/smarttask_db")
    pdf.bullet("app.ai.service-url=http://localhost:8000")
    pdf.bullet("app.automation.express.enabled=true")
    pdf.bullet("app.automation.express.auto-trigger-priorities=HIGH,CRITICAL")
    pdf.bullet("app.driver.alerts.enabled=true")
    pdf.bullet("app.driver.alerts.interval-ms=300000")
    pdf.h2("Annexe D - URLs utiles")
    pdf.bullet("Frontend : http://localhost:4200")
    pdf.bullet("Swagger : http://localhost:9090/swagger-ui.html")
    pdf.bullet("Python docs : http://localhost:8000/docs")
    pdf.h2("Annexe E - Enums principaux")
    pdf.p("Role: ADMIN, MANAGER, OPERATOR, DRIVER, CLIENT")
    pdf.p("Priority: LOW, MEDIUM, HIGH, CRITICAL")
    pdf.p("TaskStatus: PENDING, PREPARED, ASSIGNED, ACCEPTED, IN_PROGRESS, IN_DELIVERY, COMPLETED, CANCELLED")
    pdf.p("OrderStatus: PENDING, VERIFIED, PREPARING, READY, IN_DELIVERY, DELIVERED, RECEIVED, CANCELLED")


def resume_content(pdf):
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "RESUME EXECUTIF", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    pdf.p(
        f"{PROJECT} est une plateforme logistique intelligente developpee en Java Spring Boot, "
        "Angular et Python. Elle dessert 5 roles (Admin, Manager, Operator, Driver, Client) "
        "et couvre le cycle complet commande-livraison-avis."
    )
    pdf.p(
        "Architecture : Angular (4200) -> Spring Boot (9090) -> PostgreSQL + Python FastAPI (8000). "
        f"{len(ENDPOINTS)} endpoints REST, 11 entites JPA, 10 migrations Flyway, 49 composants Angular."
    )
    pdf.p(
        "Intelligence artificielle : prediction retard (F1=0.982), ETA (MAE=6.3 min), "
        "chaine automation 7 etapes, chatbot Copilot, optimisation itineraire, alertes chauffeur."
    )
    pdf.p(
        "Securite JWT, RBAC, BCrypt. Tests : JUnit (7 fichiers), pytest (14 tests). "
        "Docker partiel (service IA). Perspectives : CI/CD, donnees reelles ML, mobile chauffeur."
    )


def write_diagrams():
    os.makedirs(DIAGRAM_DIR, exist_ok=True)
    diagrams = {
        "01_architecture_generale.txt": """
Utilisateur -> Angular 4200 -> Spring Boot 9090 -> PostgreSQL 5432
                                      |
                                      v
                              Python FastAPI 8000
        """,
        "02_use_case_global.txt": "Voir Figure 5.1 du rapport",
        "03_class_diagram.txt": "User-Task-Order-ProductType relations (voir Chapitre 6)",
        "04_sequence_auth.txt": "Login -> JWT -> Bearer requests",
        "05_sequence_automation.txt": "Order HIGH -> Event -> 7 steps automation",
        "06_erd.txt": "11 tables PostgreSQL Flyway V1-V10",
    }
    for name, content in diagrams.items():
        path = os.path.join(DIAGRAM_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())


def build_main():
    write_diagrams()
    pdf = RapportPFE()
    cover(pdf)
    toc_page(pdf)
    list_figures_tables(pdf)
    pdf.add_page()
    resume_content(pdf)
    cartographie(pdf)
    chapitre_1(pdf)
    chapitre_2(pdf)
    chapitre_3(pdf)
    chapitre_4(pdf)
    chapitre_5(pdf)
    chapitre_6(pdf)
    chapitre_7(pdf)
    chapitre_8(pdf)
    chapitre_9(pdf)
    chapitre_10(pdf)
    chapitre_11(pdf)
    chapitre_12_21(pdf)
    expand_backend_detail(pdf)
    expand_dto_detail(pdf)
    expand_frontend_components(pdf)
    expand_ml_detail(pdf)
    expand_json_examples(pdf)
    expand_security_detail(pdf)
    expand_flyway_detail(pdf)
    expand_tests_detail(pdf)
    expand_ux_ui(pdf)
    expand_scenario_jury(pdf)
    expand_glossary(pdf)
    expand_project_structure(pdf)
    annexes(pdf)
    remerciements(pdf)
    pdf.output(OUT_PDF)
    return OUT_PDF, pdf.page_no()


def build_resume():
    pdf = RapportPFE()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, f"Resume Executif - {PROJECT}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    resume_content(pdf)
    pdf.output(OUT_RESUME)
    return OUT_RESUME


if __name__ == "__main__":
    path, pages = build_main()
    build_resume()
    print(f"Rapport genere : {path}")
    print(f"Nombre de pages : {pages}")
    print(f"Resume : {OUT_RESUME}")
    print(f"Diagrammes : {DIAGRAM_DIR}")
