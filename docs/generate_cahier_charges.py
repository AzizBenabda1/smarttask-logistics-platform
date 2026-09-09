# -*- coding: utf-8 -*-
"""
Generateur Cahier des Charges SmartLogix Prioritizer with IA
Document de commande entreprise -> equipe de developpement
40-50 pages PDF via fpdf2
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
OUT_PDF = os.path.join(OUT_DIR, "Cahier_des_charges_SmartLogix.pdf")
OUT_MD = os.path.join(OUT_DIR, "Cahier_des_charges_SmartLogix.md")
DIAGRAM_DIR = os.path.join(OUT_DIR, "diagrammes")

DOC_TITLE = "SmartLogix Prioritizer with IA"
DOC_VERSION = "1.0"
DOC_DATE = date.today().strftime("%d/%m/%Y")


class CahierCharges(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(15, 15, 15)
        self.chapter = 0

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"{DOC_TITLE} | Cahier des Charges v{DOC_VERSION} | Page {self.page_no()}", align="C")

    def h1(self, num, title):
        self.chapter = num
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
            self.set_fill_color(240, 244, 248) if fill else self.set_fill_color(255, 255, 255)
            self.set_text_color(30, 30, 30)
            for i, cell in enumerate(row):
                self.cell(widths[i], 5.5, str(cell)[:58], border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(2)

    def req(self, ref, desc, prio="Must"):
        self.bullet(f"[{ref}] ({prio}) {desc}")


def load_diagram(name):
    path = os.path.join(DIAGRAM_DIR, name)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return "(Diagramme non disponible)"


def cover(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "DOCUMENT DE COMMANDE INTERNE", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(15, 60, 110)
    pdf.cell(0, 12, "CAHIER DES CHARGES", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, DOC_TITLE, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "Plateforme intelligente de gestion et priorisation", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, "des operations logistiques de derniere mile", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(18)
    meta = [
        ("Commanditaire", "Direction Operations & Innovation Digitale"),
        ("Projet", "SmartLogix / SmartTask"),
        ("Reference document", "CDC-SLX-2026-001"),
        ("Version", DOC_VERSION),
        ("Date", DOC_DATE),
        ("Classification", "Confidentiel - Usage interne"),
        ("Destinataire", "Equipe de developpement (prestataire / PFE)"),
        ("Statut", "Valide pour lancement"),
    ]
    for k, v in meta:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(55, 7, k + " :", align="R")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, v, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5,
        "Ce document definit les exigences fonctionnelles et non fonctionnelles "
        "de la solution a developper. Il sert de reference contractuelle entre "
        "le commanditaire et l'equipe de realisation.", align="C")


def approval_page(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Validation du document", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    pdf.table(
        ["Role", "Nom", "Signature", "Date"],
        [
            ["MOA - Sponsor projet", "[A completer]", "", ""],
            ["MOA - Responsable metier", "[A completer]", "", ""],
            ["MOE - Chef de projet", "[A completer]", "", ""],
            ["MOE - Architecte technique", "[A completer]", "", ""],
        ],
        [40, 50, 45, 45],
    )
    pdf.h2("Historique des revisions")
    pdf.table(
        ["Version", "Date", "Auteur", "Modifications"],
        [
            ["0.1", "01/2026", "Direction SI", "Ebauche initiale"],
            ["0.5", "02/2026", "Equipe AMOA", "Besoins fonctionnels detailles"],
            ["1.0", DOC_DATE, "Comite projet", "Version validee pour developpement"],
        ],
        [20, 25, 45, 90],
    )


def toc_page(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Table des matieres", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    items = [
        "Introduction et objet du document",
        "Contexte et presentation du commanditaire",
        "Problematique metier",
        "Solution proposee SmartLogix",
        "Etude de l'existant",
        "Critique de l'existant",
        "Besoins fonctionnels",
        "Besoins non fonctionnels",
        "Contraintes, hypotheses et perimetre",
        "Methodologie de realisation adoptee",
        "Planning previsionnel et jalons",
        "Architecture cible du systeme",
        "Modele de donnees et regles metier",
        "Interfaces utilisateur et parcours",
        "Specifications des API",
        "Intelligence artificielle et priorisation",
        "Securite et conformite",
        "Criteres d'acceptation et recette",
        "Livrables attendus",
        "Gestion des risques",
        "Personas metier et user stories",
        "Workflows metier detailles",
        "Annexe A - Catalogue complet API",
        "Exigences DevOps et deploiement",
        "Qualite, tests et communication",
        "Glossaire et annexes",
    ]
    pdf.set_font("Helvetica", "", 11)
    for i, item in enumerate(items, 1):
        pdf.cell(0, 6.5, f"{i}. {item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def ch1_intro(pdf):
    pdf.h1(1, "INTRODUCTION ET OBJET DU DOCUMENT")
    pdf.h2("1.1 Objet")
    pdf.p(
        "Le present cahier des charges a pour objet de definir, de maniere exhaustive et "
        "non ambigue, les exigences auxquelles doit repondre la solution SmartLogix Prioritizer "
        "with IA (ci-apres SmartLogix ou la Solution). Ce document est emis par la Direction "
        "Operations & Innovation Digitale en qualite de maitre d'ouvrage (MOA) et adresse a "
        "l'equipe de developpement chargee de la conception, realisation, tests et mise en "
        "production de la plateforme."
    )
    pdf.h2("1.2 Perimetre du document")
    pdf.p(
        "Le perimetre couvre l'ensemble du cycle de vie initial du produit : analyse, "
        "conception, developpement, integration, tests, documentation utilisateur et "
        "deploiement en environnement de pre-production. Sont exclus du present document : "
        "la maintenance corrective de niveau 3 apres garantie, l'integration avec des ERP "
        "tiers non specifies, et le deploiement multi-pays hors Tunisie."
    )
    pdf.h2("1.3 Destinataires")
    pdf.table(
        ["Profil", "Usage du document"],
        [
            ["Chef de projet MOE", "Pilotage, planning, suivi des exigences"],
            ["Developpeurs backend/frontend/IA", "Specifications techniques detaillees"],
            ["Architecte", "Coherence architecture et integrations"],
            ["Testeurs / QA", "Scenarios de recette et criteres d'acceptation"],
            ["Product Owner MOA", "Validation fonctionnelle"],
            ["Encadrant academique (PFE)", "Evaluation du projet etudiant"],
        ],
        [55, 125],
    )
    pdf.h2("1.4 Documents de reference")
    pdf.bullet("Norme ISO/IEC 25010 - Qualite des produits logiciels")
    pdf.bullet("OWASP Top 10 - Securite applicative web")
    pdf.bullet("Guide AMOA logistique derniere mile - secteur transport")
    pdf.bullet("Reglement general sur la protection des donnees (RGPD) - principes applicables")
    pdf.bullet("Documentation interne : processus commande-livraison actuel (v2.3)")


def ch2_contexte(pdf):
    pdf.h1(2, "CONTEXTE ET PRESENTATION DU COMMANDITAIRE")
    pdf.h2("2.1 Presentation de l'organisation")
    pdf.p(
        "Le commanditaire est une entreprise de logistique et distribution operating in Tunisia, "
        "specialisee dans la livraison de colis, documents et produits sensibles (pharmaceutiques, "
        "electronique). L'activite couvre le dernier kilometre (last-mile delivery) avec un reseau "
        "de chauffeurs independants et salariees, un centre d'appels operateur, et une clientèle "
        "B2B/B2C croissante."
    )
    pdf.h2("2.2 Contexte strategique")
    pdf.p(
        "Face a la concurrence des plateformes digitales et a l'augmentation des attentes clients "
        "(suivi temps reel, fenetres horaires respectees, transparence), la direction a lance "
        "un programme de transformation numerique 2025-2027. SmartLogix constitue le pilier "
        "operationnel de ce programme : centraliser les commandes, automatiser la priorisation, "
        "optimiser les tournées chauffeurs et reduire les echecs de livraison."
    )
    pdf.h2("2.3 Acteurs metier concernes")
    pdf.table(
        ["Acteur", "Role", "Volume estime"],
        [
            ["Administrateur (ADMIN)", "Gestion utilisateurs, roles, configuration", "2-3"],
            ["Manager logistique (MANAGER)", "Supervision, assignation, IA, analytics", "5-10"],
            ["Operateur (OPERATOR)", "Saisie/verification commandes, preparation", "15-25"],
            ["Chauffeur (DRIVER)", "Execution livraisons, GPS, preuves", "50-150"],
            ["Client (CLIENT)", "Commandes, suivi, avis, incidents", "5000+"],
            ["Systeme IA", "Predictions, recommandations, automation", "Automatique"],
        ],
        [45, 85, 50],
    )
    pdf.h2("2.4 Objectifs strategiques du projet")
    pdf.bullet("Reduire de 25% les retards de livraison dans les 12 mois suivant la mise en production")
    pdf.bullet("Automatiser 60% des commandes prioritaires (HIGH/CRITICAL) sans intervention manuelle")
    pdf.bullet("Ameliorer le taux de reussite au premier passage de livraison de 78% a 90%")
    pdf.bullet("Fournir une visibilite temps reel aux clients finaux")
    pdf.bullet("Industrialiser les decisions d'assignation chauffeur via IA explicable")


def ch3_problematique(pdf):
    pdf.h1(3, "PROBLEMATIQUE METIER")
    pdf.h2("3.1 Constat general")
    pdf.p(
        "Aujourd'hui, la gestion des operations logistiques repose sur des processus partiellement "
        "manualises, des fichiers Excel partages, des echanges telephoniques entre operateurs et "
        "chauffeurs, et une absence d'outil unifie de priorisation. Les managers passent en moyenne "
        "2 heures par jour a reconcilier les commandes, identifier les retards potentiels et "
        "reassigner manuellement les missions."
    )
    pdf.h2("3.2 Problemes identifies")
    pdf.h3("3.2.1 Fragmentation des outils")
    pdf.p(
        "Les commandes sont saisies dans un outil, les taches assignees par email ou WhatsApp, "
        "le suivi GPS effectue via une application tierce non integree. Aucune source de verite "
        "unique n'existe. Les donnees historiques ne sont pas exploitables pour l'analyse predictive."
    )
    pdf.h3("3.2.2 Priorisation subjective")
    pdf.p(
        "La priorisation des livraisons depend de l'experience individuelle du manager. Deux managers "
        "peuvent traiter differemment une commande CRITICAL selon leur charge de travail. Il n'existe "
        "pas de score objectif combinant distance, historique client, type produit et charge chauffeur."
    )
    pdf.h3("3.2.3 Retards et echecs de livraison")
    pdf.p(
        "En 2025, 22% des livraisons ont subi un retard superieur a 30 minutes. 15% des tentatives "
        "ont echoue au premier passage (client absent, adresse incorrecte, produit refuse). Ces "
        "echecs generent des couts de re-livraison, des reclamations et une degradation de la "
        "satisfaction client (NPS actuel : 32)."
    )
    pdf.h3("3.2.4 Manque de visibilite client")
    pdf.p(
        "Les clients contactent le call center pour connaitre le statut de leur livraison. "
        "Aucun portail self-service n'est disponible. Les notifications sont envoiees manuellement "
        "par SMS avec un delai moyen de 45 minutes apres changement de statut."
    )
    pdf.h3("3.2.5 Absence d'intelligence operationnelle")
    pdf.p(
        "Les decisions d'assignation chauffeur ne tiennent pas compte systematiquement de la "
        "performance historique, de la zone geographique, ni du risque de retard predit. "
        "L'optimisation d'itineraire est rarement appliquee lorsque un chauffeur a plusieurs "
        "missions simultanees."
    )
    pdf.h2("3.3 Question centrale")
    pdf.p(
        "Comment concevoir et deployer une plateforme web integrée, securisee et intelligente, "
        "permettant de piloter l'ensemble du cycle commande-livraison, de prioriser automatiquement "
        "les taches critiques, d'optimiser les tournées chauffeurs et de predire les risques "
        "de retard et d'echec de livraison, tout en offrant une experience client temps reel ?"
    )
    pdf.h2("3.4 Enjeux")
    pdf.table(
        ["Enjeu", "Impact si non traite"],
        [
            ["Operationnel", "Perte de productivite, surcharge managers"],
            ["Financier", "Couts re-livraison, penalites contractuelles B2B"],
            ["Client", "Churn, avis negatifs, pression concurrentielle"],
            ["RH", "Turnover chauffeurs par manque d'outils"],
            ["Reglementaire", "Tracabilite insuffisante pour produits sensibles"],
        ],
        [45, 135],
    )
    pdf.h2("3.5 Impact chiffre estime")
    pdf.p(
        "logistiques a environ 180 000 TND : re-livraisons (45 000 TND), temps managers (60 000 TND), "
        "appels call center suivi (35 000 TND), penalites B2B (25 000 TND), churn client (15 000 TND). "
        "SmartLogix vise un ROI positif des la premiere annee si les KPIs cibles sont atteints."
    )
    pdf.h2("3.6 Parties prenantes impactees")
    pdf.bullet("Direction generale : visibilite KPI strategiques")
    pdf.bullet("Service logistique : outil operationnel quotidien")
    pdf.bullet("Service client : reduction appels suivi")
    pdf.bullet("Chauffeurs : missions clarifiees, moins d'appels")
    pdf.bullet("Clients finaux : experience digitale moderne")
    pdf.bullet("SI interne : maintenance plateforme conteneurisee")


def ch4_solution(pdf):
    pdf.h1(4, "SOLUTION PROPOSEE SMARTLOGIX")
    pdf.h2("4.1 Vision produit")
    pdf.p(
        "SmartLogix Prioritizer with IA est une plateforme web multi-acteurs qui couvre le "
        "workflow complet : prise de commande, verification, preparation, creation de tache "
        "logistique, assignation chauffeur (manuelle ou IA), execution livraison avec preuve, "
        "suivi client temps reel, gestion incidents et analytics manager."
    )
    pdf.h2("4.2 Principes directeurs de la solution")
    pdf.bullet("Architecture microservices leger : backend metier + microservice IA decouple")
    pdf.bullet("Single source of truth : PostgreSQL centralise via Spring Boot")
    pdf.bullet("Securite by design : JWT, RBAC 5 roles, CORS controle")
    pdf.bullet("IA explicable : scores accompagnes de facteurs contributifs")
    pdf.bullet("Automation opt-in : chaine express declenchable automatiquement ou manuellement")
    pdf.bullet("Resilience : fallbacks rule-based si microservice IA indisponible")
    pdf.h2("4.3 Composants majeurs")
    pdf.table(
        ["Composant", "Technologie", "Port", "Responsabilite"],
        [
            ["Frontend web", "Angular 16", "4200 / 80", "Interfaces multi-role"],
            ["Backend API", "Spring Boot 4.1 / Java 17", "9090", "Metier, securite, persistence"],
            ["Microservice IA", "Python FastAPI", "8000", "ML, scoring, chatbot, routes"],
            ["Base de donnees", "PostgreSQL 15+", "5432", "Donnees transactionnelles"],
            ["Reverse proxy", "Nginx (cible prod)", "80/443", "Routage, SSL, cache statique"],
        ],
        [40, 50, 25, 65],
    )
    pdf.h2("4.4 Flux metier cible")
    pdf.fig("Figure 4.1 - Architecture generale", load_diagram("01_architecture_generale.txt"))
    pdf.p(
        "Le frontend Angular ne communique jamais directement avec le microservice Python. "
        "Toutes les requetes IA transitent par Spring Boot qui agit comme orchestrateur, "
        "applique les regles metier et journalise les decisions."
    )
    pdf.h2("4.5 Innovations cles")
    pdf.bullet("Priorisation IA des taches avec score explicable")
    pdf.bullet("Recommandation chauffeur multi-criteres")
    pdf.bullet("Prediction retard et temps de livraison (ML)")
    pdf.bullet("Delivery Success AI : probabilite reussite premier passage")
    pdf.bullet("Automation chaine express 7 etapes pour commandes HIGH/CRITICAL")
    pdf.bullet("Optimisation itineraire TSP pour chauffeurs multi-missions")
    pdf.bullet("Alertes proactives chauffeur (scheduler 5 min)")
    pdf.bullet("Chatbot Copilot contextuel SmartLogix")


def ch5_existant(pdf):
    pdf.h1(5, "ETUDE DE L'EXISTANT")
    pdf.h2("5.1 Methodologie d'audit")
    pdf.p(
        "Une mission d'audit AMOA a ete conduite sur 4 semaines (janvier 2026) comprenant : "
        "entretiens 12 collaborateurs, shadowing operateurs (3 jours), analyse de 1500 "
        "commandes historiques, benchmark 5 solutions du marche, et cartographie AS-IS des "
        "processus."
    )
    pdf.h2("5.2 Processus actuel (AS-IS)")
    pdf.h3("5.2.1 Prise de commande")
    pdf.p(
        "Le client appelle le centre de relation ou envoie un email. L'operateur saisit la "
        "commande dans un tableur partage ou un CRM basique. Validation manuelle par appel "
        "retour. Delai moyen de prise en charge : 35 minutes."
    )
    pdf.h3("5.2.2 Preparation et dispatch")
    pdf.p(
        "Le manager consulte le tableur chaque matin, cree mentalement un plan de tournées, "
        "contacte les chauffeurs par telephone. Aucune trace numerique de la decision d'assignation. "
        "Temps moyen d'assignation : 15 minutes par commande urgente."
    )
    pdf.h3("5.2.3 Execution livraison")
    pdf.p(
        "Le chauffeur utilise Google Maps independamment. La preuve de livraison est une photo "
        "WhatsApp envoyee au manager. Mise a jour statut manuelle dans le tableur en fin de journee."
    )
    pdf.h3("5.2.4 Suivi client")
    pdf.p(
        "Le client rappelle le call center. L'operateur contacte le chauffeur par telephone pour "
        "obtenir une estimation. Pas de notification automatique."
    )
    pdf.h2("5.3 Outils existants inventorie")
    pdf.table(
        ["Outil", "Usage", "Limites"],
        [
            ["Excel / Google Sheets", "Suivi commandes", "Pas de workflow, conflits version"],
            ["WhatsApp", "Communication chauffeurs", "Non tracable, donnees eparses"],
            ["CRM basique", "Fiche client", "Non integre livraison"],
            ["Google Maps", "Navigation", "Pas lie aux missions"],
            ["SMS manuel", "Notifications", "Lent, couteux, non personnalise"],
        ],
        [45, 50, 85],
    )
    pdf.h2("5.4 Benchmark solutions marche")
    pdf.table(
        ["Solution", "Points forts", "Points faibles vs besoin"],
        [
            ["Onfleet", "Tracking, API", "Cout eleve, IA limitee, pas on-premise"],
            ["Bringg", "Orchestration", "Complexite, surdimensionne PME"],
            ["Odoo Logistics", "ERP integre", "Personnalisation lourde, IA basique"],
            ["Developpement interne", "Adapte metier", "Investissement initial"],
        ],
        [35, 55, 90],
    )
    pdf.p(
        "Conclusion audit : aucune solution COTS ne combine priorisation IA explicable, "
        "automation chaine express, suivi SSE client et controle total des donnees. "
        "Le developpement sur mesure SmartLogix est retenu."
    )


def ch6_critique(pdf):
    pdf.h1(6, "CRITIQUE DE L'EXISTANT")
    pdf.h2("6.1 Analyse SWOT de la situation actuelle")
    pdf.h3("Forces")
    pdf.bullet("Equipe metier experimentee (5+ ans en moyenne)")
    pdf.bullet("Base clients fidele malgre les irritants")
    pdf.bullet("Connaissance fine des zones geographiques tunisiennes")
    pdf.h3("Faiblesses")
    pdf.bullet("Processus non standardises entre equipes")
    pdf.bullet("Donnees non fiables (doublons, statuts obsoletes)")
    pdf.bullet("Dependance aux individus cles (manager senior)")
    pdf.bullet("Zero capacite analytique predictive")
    pdf.h3("Opportunites")
    pdf.bullet("Maturite technologique IA/ML accessible (FastAPI, scikit-learn)")
    pdf.bullet("Demande client forte pour suivi digital")
    pdf.bullet("Possibilite d'integrer un projet PFE comme accelerateur")
    pdf.h3("Menaces")
    pdf.bullet("Concurrents 100% digital")
    pdf.bullet("Reglementation tracabilite renforcee (produits sensibles)")
    pdf.bullet("Turnover chauffeurs si outils inadaptes")
    pdf.h2("6.2 Critique detaillee par dimension")
    pdf.h3("6.2.1 Processus")
    pdf.p(
        "Les processus AS-IS ne possedent pas de workflow formalise avec etats transitions valides. "
        "Les statuts sont mis a jour de maniere asynchrone et parfois incoherente (commande DELIVERED "
        "alors que tache encore IN_DELIVERY). La Solution DOIT imposer un workflow OrderStatus et "
        "TaskStatus avec transitions controlees cote backend."
    )
    pdf.h3("6.2.2 Donnees")
    pdf.p(
        "L'absence de base relationnelle centralisee empeche toute requete analytique fiable. "
        "Les historiques de performance chauffeur sont estimes, pas mesures. La Solution DOIT "
        "persister TaskHistory, AutomationLog, ChatMessage et Review pour audit complet."
    )
    pdf.h3("6.2.3 Technique")
    pdf.p(
        "Les outils actuels ne sont pas integrables via API. Aucune authentification centralisee. "
        "La Solution DOIT exposer une API REST securisee JWT documentee OpenAPI/Swagger."
    )
    pdf.h3("6.2.4 Humain")
    pdf.p(
        "La charge cognitive des managers est excessive. Les operateurs ressaisissent des informations "
        "deja connues du CRM. Les chauffeurs perdent du temps a communiquer manuellement. "
        "La Solution DOIT reduire les saisies redondantes et automatiser les notifications."
    )
    pdf.h2("6.3 Ecarts AS-IS vs TO-BE")
    pdf.table(
        ["Capacite", "AS-IS", "TO-BE SmartLogix"],
        [
            ["Priorisation", "Subjective", "Score IA + regles metier"],
            ["Assignation", "Telephone", "Recommandation IA + 1 clic"],
            ["Suivi client", "Call center", "Portail SSE temps reel"],
            ["Preuve livraison", "WhatsApp", "Upload securise + horodatage"],
            ["Analytics", "Inexistant", "Dashboard KPI + export CSV"],
            ["Incidents", "Email", "Workflow OPEN->RESOLVED"],
        ],
        [40, 55, 85],
    )


def ch7_bf(pdf):
    pdf.h1(7, "BESOINS FONCTIONNELS")
    pdf.h2("7.1 Conventions")
    pdf.p(
        "Chaque exigence est identifiee par un code BF-XXX (Must = obligatoire, Should = "
        "souhaitable, Could = optionnel). Priorite Must sauf indication contraire."
    )
    pdf.h2("7.2 Authentification et gestion utilisateurs")
    pdf.req("BF-001", "Le systeme doit permettre l'authentification par email/mot de passe avec JWT")
    pdf.req("BF-002", "Le systeme doit supporter 5 roles : ADMIN, MANAGER, OPERATOR, DRIVER, CLIENT")
    pdf.req("BF-003", "L'ADMIN doit gerer le CRUD utilisateurs avec activation/desactivation")
    pdf.req("BF-004", "Chaque utilisateur doit modifier son profil et mot de passe")
    pdf.req("BF-005", "Le systeme doit rediriger vers le dashboard selon le role apres login")
    pdf.h2("7.3 Module Operateur")
    pdf.req("BF-010", "Creer une commande avec client, type produit, priorite, adresse, montant")
    pdf.req("BF-011", "Verifier une commande PENDING -> VERIFIED")
    pdf.req("BF-012", "Preparer une commande READY et creer la tache associee")
    pdf.req("BF-013", "Consulter dashboard KPI : commandes jour, en attente, pretes")
    pdf.req("BF-014", "Preview Delivery Success AI avant enregistrement commande")
    pdf.req("BF-015", "Signaler un incident lie a une commande")
    pdf.h2("7.4 Module Manager")
    pdf.req("BF-020", "Dashboard KPI : taches actives, retards, chauffeurs disponibles")
    pdf.req("BF-021", "CRUD taches avec filtres statut/priorite/recherche")
    pdf.req("BF-022", "Assigner manuellement ou via recommandation IA (assign-recommended)")
    pdf.req("BF-023", "Consulter retards, incidents, analytics avec export CSV")
    pdf.req("BF-024", "Page IA : predict delay, delivery time, delivery success, anomaly")
    pdf.req("BF-025", "Page automation : lancer chaine express, consulter logs")
    pdf.req("BF-026", "Vue cartes et vue liste pour taches et recommandations IA")
    pdf.h2("7.5 Module Chauffeur")
    pdf.req("BF-030", "Consulter missions assignees avec detail adresse/deadline")
    pdf.req("BF-031", "Workflow mission : accept -> start -> delivery -> complete")
    pdf.req("BF-032", "Mettre a jour position GPS (latitude/longitude)")
    pdf.req("BF-033", "Soumettre preuve livraison (image base64)")
    pdf.req("BF-034", "Consulter itineraire optimise IA multi-missions")
    pdf.req("BF-035", "Recevoir alertes proactives retard (scheduler)")
    pdf.req("BF-036", "Consulter historique et performance personnelle")
    pdf.h2("7.6 Module Client")
    pdf.req("BF-040", "Consulter ses commandes et statuts")
    pdf.req("BF-041", "Suivre livraison temps reel via SSE")
    pdf.req("BF-042", "Confirmer reception -> statut RECEIVED")
    pdf.req("BF-043", "Laisser avis note 1-5 avec commentaire (unique par tache)")
    pdf.req("BF-044", "Signaler incident sur commande/livraison")
    pdf.h2("7.7 Intelligence artificielle")
    pdf.req("BF-050", "Microservice Python expose /api/ai/predict/delay (ML ou fallback)")
    pdf.req("BF-051", "Prediction temps livraison /api/ai/predict/delivery-time")
    pdf.req("BF-052", "Delivery Success AI /api/ai/predict/delivery-success")
    pdf.req("BF-053", "Recommandation chauffeur /api/ai/recommend/driver")
    pdf.req("BF-054", "Priorisation tache /api/ai/prioritize/task")
    pdf.req("BF-055", "Optimisation route /api/ai/optimize/route")
    pdf.req("BF-056", "Chatbot Copilot /api/ai/chat avec suggestions")
    pdf.req("BF-057", "Health et model/status pour supervision")
    pdf.h2("7.8 Automation")
    pdf.req("BF-060", "Chaine express 7 etapes : verify, create task, prioritize, assign, notify")
    pdf.req("BF-061", "Declenchement auto sur OrderCreatedEvent si priorite HIGH/CRITICAL")
    pdf.req("BF-062", "Journal AutomationLog avec runId, stepNumber, status")
    pdf.h2("7.9 Cas d'utilisation detailles")
    for i, uc in enumerate(USE_CASES[:6], 1):
        pdf.h3(f"CU-{i:02d} : {uc['name']}")
        pdf.bullet(f"Acteur : {uc['actor']}")
        pdf.bullet(f"Preconditions : {uc['pre']}")
        pdf.bullet(f"Declencheur : {uc['trigger']}")
        pdf.bullet(f"Scenario nominal : {uc['nominal']}")
        pdf.bullet(f"Scenario alternatif : {uc['alt']}")
        pdf.bullet(f"Postconditions : {uc['post']}")
        pdf.ln(1)


def ch7_bf_suite(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "7.10 Suite cas d'utilisation", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    for i, uc in enumerate(USE_CASES[6:], 7):
        pdf.h3(f"CU-{i:02d} : {uc['name']}")
        pdf.bullet(f"Acteur : {uc['actor']}")
        pdf.bullet(f"Preconditions : {uc['pre']}")
        pdf.bullet(f"Scenario nominal : {uc['nominal']}")
        pdf.bullet(f"Postconditions : {uc['post']}")
        pdf.ln(1)
    pdf.h2("7.11 Matrice acteurs x fonctionnalites")
    pdf.table(
        ["Fonctionnalite", "ADM", "MGR", "OPR", "DRV", "CLT"],
        [
            ["Gestion utilisateurs", "X", "", "", "", ""],
            ["Dashboard KPI", "", "X", "X", "X", "X"],
            ["Commandes CRUD", "", "", "X", "", "R"],
            ["Taches CRUD", "", "X", "R", "R", ""],
            ["IA predictions", "", "X", "P", "", ""],
            ["Automation", "", "X", "X", "", ""],
            ["Suivi livraison SSE", "", "", "", "", "X"],
            ["Chatbot Copilot", "X", "X", "X", "X", "X"],
        ],
        [55, 15, 15, 15, 15, 15],
    )
    pdf.p("Legende : X = acces complet, R = lecture, P = preview limite")


def ch8_bnf(pdf):
    pdf.h1(8, "BESOINS NON FONCTIONNELS")
    pdf.h2("8.1 Performance")
    pdf.req("BNF-001", "Temps reponse API REST < 500ms pour 95% requetes metier (hors IA)", "Must")
    pdf.req("BNF-002", "Prediction IA < 3 secondes timeout configurable", "Must")
    pdf.req("BNF-003", "Support 100 utilisateurs concurrents minimum", "Must")
    pdf.req("BNF-004", "Chargement initial frontend < 3 secondes", "Should")
    pdf.h2("8.2 Disponibilite et fiabilite")
    pdf.req("BNF-010", "Disponibilite cible 99% heures ouvrables", "Should")
    pdf.req("BNF-011", "Fallback rule-based si microservice IA down", "Must")
    pdf.req("BNF-012", "Migrations Flyway versionnees sans perte donnees", "Must")
    pdf.h2("8.3 Securite")
    pdf.req("BNF-020", "Mots de passe hashes BCrypt", "Must")
    pdf.req("BNF-021", "JWT expiration configurable (defaut 24h)", "Must")
    pdf.req("BNF-022", "RBAC strict sur tous endpoints", "Must")
    pdf.req("BNF-023", "CORS restreint aux origines autorisees", "Must")
    pdf.req("BNF-024", "Pas de secrets en clair dans le code source", "Must")
    pdf.h2("8.4 Utilisabilite")
    pdf.req("BNF-030", "Interface responsive desktop/tablette", "Must")
    pdf.req("BNF-031", "Dashboards avec vues cartes et liste", "Must")
    pdf.req("BNF-032", "Notifications toast et alertes visuelles", "Must")
    pdf.req("BNF-033", "Navigation sidebar par role", "Must")
    pdf.h2("8.5 Maintenabilite")
    pdf.req("BNF-040", "Architecture en couches backend (controller/service/repository)", "Must")
    pdf.req("BNF-041", "Frontend Angular standalone components", "Must")
    pdf.req("BNF-042", "Documentation OpenAPI Swagger backend", "Must")
    pdf.req("BNF-043", "Tests unitaires Python (pytest) et Java (JUnit)", "Must")
    pdf.h2("8.6 Interoperabilite")
    pdf.req("BNF-050", "API REST JSON UTF-8", "Must")
    pdf.req("BNF-051", "Communication backend-IA via HTTP/WebClient", "Must")
    pdf.req("BNF-052", "SSE pour streaming suivi client", "Must")
    pdf.h2("8.7 Scalabilite et deploiement")
    pdf.req("BNF-060", "Conteneurisation Docker chaque service", "Must")
    pdf.req("BNF-061", "Orchestration Docker Compose dev/preprod", "Must")
    pdf.req("BNF-062", "CI/CD GitHub Actions build + test", "Must")
    pdf.req("BNF-063", "Reverse proxy Nginx production", "Should")
    pdf.h2("8.8 Qualite des donnees IA")
    pdf.req("BNF-070", "Dataset documente (synthetique dev, reel prod)", "Must")
    pdf.req("BNF-071", "Metriques ML tracees (F1, MAE, R2) dans model_metadata.json", "Must")
    pdf.req("BNF-072", "Endpoints ML retournent 503 si modele absent", "Must")


def ch9_contraintes(pdf):
    pdf.h1(9, "CONTRAINTES, HYPOTHESES ET PERIMETRE")
    pdf.h2("9.1 Contraintes")
    pdf.bullet("Budget projet PFE : ressources humaines limitees (1-2 developpeurs)")
    pdf.bullet("Delai : livraison MVP en 4 mois, version complete en 6 mois")
    pdf.bullet("Stack imposee : Java/Spring, Angular, Python, PostgreSQL")
    pdf.bullet("Hebergement initial : on-premise ou cloud basique (VPS)")
    pdf.bullet("Donnees ML initiales synthetiques faute d'historique exploitable")
    pdf.h2("9.2 Hypotheses")
    pdf.bullet("Les chauffeurs disposent d'un smartphone avec connexion 4G")
    pdf.bullet("PostgreSQL disponible et administre")
    pdf.bullet("Le microservice IA est deploye sur le meme reseau que le backend")
    pdf.bullet("Les utilisateurs sont formes aux roles respectifs")
    pdf.h2("9.3 Perimetre IN")
    pdf.bullet("5 roles et leurs interfaces dediees")
    pdf.bullet("Workflow commande-tache-livraison complet")
    pdf.bullet("Module IA complet avec fallbacks")
    pdf.bullet("Automation express et alertes chauffeur")
    pdf.bullet("Chatbot Copilot")
    pdf.bullet("Documentation technique et cahier de tests")
    pdf.h2("9.4 Perimetre OUT")
    pdf.bullet("Application mobile native iOS/Android (web responsive suffit MVP)")
    pdf.bullet("Integration ERP/SAP")
    pdf.bullet("Paiement en ligne")
    pdf.bullet("Multi-tenant SaaS")
    pdf.bullet("Mode offline chauffeur")


def ch10_methodo(pdf):
    pdf.h1(10, "METHODOLOGIE DE REALISATION ADOPTEE")
    pdf.h2("10.1 Approche globale : Agile Scrum adapte")
    pdf.p(
        "La MOA retient une approche Agile Scrum adaptee au contexte PFE : sprints de 2 semaines, "
        "backlog priorise par valeur metier, demos fin de sprint au Product Owner, retrospectives "
        "pour amelioration continue. Un cycle en V est applique pour les specifications critiques "
        "(securite, workflow, donnees) via revues formelles."
    )
    pdf.h2("10.2 Roles projet")
    pdf.table(
        ["Role Scrum", "Responsable", "Mission"],
        [
            ["Product Owner", "MOA metier", "Prioriser backlog, valider incréments"],
            ["Scrum Master", "Chef de projet MOE", "Faciliter, lever impediments"],
            ["Dev Team", "Developpeurs", "Concevoir, coder, tester"],
            ["Architecte", "MOE technique", "Coherence technique, revues"],
            ["QA", "Testeur", "Plans de test, recette"],
        ],
        [40, 45, 95],
    )
    pdf.h2("10.3 Phases du projet")
    pdf.table(
        ["Phase", "Duree", "Livrables"],
        [
            ["Phase 0 - Cadrage", "2 sem", "Cahier des charges, backlog initial"],
            ["Phase 1 - Conception", "3 sem", "UML, maquettes, architecture, MCD"],
            ["Phase 2 - Socle technique", "2 sem", "Auth, users, BDD, CI"],
            ["Phase 3 - Metier core", "4 sem", "Commandes, taches, roles"],
            ["Phase 4 - IA & automation", "3 sem", "Microservice ML, chaine express"],
            ["Phase 5 - Frontend avance", "3 sem", "Dashboards, UX pro, chatbot"],
            ["Phase 6 - Tests & deploiement", "2 sem", "Recette, Docker, doc"],
        ],
        [55, 20, 105],
    )
    pdf.h2("10.4 Pratiques techniques")
    pdf.bullet("Git flow : branche main protegee, feature branches, PR review")
    pdf.bullet("Definition of Done : code review + tests passants + doc API a jour")
    pdf.bullet("UML : cas utilisation, classes, sequences pour flux critiques")
    pdf.bullet("TDD partiel sur services metier critiques")
    pdf.bullet("Revue architecture avant sprint 3")
    pdf.h2("10.5 Outils de pilotage")
    pdf.bullet("GitHub : versioning, Issues, Projects, Actions CI")
    pdf.bullet("Postman : collection API SmartTask-API")
    pdf.bullet("Swagger UI : documentation interactive backend")
    pdf.bullet("Draw.io / ASCII : diagrammes architecture")


def ch11_planning(pdf):
    pdf.h1(11, "PLANNING PREVISIONNEL ET JALONS")
    pdf.h2("11.1 Jalons contractuels")
    pdf.table(
        ["Jalon", "Date cible", "Critere validation"],
        [
            ["J1 - Kick-off", "S0", "Equipe constituee, env dev pret"],
            ["J2 - Socle auth+BDD", "S4", "Login JWT 5 roles, Flyway OK"],
            ["J3 - MVP metier", "S10", "Commande->Tache->Livraison manuel"],
            ["J4 - IA operationnelle", "S14", "Predictions + fallback testes"],
            ["J5 - Beta interne", "S18", "5 utilisateurs pilotes par role"],
            ["J6 - Recette MOA", "S22", "100% Must validés"],
            ["J7 - Mise en production", "S24", "Docker Compose prod OK"],
        ],
        [45, 25, 110],
    )
    pdf.h2("11.2 Diagramme de Gantt simplifie")
    pdf.fig("Planning haut niveau (24 semaines)",
        "S1-S2   : Cadrage + Conception\n"
        "S3-S4   : Auth, Users, PostgreSQL, CI\n"
        "S5-S8   : Orders, Tasks, Operator, Manager\n"
        "S9-S10  : Driver, Client, SSE tracking\n"
        "S11-S14 : Python IA, ML training, integration\n"
        "S15-S16 : Automation express, alertes\n"
        "S17-S18 : Frontend pro, dashboards, chatbot\n"
        "S19-S20 : Tests integration, securite\n"
        "S21-S22 : Recette MOA, corrections\n"
        "S23-S24 : Docker prod, Nginx, documentation"
    )


def ch12_archi(pdf):
    pdf.h1(12, "ARCHITECTURE CIBLE DU SYSTEME")
    pdf.h2("12.1 Architecture logique")
    pdf.fig("Figure 12.1 - Couches applicatives",
        "+--------------------------------------------------+\n"
        "|  PRESENTATION : Angular 16 (5 espaces role)       |\n"
        "+--------------------------------------------------+\n"
        "|  API GATEWAY  : Spring Boot REST + JWT + CORS    |\n"
        "+--------------------------------------------------+\n"
        "|  METIER       : Services, Events, Schedulers     |\n"
        "+--------------------------------------------------+\n"
        "|  PERSISTANCE  : JPA/Hibernate + Flyway           |\n"
        "+--------------------------------------------------+\n"
        "|  IA CLIENT    : WebClient -> FastAPI :8000       |\n"
        "+--------------------------------------------------+\n"
        "|  DONNEES      : PostgreSQL 15                    |\n"
        "+--------------------------------------------------+"
    )
    pdf.h2("12.2 Architecture physique cible")
    pdf.table(
        ["Noeud", "Services", "Ports"],
        [
            ["Nginx", "Reverse proxy, SSL, static Angular", "80, 443"],
            ["App Server", "Spring Boot JAR", "9090"],
            ["AI Server", "FastAPI uvicorn", "8000"],
            ["DB Server", "PostgreSQL", "5432"],
        ],
        [40, 90, 50],
    )
    pdf.h2("12.3 Principes d'integration")
    pdf.bullet("Angular -> Spring Boot uniquement (jamais Python direct)")
    pdf.bullet("Spring Boot -> Python via SmartTaskAIClient (WebClient)")
    pdf.bullet("Python -> pas d'acces PostgreSQL (separation concerns)")
    pdf.bullet("Events Spring : OrderCreatedEvent -> AutomationEventListener")


def ch13_donnees(pdf):
    pdf.h1(13, "MODELE DE DONNEES ET REGLES METIER")
    pdf.h2("13.1 Entites principales")
    for name, fields in list(ENTITIES.items())[:6]:
        pdf.h3(name)
        rows = [(f[0], f[1], f[2]) for f in fields]
        pdf.table(["Attribut", "Type", "Contrainte"], rows, [60, 45, 75])
    pdf.h2("13.2 Entites complementaires")
    for name, fields in list(ENTITIES.items())[6:]:
        pdf.h3(name)
        rows = [(f[0], f[1], f[2]) for f in fields]
        pdf.table(["Attribut", "Type", "Contrainte"], rows, [60, 45, 75])
    pdf.h2("13.3 Regles metier critiques")
    pdf.bullet("RB-01 : Une commande READY peut generer une tache PREPARED")
    pdf.bullet("RB-02 : Transition tache ASSIGNED -> ACCEPTED par chauffeur uniquement")
    pdf.bullet("RB-03 : Un avis Review est unique par Task (OneToOne)")
    pdf.bullet("RB-04 : Automation express declenche si priorite in (HIGH, CRITICAL)")
    pdf.bullet("RB-05 : Flyway ddl-auto=validate (pas de generation auto schema prod)")
    pdf.fig("Figure 13.1 - ERD simplifie", load_diagram("06_erd.txt"))


def ch14_ui(pdf):
    pdf.h1(14, "INTERFACES UTILISATEUR ET PARCOURS")
    pdf.h2("14.1 Principes UX")
    pdf.bullet("Design professionnel SmartLogix : dashboards, cartes KPI, alertes")
    pdf.bullet("View toggle cartes/liste sur ecrans de gestion")
    pdf.bullet("Toast notifications pour feedback actions")
    pdf.bullet("Alert banners pour nouveautes IA")
    pdf.bullet("Sidebar navigation par role avec logo SL")
    pdf.h2("14.2 Ecrans par role (extrait)")
    rows = [(r[0], r[1], r[2]) for r in ANGULAR_ROUTES[:20]]
    pdf.table(["Route", "Composant", "Acces"], rows, [55, 75, 50])
    pdf.h2("14.3 Parcours critique : commande express")
    pdf.fig("Figure 14.1 - Sequence automation", load_diagram("05_sequence_automation.txt"))
    pdf.p(
        "Parcours utilisateur : Operateur cree commande HIGH -> systeme declenche automation -> "
        "Manager recoit notification tache assignee -> Chauffeur voit mission -> Client suit SSE."
    )


def ch15_api(pdf):
    pdf.h1(15, "SPECIFICATIONS DES API")
    pdf.h2("15.1 API Spring Boot (extrait)")
    rows = [(e[0], e[1][:42], e[2], e[3][:35]) for e in ENDPOINTS[:25]]
    pdf.table(["Methode", "Endpoint", "Role", "Description"], rows, [18, 62, 22, 78])
    pdf.h2("15.2 Suite endpoints Spring Boot")
    rows = [(e[0], e[1][:42], e[2], e[3][:35]) for e in ENDPOINTS[25:50]]
    pdf.table(["Methode", "Endpoint", "Role", "Description"], rows, [18, 62, 22, 78])
    pdf.h2("15.3 API Python IA")
    rows = [(e[0], e[1], e[2][:70]) for e in PYTHON_ENDPOINTS]
    pdf.table(["Methode", "Endpoint", "Description"], rows, [18, 55, 107])
    pdf.h2("15.4 Standards API")
    pdf.bullet("Format JSON, codes HTTP standards (200, 201, 400, 401, 403, 404, 503)")
    pdf.bullet("Erreurs structurees ApiErrorResponse")
    pdf.bullet("Pagination sur listes (page, size, totalElements)")
    pdf.bullet("Documentation Swagger : /swagger-ui.html")


def ch16_ia(pdf):
    pdf.h1(16, "INTELLIGENCE ARTIFICIELLE ET PRIORISATION")
    pdf.h2("16.1 Objectifs IA")
    pdf.p(
        "Le module IA doit transformer des donnees operationnelles en decisions actionnables : "
        "quelle tache prioriser, quel chauffeur assigner, quel risque de retard anticiper, "
        "quelle probabilite de reussite de livraison estimer."
    )
    pdf.h2("16.2 Modeles ML")
    pdf.table(
        ["Modele", "Algorithme", "Fichier", "Metrique cible"],
        [
            ["Retard", "Logistic Regression", "delay_model.pkl", "F1 > 0.85"],
            ["Temps livraison", "XGBoost", "delivery_time_model.pkl", "MAE < 10 min"],
            ["Reussite livraison", "Gradient Boosting", "delivery_success_model.pkl", "AUC > 0.80"],
            ["Priorite", "Rule-based scoring", "N/A", "Explicable 100%"],
            ["Chauffeur", "Rule-based scoring", "N/A", "Explicable 100%"],
        ],
        [40, 45, 55, 40],
    )
    pdf.h2("16.3 Pipeline ML")
    pdf.bullet("1. generate_dataset.py : dataset synthetique documente")
    pdf.bullet("2. train_*.py : entrainement par modele")
    pdf.bullet("3. train_all.py : pipeline complet")
    pdf.bullet("4. ModelService.load_all() au demarrage FastAPI")
    pdf.bullet("5. Fallback rule-based si .pkl absent ou erreur")
    pdf.h2("16.4 Automation chaine express")
    pdf.fig("Etapes chaine EXPRESS (7 steps)",
        "1. READ_ORDER\n2. AUTO_VERIFY\n3. CREATE_TASK\n4. AI_PRIORITIZE\n5. AI_ASSIGN_DRIVER\n"
        "6. ESTIMATE_AND_NOTIFY\n7. LOG_COMPLETE"
    )
    pdf.h2("16.5 Exigences IA non fonctionnelles")
    pdf.bullet("Latence prediction < 3s")
    pdf.bullet("Explicabilite : facteurs contributifs retournes au frontend")
    pdf.bullet("Versioning modeles via model_metadata.json")
    pdf.bullet("Health check /api/ai/health et /api/ai/model/status")


def ch17_securite(pdf):
    pdf.h1(17, "SECURITE ET CONFORMITE")
    pdf.h2("17.1 Authentification JWT")
    pdf.p(
        "Spring Security stateless avec JwtAuthenticationFilter. Token transmis header "
        "Authorization Bearer. Secret configurable via JWT_SECRET (min 256 bits prod)."
    )
    pdf.h2("17.2 Matrice autorisation (extrait)")
    pdf.table(
        ["Ressource", "ADMIN", "MANAGER", "OPERATOR", "DRIVER", "CLIENT"],
        [
            ["/api/users/**", "CRUD", "-", "-", "-", "-"],
            ["/api/manager/**", "-", "RW", "-", "-", "-"],
            ["/api/operator/**", "-", "-", "RW", "-", "-"],
            ["/api/driver/**", "-", "-", "-", "RW", "-"],
            ["/api/client/**", "-", "-", "-", "-", "RW"],
            ["/api/tasks/**", "-", "RW", "-", "-", "-"],
        ],
        [40, 22, 22, 22, 22, 22],
    )
    pdf.h2("17.3 Donnees personnelles")
    pdf.bullet("Minimisation : seules donnees necessaires collectees")
    pdf.bullet("Droit acces : profil utilisateur /api/users/me")
    pdf.bullet("Retention : a definir avec DPO (recommandation 3 ans)")
    pdf.bullet("Preuve livraison : stockage securise, acces restreint")
    pdf.h2("17.4 OWASP")
    pdf.bullet("Injection : JPA parametre, validation Jakarta Bean Validation")
    pdf.bullet("Broken Auth : JWT + BCrypt")
    pdf.bullet("XSS : Angular sanitization par defaut")
    pdf.bullet("CSRF : desactive (API stateless JWT)")


def ch18_recette(pdf):
    pdf.h1(18, "CRITERES D'ACCEPTATION ET RECETTE")
    pdf.h2("18.1 Criteres generaux")
    pdf.bullet("100% exigences Must implementees et testees")
    pdf.bullet("0 bug bloquant en recette")
    pdf.bullet("Documentation utilisateur par role livree")
    pdf.bullet("Collection Postman executable")
    pdf.h2("18.2 Scenarios recette (extrait)")
    pdf.table(
        ["ID", "Scenario", "Resultat attendu"],
        [
            ["REC-01", "Login manager@smarttask.com", "Redirect /manager/dashboard"],
            ["REC-02", "Operateur cree commande HIGH", "Automation declenchee"],
            ["REC-03", "Manager assign-recommended", "Chauffeur assigne, toast OK"],
            ["REC-04", "Chauffeur complete livraison + preuve", "Statut DELIVERED"],
            ["REC-05", "Client confirme + avis 5 etoiles", "Statut RECEIVED, review OK"],
            ["REC-06", "IA down, predict delay", "Fallback rule-based, pas 500"],
            ["REC-07", "Export analytics CSV", "Fichier telecharge"],
        ],
        [18, 65, 97],
    )
    pdf.h2("18.3 Comptes test exiges")
    pdf.table(
        ["Role", "Email", "Password"],
        [
            ["ADMIN", "admin@smarttask.com", "Admin123!"],
            ["MANAGER", "manager@smarttask.com", "Manager123!"],
            ["OPERATOR", "operator1@smarttask.com", "Operator123!"],
            ["DRIVER", "driver1@smarttask.com", "Driver123!"],
            ["CLIENT", "client1@smarttask.com", "Client123!"],
        ],
        [30, 75, 75],
    )


def ch19_livrables(pdf):
    pdf.h1(19, "LIVRABLES ATTENDUS")
    pdf.table(
        ["Livrable", "Format", "Echeance"],
        [
            ["Code source complet", "GitHub repo", "S24"],
            ["Backend Spring Boot", "JAR + Dockerfile", "S20"],
            ["Frontend Angular", "dist/ + Dockerfile", "S20"],
            ["Microservice IA", "Dockerfile existant", "S16"],
            ["Docker Compose", "docker-compose.yml", "S22"],
            ["Nginx config", "nginx.conf", "S23"],
            ["GitHub Actions CI", ".github/workflows/", "S8"],
            ["Documentation API", "Swagger + Postman", "S20"],
            ["Cahier de tests", "PDF/Markdown", "S22"],
            ["Manuel utilisateur", "PDF par role", "S24"],
            ["Rapport PFE / technique", "PDF 50 pages", "S24"],
        ],
        [55, 55, 70],
    )


def ch20_risques(pdf):
    pdf.h1(20, "GESTION DES RISQUES")
    pdf.table(
        ["Risque", "Prob.", "Impact", "Mitigation"],
        [
            ["Indisponibilite IA", "M", "M", "Fallback rule-based, health checks"],
            ["Retard planning PFE", "H", "H", "MVP scope, priorisation Must"],
            ["Qualite dataset ML", "H", "M", "Dataset synthetique documente, retrain"],
            ["Performance PostgreSQL", "L", "M", "Index V6 migration, pagination"],
            ["Fuite secrets Git", "M", "H", ".gitignore, variables env, review"],
            ["Complexite Angular", "M", "M", "Standalone components, lazy loading"],
            ["Scope creep", "H", "H", "Perimetre OUT formalise, change control"],
        ],
        [45, 18, 18, 99],
    )


def ch_extra_personas(pdf):
    pdf.h1(22, "PERSONAS METIER ET SCENARIOS UTILISATEUR")
    pdf.h2("22.1 Persona : Karim - Manager logistique")
    pdf.p(
        "Karim, 38 ans, responsable de 12 chauffeurs et 4 operateurs. Il arrive a 7h30, "
        "consulte les commandes urgentes et assigne les missions. Il perd 2h/jour sur Excel "
        "et WhatsApp. Il veut un dashboard unique, des alertes retard automatiques et "
        "une recommandation IA fiable pour l'assignation."
    )
    pdf.h2("22.2 Persona : Sami - Operateur")
    pdf.p(
        "Sami, 26 ans, traite 40-60 appels/jour. Il saisit les commandes, verifie les "
        "coordonnees client et prepare les colis. Il a besoin d'un formulaire rapide, "
        "d'une preview IA reussite livraison avant validation, et d'un suivi clair des "
        "commandes en attente."
    )
    pdf.h2("22.3 Persona : Mohamed - Chauffeur")
    pdf.p(
        "Mohamed, 32 ans, effectue 15-20 livraisons/jour en zone Tunis. Il utilise son "
        "smartphone pour naviguer. Il souhaite voir ses missions triees par priorite, "
        "un itineraire optimise, des alertes si risque retard, et un upload simple "
        "de preuve livraison."
    )
    pdf.h2("22.4 Persona : Ahmed - Client")
    pdf.p(
        "Ahmed, 45 ans, commande des pieces auto et medicaments. Il exige transparence : "
        "ou est mon colis, quand arrivera-t-il ? Il veut un portail self-service, "
        "notifications temps reel et possibilite de confirmer reception et noter le service."
    )
    pdf.h2("22.5 User stories prioritaires (Product Backlog)")
    stories = [
        ("US-01", "Manager", "Voir KPIs jour en 1 ecran", "Must", "5"),
        ("US-02", "Operateur", "Creer commande en < 2 min", "Must", "8"),
        ("US-03", "Manager", "Assigner chauffeur recommande IA", "Must", "13"),
        ("US-04", "Chauffeur", "Accepter et demarrer mission mobile", "Must", "8"),
        ("US-05", "Client", "Suivre livraison temps reel", "Must", "13"),
        ("US-06", "Manager", "Predire risque retard tache", "Must", "8"),
        ("US-07", "Operateur", "Preview score reussite livraison", "Must", "5"),
        ("US-08", "Systeme", "Automation express HIGH/CRITICAL", "Must", "13"),
        ("US-09", "Chauffeur", "Itineraire optimise multi-stops", "Should", "8"),
        ("US-10", "Tous", "Chatbot Copilot contextuel", "Should", "5"),
        ("US-11", "Manager", "Export analytics CSV", "Should", "3"),
        ("US-12", "Admin", "Gerer utilisateurs et roles", "Must", "5"),
    ]
    pdf.table(["ID", "Role", "Story", "Priorite", "Points"], stories, [15, 22, 75, 22, 18])


def ch_extra_workflows(pdf):
    pdf.h1(23, "WORKFLOWS METIER DETAILLES")
    pdf.h2("23.1 Cycle de vie OrderStatus")
    pdf.table(
        ["Statut", "Description", "Acteur declencheur", "Statut suivant"],
        [
            ["PENDING", "Commande saisie, non verifiee", "OPERATOR create", "VERIFIED"],
            ["VERIFIED", "Informations validees", "OPERATOR verify", "PREPARING/READY"],
            ["PREPARING", "En cours preparation", "OPERATOR", "READY"],
            ["READY", "Pret pour dispatch", "OPERATOR prepare", "IN_DELIVERY"],
            ["IN_DELIVERY", "En cours livraison", "DRIVER start", "DELIVERED"],
            ["DELIVERED", "Livre chez client", "DRIVER complete", "RECEIVED"],
            ["RECEIVED", "Confirme par client", "CLIENT confirm", "Final"],
            ["CANCELLED", "Annulee", "MANAGER/OPERATOR", "Final"],
        ],
        [28, 50, 45, 57],
    )
    pdf.h2("23.2 Cycle de vie TaskStatus")
    pdf.table(
        ["Statut", "Description", "Transition"],
        [
            ["PREPARED", "Tache creee, non assignee", "-> ASSIGNED"],
            ["ASSIGNED", "Chauffeur designe", "-> ACCEPTED (driver)"],
            ["ACCEPTED", "Chauffeur a accepte", "-> IN_DELIVERY"],
            ["IN_DELIVERY", "Livraison en cours", "-> DELIVERED"],
            ["DELIVERED", "Livraison effectuee", "-> COMPLETED"],
            ["COMPLETED", "Cycle termine", "Final"],
            ["CANCELLED", "Annulee", "Final"],
        ],
        [35, 75, 70],
    )
    pdf.h2("23.3 Diagramme cas d'utilisation global")
    pdf.fig("Figure 23.1 - Cas d'utilisation", load_diagram("02_use_case_global.txt"))
    pdf.h2("23.4 Diagramme de classes metier")
    pdf.fig("Figure 23.2 - Classes", load_diagram("03_class_diagram.txt"))
    pdf.h2("23.5 Sequence authentification")
    pdf.fig("Figure 23.3 - Auth JWT", load_diagram("04_sequence_auth.txt"))


def ch_extra_api_complete(pdf):
    pdf.h1(24, "ANNEXE A - CATALOGUE COMPLET DES API")
    pdf.h2("24.1 Endpoints Spring Boot (suite 50-75)")
    rows = [(e[0], e[1][:44], e[2], e[3][:32]) for e in ENDPOINTS[50:75]]
    pdf.table(["Methode", "Endpoint", "Role", "Description"], rows, [18, 64, 22, 76])
    pdf.h2("24.2 Endpoints Spring Boot (suite 75-100)")
    rows = [(e[0], e[1][:44], e[2], e[3][:32]) for e in ENDPOINTS[75:]]
    pdf.table(["Methode", "Endpoint", "Role", "Description"], rows, [18, 64, 22, 76])
    pdf.h2("24.3 Routes Angular completes")
    rows = [(r[0], r[1][:40], r[2]) for r in ANGULAR_ROUTES]
    pdf.table(["Route", "Composant", "Acces"], rows, [55, 80, 45])


def ch_extra_devops(pdf):
    pdf.h1(25, "EXIGENCES DEVOPS ET DEPLOIEMENT")
    pdf.h2("25.1 Conteneurisation")
    pdf.req("DEV-001", "Dockerfile multi-stage pour backend Spring Boot (Java 17)", "Must")
    pdf.req("DEV-002", "Dockerfile multi-stage pour frontend Angular (nginx alpine)", "Must")
    pdf.req("DEV-003", "Dockerfile Python existant smarttask-ai/Dockerfile valide", "Must")
    pdf.req("DEV-004", "docker-compose.yml orchestrant postgres, backend, ai, frontend, nginx", "Must")
    pdf.h2("25.2 Variables d'environnement")
    pdf.table(
        ["Variable", "Service", "Description", "Exemple"],
        [
            ["DB_URL", "Backend", "JDBC PostgreSQL", "jdbc:postgresql://db:5432/smarttask_db"],
            ["DB_USERNAME", "Backend", "User BDD", "postgres"],
            ["DB_PASSWORD", "Backend", "Mot de passe BDD", "[secret]"],
            ["JWT_SECRET", "Backend", "Cle JWT 256+ bits", "[secret]"],
            ["AI_SERVICE_URL", "Backend", "URL microservice IA", "http://ai:8000"],
            ["CORS_ORIGINS", "Backend", "Origines autorisees", "http://localhost"],
            ["SPRING_BOOT_URL", "Python", "URL backend pour CORS", "http://backend:9090"],
            ["MODEL_PATH", "Python", "Repertoire modeles ML", "./app/models"],
        ],
        [35, 22, 58, 65],
    )
    pdf.h2("25.3 Nginx reverse proxy")
    pdf.bullet("Route / -> frontend Angular static")
    pdf.bullet("Route /api/ -> proxy backend :9090")
    pdf.bullet("Route /swagger-ui/ -> proxy backend (dev/preprod)")
    pdf.bullet("Compression gzip, cache assets statiques")
    pdf.bullet("Headers securite : X-Frame-Options, X-Content-Type-Options")
    pdf.h2("25.4 GitHub Actions CI")
    pdf.bullet("Workflow backend : ./gradlew test sur push/PR")
    pdf.bullet("Workflow frontend : npm ci && npm run build")
    pdf.bullet("Workflow Python : pip install && pytest")
    pdf.bullet("Declenchement sur branches main et develop")
    pdf.h2("25.5 Environnements")
    pdf.table(
        ["Env", "Usage", "BDD", "IA"],
        [
            ["dev", "Developpement local", "PostgreSQL local", "uvicorn reload"],
            ["docker", "Integration conteneurs", "postgres service", "ai service"],
            ["preprod", "Recette MOA", "PostgreSQL dedie", "Modeles ML entraines"],
            ["prod", "Production", "PostgreSQL HA", "Modeles ML + monitoring"],
        ],
        [25, 55, 50, 50],
    )


def ch_extra_qualite(pdf):
    pdf.h1(26, "QUALITE, TESTS ET COMMUNICATION")
    pdf.h2("26.1 Strategie de tests")
    pdf.table(
        ["Niveau", "Outil", "Couverture cible", "Responsable"],
        [
            ["Unitaire Java", "JUnit 5 + Spring Test", "Services metier > 60%", "Dev backend"],
            ["Unitaire Python", "pytest", "API + services > 70%", "Dev IA"],
            ["Unitaire Angular", "Jasmine/Karma", "Services core", "Dev frontend"],
            ["Integration", "Postman/Newman", "Endpoints critiques 100%", "QA"],
            ["E2E manuel", "Scenarios recette", "Parcours Must 100%", "MOA + QA"],
            ["Securite", "OWASP checklist", "Top 10 verifie", "Architecte"],
        ],
        [35, 45, 50, 50],
    )
    pdf.h2("26.2 Plan de communication projet")
    pdf.bullet("Reunion kick-off : presentation cahier des charges a l'equipe")
    pdf.bullet("Daily standup 15 min (equipe dev)")
    pdf.bullet("Demo sprint : fin de chaque sprint 2 semaines")
    pdf.bullet("Comite pilotage : mensuel MOA/MOE")
    pdf.bullet("Rapport avancement : hebdomadaire email sponsor")
    pdf.h2("26.3 Plan de formation utilisateurs")
    pdf.table(
        ["Cible", "Duree", "Contenu", "Support"],
        [
            ["Operateurs", "2h", "Commandes, verification, incidents", "Guide PDF + video"],
            ["Managers", "3h", "Dashboard, IA, automation, analytics", "Atelier pratique"],
            ["Chauffeurs", "1h", "Missions, GPS, preuve, route IA", "Fiche memo mobile"],
            ["Clients", "N/A", "Portail self-service intuitif", "FAQ en ligne"],
        ],
        [35, 18, 75, 52],
    )
    pdf.h2("26.4 Gestion des changements")
    pdf.p(
        "Toute demande hors perimetre Must doit faire l'objet d'une fiche de changement "
        "evaluee par le Product Owner (impact planning, cout, risque). Les exigences Should "
        "peuvent etre reportees en phase 2 sans remettre en cause la recette MVP."
    )


def ch_extra_kpi(pdf):
    pdf.h1(27, "INDICATEURS DE PERFORMANCE ET BUDGET")
    pdf.h2("27.1 KPIs de succes projet")
    pdf.table(
        ["KPI", "Baseline AS-IS", "Cible TO-BE", "Mesure"],
        [
            ["Taux retard livraison", "22%", "< 12%", "Analytics mensuel"],
            ["Echec 1er passage", "15%", "< 10%", "Delivery Success AI + reviews"],
            ["Temps assignation", "15 min/cmd", "< 2 min", "Automation logs"],
            ["NPS client", "32", "> 50", "Enquete trimestrielle"],
            ["Productivite manager", "2h/j admin", "< 30 min/j", "Time tracking"],
            ["Disponibilite plateforme", "N/A", "> 99%", "Monitoring"],
        ],
        [45, 35, 35, 65],
    )
    pdf.h2("27.2 Budget previsionnel (estimation)")
    pdf.table(
        ["Poste", "Estimation", "Commentaire"],
        [
            ["Developpement PFE (6 mois)", "Ressource humaine", "1-2 etudiants + encadrant"],
            ["Infrastructure VPS/Cloud", "50-100 EUR/mois", "4 conteneurs + PostgreSQL"],
            ["Nom de domaine + SSL", "30 EUR/an", "Let's Encrypt gratuit"],
            ["Outils (GitHub, Postman)", "Gratuit", "Plans community"],
            ["Formation utilisateurs", "Interne MOA", "2 jours ateliers"],
            ["Maintenance an 1", "A definir", "20% effort dev initial"],
        ],
        [55, 45, 80],
    )
    pdf.h2("27.3 Indicateurs de suivi projet (EVM simplifie)")
    pdf.p(
        "Le chef de projet suivra mensuellement : pourcentage exigences Must implementees, "
        "velocity moyenne (story points/sprint), nombre bugs ouverts vs fermes, couverture "
        "tests, et respect jalons J1-J7. Un tableau de bord GitHub Projects sera partage "
        "avec le sponsor."
    )


def ch_extra_incidents(pdf):
    pdf.h1(28, "GESTION INCIDENTS ET NOTIFICATIONS")
    pdf.h2("28.1 Types d'incidents")
    pdf.table(
        ["Type", "Description", "Acteurs signaleurs"],
        [
            ["DELIVERY_FAILED", "Echec livraison", "DRIVER, CLIENT"],
            ["DAMAGED_PRODUCT", "Produit endommage", "CLIENT, DRIVER"],
            ["WRONG_ADDRESS", "Adresse incorrecte", "DRIVER, OPERATOR"],
            ["CLIENT_ABSENT", "Client absent", "DRIVER"],
            ["VEHICLE_ISSUE", "Probleme vehicule", "DRIVER"],
            ["OTHER", "Autre", "Tous"],
        ],
        [40, 70, 70],
    )
    pdf.h2("28.2 Workflow incident")
    pdf.p(
        "Cycle OPEN -> IN_PROGRESS -> RESOLVED -> CLOSED. Le manager traite via "
        "/api/manager/incidents/{id}. Chaque incident est lie a une commande et/ou tache. "
        "Notification automatique au manager lors de creation."
    )
    pdf.h2("28.3 Systeme de notifications")
    pdf.bullet("NotificationType : TASK_ASSIGNED, DELAY_RISK, DELIVERY_UPDATE, INCIDENT, SYSTEM")
    pdf.bullet("Notifications persistees en base avec readFlag")
    pdf.bullet("Affichage dashboard par role (manager, client)")
    pdf.bullet("Alertes proactives chauffeur via DriverProactiveAlertScheduler")
    pdf.h2("28.4 Migrations Flyway")
    pdf.table(
        ["Version", "Fichier", "Contenu"],
        [
            ["V1", "create_users_table", "Users, roles, auth"],
            ["V2", "create_tasks_and_logistics", "Tasks, drivers, history"],
            ["V3", "orders_incidents_reviews", "Orders, incidents, reviews"],
            ["V4", "add_order_received_status", "Statut RECEIVED"],
            ["V5", "seed_client_confirm", "Donnees seed confirmation"],
            ["V6", "performance_indexes", "Index performance"],
            ["V7", "proof_of_delivery", "Preuve livraison image"],
            ["V8", "chat_messages", "Historique chatbot"],
            ["V9", "automation_logs", "Journal automation IA"],
            ["V10", "product_types", "Catalogue types produit"],
        ],
        [18, 55, 107],
    )


def ch_extra_synthese(pdf):
    pdf.h1(29, "SYNTHESE EXECUTIVE POUR LA DIRECTION")
    pdf.h2("29.1 Resume en une page")
    pdf.p(
        "SmartLogix Prioritizer with IA repond a une problematique operationnelle critique : "
        "fragmentation des outils, priorisation subjective, retards frequents et absence de "
        "visibilite client. La solution propose une plateforme web integrée Angular + Spring Boot "
        "+ Python IA + PostgreSQL, avec automation chaine express, predictions ML et dashboards "
        "professionnels multi-role."
    )
    pdf.p(
        "Investissement estime : 6 mois de developpement, infrastructure cloud modeste, "
        "retour attendu via reduction retards (-25%), amelioration NPS et productivite managers. "
        "Le present cahier des charges constitue le contrat fonctionnel entre la MOA et l'equipe "
        "de realisation."
    )
    pdf.h2("29.2 Decision attendue")
    pdf.bullet("Valider le perimetre Must et les jalons J1-J7")
    pdf.bullet("Nommer le Product Owner MOA et le chef de projet MOE")
    pdf.bullet("Allouer les ressources infrastructure (PostgreSQL, VPS/Docker)")
    pdf.bullet("Autoriser le demarrage Sprint 1")
    pdf.h2("29.3 Contacts projet")
    pdf.table(
        ["Role", "Organisation", "Contact"],
        [
            ["Sponsor", "Direction Operations", "[A completer]"],
            ["Product Owner", "Service Logistique", "[A completer]"],
            ["Chef de projet MOE", "Equipe developpement", "[A completer]"],
            ["Architecte SI", "Direction SI", "[A completer]"],
            ["Encadrant PFE", "Etablissement", "[A completer]"],
        ],
        [40, 55, 85],
    )


def ch21_glossaire(pdf):
    pdf.h1(21, "GLOSSAIRE ET ANNEXES")
    pdf.h2("21.1 Glossaire")
    glossary = [
        ("SmartLogix", "Nom commercial de la plateforme"),
        ("SmartTask", "Nom technique du code source"),
        ("Last-mile", "Dernier kilometre de livraison"),
        ("JWT", "JSON Web Token pour authentification"),
        ("SSE", "Server-Sent Events pour streaming temps reel"),
        ("TSP", "Travelling Salesman Problem - optimisation route"),
        ("Flyway", "Outil migrations base de donnees"),
        ("RBAC", "Role-Based Access Control"),
        ("MOA", "Maitrise d'ouvrage (commanditaire)"),
        ("MOE", "Maitrise d'oeuvre (realisation)"),
        ("MVP", "Minimum Viable Product"),
        ("CRUD", "Create Read Update Delete"),
    ]
    pdf.table(["Terme", "Definition"], glossary, [45, 135])
    pdf.h2("21.2 Annexes")
    pdf.bullet("Annexe A : Liste complete endpoints (cf. rapport_data.py)")
    pdf.bullet("Annexe B : Migrations Flyway V1 a V10")
    pdf.bullet("Annexe C : Diagrammes UML (dossier docs/diagrammes/)")
    pdf.bullet("Annexe D : Collection Postman SmartTask-API")
    pdf.h2("21.3 Approbation finale")
    pdf.p(
        "La signature des parties mentionnees en page de validation vaut acceptation du "
        "present cahier des charges et autorise le demarrage de la phase de realisation "
        "de SmartLogix Prioritizer with IA."
    )


def build():
    pdf = CahierCharges()
    cover(pdf)
    approval_page(pdf)
    toc_page(pdf)
    ch1_intro(pdf)
    ch2_contexte(pdf)
    ch3_problematique(pdf)
    ch4_solution(pdf)
    ch5_existant(pdf)
    ch6_critique(pdf)
    ch7_bf(pdf)
    ch7_bf_suite(pdf)
    ch8_bnf(pdf)
    ch9_contraintes(pdf)
    ch10_methodo(pdf)
    ch11_planning(pdf)
    ch12_archi(pdf)
    ch13_donnees(pdf)
    ch14_ui(pdf)
    ch15_api(pdf)
    ch16_ia(pdf)
    ch17_securite(pdf)
    ch18_recette(pdf)
    ch19_livrables(pdf)
    ch20_risques(pdf)
    ch_extra_personas(pdf)
    ch_extra_workflows(pdf)
    ch_extra_api_complete(pdf)
    ch_extra_devops(pdf)
    ch_extra_qualite(pdf)
    ch_extra_kpi(pdf)
    ch_extra_incidents(pdf)
    ch_extra_synthese(pdf)
    ch21_glossaire(pdf)
    pdf.output(OUT_PDF)
    print(f"PDF genere : {OUT_PDF} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build()
