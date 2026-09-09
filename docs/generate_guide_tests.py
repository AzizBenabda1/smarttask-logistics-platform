# -*- coding: utf-8 -*-
"""
Generateur Guide de Tests SmartLogix - Tous roles, toutes fonctionnalites
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from rapport_data import PROJECT, ENDPOINTS, PYTHON_ENDPOINTS, ANGULAR_ROUTES

OUT_PDF = os.path.join(os.path.dirname(__file__), "Guide_Tests_SmartLogix.pdf")
DOC_DATE = date.today().strftime("%d/%m/%Y")

ACCOUNTS = [
    ("ADMIN", "admin@smarttask.com", "Admin123!", "/admin/dashboard"),
    ("MANAGER", "manager@smarttask.com", "Manager123!", "/manager/dashboard"),
    ("OPERATOR", "operator1@smarttask.com", "Operator123!", "/operator/dashboard"),
    ("DRIVER", "driver1@smarttask.com", "Driver123!", "/driver/dashboard"),
    ("DRIVER 2", "driver2@smarttask.com", "Driver123!", "/driver/dashboard"),
    ("CLIENT", "client1@smarttask.com", "Client123!", "/client/dashboard"),
    ("CLIENT 2", "client2@smarttask.com", "Client123!", "/client/dashboard"),
]


class GuideTests(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(15, 15, 15)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"SmartLogix - Guide de Tests | Page {self.page_no()}", align="C")

    def h1(self, num, title):
        self.add_page()
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(15, 60, 110)
        self.cell(0, 10, f"{num}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(15, 60, 110)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(4)

    def h2(self, title):
        if self.get_y() > 258:
            self.add_page()
        self.ln(1)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 30, 30)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def h3(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def p(self, text):
        if self.get_y() > 265:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(35, 35, 35)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def step(self, n, text):
        if self.get_y() > 265:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9.5)
        self.multi_cell(0, 5, f"  Etape {n}. {text}")

    def ok(self, text):
        self.bullet(f"[OK attendu] {text}")

    def ko(self, text):
        self.bullet(f"[ECHEC si] {text}")

    def bullet(self, text):
        if self.get_y() > 265:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9.5)
        self.multi_cell(0, 5, f"  - {text}")

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
            self.cell(widths[i], 6, str(h)[:50], border=1, fill=True)
        self.ln()
        self.set_font("Helvetica", "", 7.5)
        fill = False
        for row in rows:
            if self.get_y() > 275:
                self.add_page()
            self.set_fill_color(240, 244, 248) if fill else self.set_fill_color(255, 255, 255)
            self.set_text_color(30, 30, 30)
            for i, cell in enumerate(row):
                self.cell(widths[i], 5.5, str(cell)[:60], border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(2)

    def test_case(self, tid, title, role, steps, expected, alt=None):
        self.h3(f"{tid} - {title}")
        self.p(f"Role : {role}")
        for i, s in enumerate(steps, 1):
            self.step(i, s)
        self.ok(expected)
        if alt:
            self.ko(alt)
        self.ln(1)


def cover(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(15, 60, 110)
    pdf.ln(30)
    pdf.cell(0, 12, "GUIDE DE TESTS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "SmartLogix Prioritizer with IA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "Scenarios complets - Tous utilisateurs - Toutes fonctionnalites", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(20)
    for k, v in [
        ("Version", "1.0"),
        ("Date", DOC_DATE),
        ("Application", "SmartLogix / SmartTask"),
        ("Frontend", "http://localhost:4200"),
        ("Backend API", "http://localhost:9090"),
        ("Service IA", "http://localhost:8000"),
        ("Swagger", "http://localhost:9090/swagger-ui.html"),
    ]:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, f"{k} : {v}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def ch_preambule(pdf):
    pdf.h1("1", "INTRODUCTION ET PREREQUIS")
    pdf.h2("1.1 Objectif du guide")
    pdf.p(
        "Ce guide permet de tester integralement SmartLogix : authentification, 5 roles, "
        "workflows commande-livraison, intelligence artificielle, automation, chatbot, "
        "incidents et securite. Chaque scenario indique les etapes UI, le resultat attendu "
        "et les cas d'echec."
    )
    pdf.h2("1.2 Demarrage des services")
    pdf.h3("Terminal 1 - PostgreSQL")
    pdf.p("PostgreSQL actif sur port 5432, base smarttask_db creee.")
    pdf.h3("Terminal 2 - Backend Spring Boot")
    pdf.p("cd \"Backend Smarttask/SmartTask\" puis .\\gradlew bootRun")
    pdf.p("Attendre : SmartTask demarre sur port 9090, Flyway migrations OK, DataInitializer seed.")
    pdf.h3("Terminal 3 - Microservice IA (optionnel mais recommande)")
    pdf.p("cd smarttask-ai && .venv\\Scripts\\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000")
    pdf.p("Entrainement modeles : python -m app.ml.train_all")
    pdf.h3("Terminal 4 - Frontend Angular")
    pdf.p("cd smarttask-frontend && npm start")
    pdf.p("Ouvrir navigateur : http://localhost:4200")
    pdf.h2("1.3 Comptes de test")
    pdf.table(["Role", "Email", "Mot de passe", "Dashboard"], ACCOUNTS, [28, 58, 35, 59])
    pdf.h2("1.4 Matrice de couverture")
    pdf.table(
        ["Module", "ADMIN", "MGR", "OPR", "DRV", "CLT"],
        [
            ["Auth / Profil", "X", "X", "X", "X", "X"],
            ["Gestion users", "X", "", "", "", ""],
            ["Commandes", "", "R", "X", "", "R"],
            ["Taches / Missions", "", "X", "R", "X", ""],
            ["IA / ML", "", "X", "P", "R", ""],
            ["Automation", "", "X", "X", "", ""],
            ["Suivi livraison", "", "R", "R", "X", "X"],
            ["Incidents", "", "X", "X", "X", "X"],
            ["Avis / Reviews", "", "", "", "", "X"],
            ["Chatbot Copilot", "X", "X", "X", "X", "X"],
            ["Analytics", "", "X", "", "R", ""],
        ],
        [45, 18, 18, 18, 18, 18],
    )


def ch_scenario_global(pdf):
    pdf.h1("2", "SCENARIO GLOBAL E2E (PARCOURS COMPLET)")
    pdf.p(
        "Ce scenario enchaine tous les roles pour valider le cycle de vie complet "
        "d'une commande CRITICAL de la creation a l'avis client. Duree estimee : 45-60 min."
    )
    pdf.h2("Phase A - Operateur : creer commande urgente")
    pdf.test_case(
        "E2E-01", "Creation commande CRITICAL",
        "OPERATOR (operator1@smarttask.com)",
        [
            "Login -> redirect /operator/dashboard",
            "Menu Commandes -> Nouvelle commande (/operator/orders/create)",
            "Selectionner client : Ahmed (client1@smarttask.com)",
            "Type produit : choisir un type catalogue ou Autre",
            "Remplir : quantite 2, montant 200, adresse livraison Tunis",
            "Priorite : CRITICAL",
            "Cliquer 'Analyser reussite livraison' (Delivery Success AI)",
            "Verifier affichage score % et facteurs",
            "Cliquer 'Enregistrer' -> toast succes",
        ],
        "Commande creee statut PENDING. Si automation active : chaine express declenchee.",
        "Formulaire invalide ou erreur 500"
    )
    pdf.h2("Phase B - Operateur : verification et preparation")
    pdf.test_case(
        "E2E-02", "Verifier et preparer commande",
        "OPERATOR",
        [
            "Aller /operator/orders/pending",
            "Ouvrir la commande creee",
            "Cliquer Verifier -> statut VERIFIED",
            "Si pas automation : /operator/tasks -> Preparer commande READY",
        ],
        "Commande READY, tache PREPARED creee (si workflow manuel)",
    )
    pdf.h2("Phase C - Manager : assignation IA")
    pdf.test_case(
        "E2E-03", "Assigner chauffeur via IA",
        "MANAGER (manager@smarttask.com)",
        [
            "Login -> /manager/dashboard : verifier KPIs",
            "Aller /manager/tasks, basculer vue Cartes ou Liste",
            "Ouvrir tache PREPARED non assignee",
            "Cliquer 'Assigner recommande (IA)' ou modal IA",
            "Bouton 'Score reussite livraison' si commande liee",
            "Confirmer assignation -> toast succes",
        ],
        "Tache ASSIGNED au chauffeur recommande (ex: Mohamed driver1)",
    )
    pdf.h2("Phase D - Chauffeur : execution livraison")
    pdf.test_case(
        "E2E-04", "Cycle mission chauffeur",
        "DRIVER (driver1@smarttask.com)",
        [
            "Login -> /driver/dashboard : alertes visibles",
            "Aller /driver/tasks -> voir mission assignee",
            "Ouvrir detail /driver/tasks/{id}",
            "Accepter mission -> statut ACCEPTED",
            "Demarrer livraison -> IN_DELIVERY",
            "Mettre a jour GPS (latitude/longitude)",
            "Soumettre preuve livraison (image)",
            "Terminer livraison -> COMPLETED / DELIVERED",
        ],
        "Mission terminee, commande DELIVERED",
    )
    pdf.h2("Phase E - Client : suivi et avis")
    pdf.test_case(
        "E2E-05", "Suivi et confirmation client",
        "CLIENT (client1@smarttask.com)",
        [
            "Login -> /client/dashboard",
            "Aller /client/orders -> voir commande",
            "Pendant livraison : /client/delivery/{id} suivi temps reel (SSE)",
            "Apres DELIVERED : Confirmer reception",
            "Aller /client/reviews -> noter 5 etoiles + commentaire",
        ],
        "Commande RECEIVED, avis enregistre, toast/confirmation OK",
        "Double avis sur meme tache -> erreur"
    )


def ch_auth_admin(pdf):
    pdf.h1("3", "TESTS AUTHENTIFICATION ET ADMIN")
    pdf.test_case("AUTH-01", "Login reussi tous roles", "Tous",
        ["Pour chaque compte du tableau 1.3 : login email/password"],
        "Redirection dashboard correspondant au role",
        "Mauvais mot de passe -> message erreur, reste sur /login")
    pdf.test_case("AUTH-02", "Acces refuse mauvais role", "CLIENT",
        ["Login client1", "Tenter URL /manager/tasks dans barre adresse"],
        "Redirect /access-denied ou 403",
    )
    pdf.test_case("AUTH-03", "Deconnexion", "Tous",
        ["Cliquer Deconnexion dans sidebar", "Tenter acceder dashboard sans login"],
        "Redirect /login",
    )
    pdf.test_case("AUTH-04", "Profil utilisateur", "Tous",
        ["Aller /profile", "Modifier nom ou telephone", "Changer mot de passe"],
        "Profil mis a jour, re-login avec nouveau MDP si change",
    )
    pdf.h2("Tests ADMIN")
    pdf.test_case("ADM-01", "Lister utilisateurs", "ADMIN (admin@smarttask.com)",
        ["Login admin", "/admin/users", "Verifier liste 7+ utilisateurs seed"],
        "Tableau users avec roles ADMIN/MANAGER/OPERATOR/DRIVER/CLIENT",
    )
    pdf.test_case("ADM-02", "Creer utilisateur", "ADMIN",
        ["Cliquer Nouveau", "Email test@test.com, role OPERATOR, MDP Test123!", "Sauvegarder"],
        "Utilisateur cree, login possible",
    )
    pdf.test_case("ADM-03", "Desactiver utilisateur", "ADMIN",
        ["Selectionner user test", "Desactiver", "Tenter login avec ce compte"],
        "Login refuse compte inactif",
    )
    pdf.test_case("ADM-04", "Changer role", "ADMIN",
        ["Modifier role user test -> CLIENT", "Verifier acces /client/dashboard"],
        "Redirection client apres re-login",
    )


def ch_manager(pdf):
    pdf.h1("4", "TESTS MANAGER (TOUTES FONCTIONNALITES)")
    routes_mgr = [r for r in ANGULAR_ROUTES if r[0].startswith("/manager")]
    pdf.h2("4.1 Pages a visiter")
    pdf.table(["Route", "Composant"], [(r[0], r[1]) for r in routes_mgr], [70, 110])
    pdf.test_case("MGR-01", "Dashboard KPIs", "MANAGER",
        ["Login manager", "/manager/dashboard"],
        "Cartes KPI : taches, retards, chauffeurs. Banniere IA visible.",
    )
    pdf.test_case("MGR-02", "Gestion taches CRUD", "MANAGER",
        ["/manager/tasks", "Nouvelle tache", "Remplir titre, client, adresse, priorite", "Sauvegarder",
         "Modifier tache", "Changer statut", "Supprimer tache test"],
        "CRUD complet, filtres statut/recherche OK, vue cartes/liste",
    )
    pdf.test_case("MGR-03", "Assignation manuelle", "MANAGER",
        ["Ouvrir tache PREPARED", "Assigner chauffeur driver1 manuellement"],
        "Tache ASSIGNED, driver1 voit mission",
    )
    pdf.test_case("MGR-04", "Assignation IA", "MANAGER",
        ["Tache PREPARED", "Bouton Assigner recommande (IA)"],
        "Toast succes, chauffeur assigne selon score IA",
    )
    pdf.test_case("MGR-05", "Page retards", "MANAGER",
        ["/manager/delays"],
        "Liste taches en retard ou message vide",
    )
    pdf.test_case("MGR-06", "Chauffeurs", "MANAGER",
        ["/manager/drivers"],
        "Liste driver1, driver2 avec statut zone performance",
    )
    pdf.test_case("MGR-07", "Incidents", "MANAGER",
        ["/manager/incidents", "Ouvrir incident OPEN", "Passer IN_PROGRESS puis RESOLVED"],
        "Statut incident mis a jour",
    )
    pdf.test_case("MGR-08", "Notifications", "MANAGER",
        ["/manager/notifications", "Marquer comme lu"],
        "readFlag true apres action",
    )
    pdf.test_case("MGR-09", "Analytics + export", "MANAGER",
        ["/manager/analytics", "Consulter graphiques", "Exporter CSV"],
        "Fichier CSV telecharge",
    )
    pdf.test_case("MGR-10", "Planning et carte", "MANAGER",
        ["/manager/planning", "/manager/map"],
        "Pages chargent sans erreur console",
    )
    pdf.h2("4.2 Module IA Manager (/manager/ai)")
    pdf.test_case("MGR-IA-01", "Sante service IA", "MANAGER",
        ["/manager/ai", "Verifier statut health et modeles"],
        "Health UP, etat modeles affiche (LOADED ou FALLBACK)",
    )
    pdf.test_case("MGR-IA-02", "Prediction retard", "MANAGER",
        ["Selectionner tache", "Analyser retard"],
        "Probabilite retard + niveau risque LOW/MEDIUM/HIGH",
    )
    pdf.test_case("MGR-IA-03", "Prediction ETA", "MANAGER",
        ["Prediction temps livraison"],
        "Minutes estimees affichees",
    )
    pdf.test_case("MGR-IA-04", "Delivery Success", "MANAGER",
        ["Modal tache", "Score reussite livraison"],
        "Pourcentage succes + facteurs",
    )
    pdf.test_case("MGR-IA-05", "Prioriser tache", "MANAGER",
        ["Prioriser via IA"],
        "Score priorite + explication",
    )
    pdf.test_case("MGR-IA-06", "Recommander chauffeur", "MANAGER",
        ["Recommandation chauffeur pour tache"],
        "Liste candidats scores decroissants",
    )
    pdf.test_case("MGR-IA-07", "Detecter anomalie", "MANAGER",
        ["Detection anomalie sur tache"],
        "Flag anomalie + details",
    )
    pdf.test_case("MGR-IA-08", "Analyse complete", "MANAGER",
        ["Analyse IA complete tache"],
        "Resultat combine delay + driver + priority",
    )
    pdf.h2("4.3 Automation (/manager/automation)")
    pdf.test_case("MGR-AU-01", "Statut automation", "MANAGER",
        ["/manager/automation"],
        "Statut enabled/disabled, config express visible",
    )
    pdf.test_case("MGR-AU-02", "Lancer chaine express manuelle", "MANAGER",
        ["Commande HIGH/CRITICAL", "Lancer automation express", "Consulter logs"],
        "7 etapes dans automation_logs : SUCCESS ou SKIPPED",
    )


def ch_operator(pdf):
    pdf.h1("5", "TESTS OPERATEUR")
    pdf.test_case("OPR-01", "Dashboard", "OPERATOR",
        ["/operator/dashboard"],
        "KPI commandes jour, pending, verified, banniere nouveautes",
    )
    pdf.test_case("OPR-02", "Liste commandes vues", "OPERATOR",
        ["/operator/orders", "Basculer Cartes / Liste"],
        "Commandes affichees, toggle fonctionne",
    )
    pdf.test_case("OPR-03", "Creer commande LOW", "OPERATOR",
        ["/operator/orders/create", "Priorite LOW", "Enregistrer"],
        "Commande PENDING, pas d'automation auto",
    )
    pdf.test_case("OPR-04", "Creer commande HIGH + IA preview", "OPERATOR",
        ["Priorite HIGH", "Analyser reussite livraison avant save", "Enregistrer"],
        "Score IA affiche, automation peut se declencher",
    )
    pdf.test_case("OPR-05", "Commandes en attente", "OPERATOR",
        ["/operator/orders/pending"],
        "Liste PENDING uniquement",
    )
    pdf.test_case("OPR-06", "Verifier commande", "OPERATOR",
        ["Ouvrir commande PENDING", "Verifier"],
        "Statut VERIFIED",
    )
    pdf.test_case("OPR-07", "Preparer commande", "OPERATOR",
        ["/operator/tasks", "Preparer commande READY"],
        "Tache PREPARED liee",
    )
    pdf.test_case("OPR-08", "Suivi taches", "OPERATOR",
        ["/operator/tasks/tracking"],
        "Statuts livraisons visibles",
    )
    pdf.test_case("OPR-09", "Signaler incident", "OPERATOR",
        ["/operator/incidents", "Nouveau incident", "Type + description"],
        "Incident OPEN cree",
    )
    pdf.test_case("OPR-10", "Liste clients", "OPERATOR",
        ["Via API ou UI clients disponibles a la creation commande"],
        "client1, client2 selectionnables",
    )


def ch_driver(pdf):
    pdf.h1("6", "TESTS CHAUFFEUR")
    pdf.test_case("DRV-01", "Dashboard + alertes", "DRIVER",
        ["/driver/dashboard"],
        "Missions du jour, alertes IA si risque retard",
    )
    pdf.test_case("DRV-02", "Liste missions", "DRIVER",
        ["/driver/tasks"],
        "Missions ASSIGNED/ACCEPTED visibles",
    )
    pdf.test_case("DRV-03", "Detail mission workflow", "DRIVER",
        ["/driver/tasks/{id}", "Accept -> Start -> Delivery -> Complete"],
        "Transitions statut OK, historique mis a jour",
    )
    pdf.test_case("DRV-04", "Mise a jour GPS", "DRIVER",
        ["Mettre a jour position lat/lng"],
        "Coordonnees sauvegardees sur tache",
    )
    pdf.test_case("DRV-05", "Preuve livraison", "DRIVER",
        ["Upload image preuve"],
        "proofOfDeliveryImage enregistre",
    )
    pdf.test_case("DRV-06", "Itineraire optimise IA", "DRIVER",
        ["/driver/route", "Consulter ordre optimise"],
        "Missions reordonnees si multi-stops",
    )
    pdf.test_case("DRV-07", "Historique", "DRIVER",
        ["/driver/history"],
        "Livraisons passees listees",
    )
    pdf.test_case("DRV-08", "Performance", "DRIVER",
        ["/driver/performance"],
        "Score performance, total livraisons",
    )
    pdf.test_case("DRV-09", "Incident chauffeur", "DRIVER",
        ["/driver/incidents", "Signaler CLIENT_ABSENT ou VEHICLE_ISSUE"],
        "Incident cree, manager notifie",
    )
    pdf.test_case("DRV-10", "Alertes proactives", "DRIVER",
        ["Attendre 5 min ou POST /api/driver/alerts/check", "Verifier dashboard"],
        "Notification si deadline proche + risque retard",
    )


def ch_client(pdf):
    pdf.h1("7", "TESTS CLIENT")
    pdf.test_case("CLT-01", "Dashboard", "CLIENT",
        ["/client/dashboard"],
        "Resume commandes actives et livrees",
    )
    pdf.test_case("CLT-02", "Mes commandes", "CLIENT",
        ["/client/orders"],
        "Uniquement commandes du client connecte (client1)",
    )
    pdf.test_case("CLT-03", "Detail commande", "CLIENT",
        ["/client/orders/{id}"],
        "Statut, adresse, priorite, taskId si lie",
    )
    pdf.test_case("CLT-04", "Suivi livraison SSE", "CLIENT",
        ["/client/delivery/{id} pendant IN_DELIVERY"],
        "Mises a jour temps reel statut/GPS",
    )
    pdf.test_case("CLT-05", "Confirmer reception", "CLIENT",
        ["Apres DELIVERED", "Confirmer reception"],
        "Statut RECEIVED, clientConfirmed true",
    )
    pdf.test_case("CLT-06", "Laisser avis", "CLIENT",
        ["/client/reviews", "Note 4/5 + commentaire"],
        "Review enregistre",
    )
    pdf.test_case("CLT-07", "Incident client", "CLIENT",
        ["/client/incidents", "Signaler DAMAGED_PRODUCT"],
        "Incident OPEN",
    )
    pdf.test_case("CLT-08", "Notifications", "CLIENT",
        ["/client/notifications"],
        "Notifications livraison visibles",
    )
    pdf.test_case("CLT-09", "Isolation donnees", "CLIENT",
        ["Login client2", "Verifier ne voit pas commandes client1"],
        "Donnees isolees par clientId",
    )


def ch_commun(pdf):
    pdf.h1("8", "TESTS TRANSVERSAUX")
    pdf.h2("8.1 Chatbot Copilot")
    pdf.test_case("CHAT-01", "Ouvrir widget", "Tous roles",
        ["Cliquer bouton flottant Copilot", "Verifier init"],
        "Fenetre chat ouverte, suggestions affichees",
    )
    pdf.test_case("CHAT-02", "Poser question metier", "MANAGER",
        ["Question : Comment assigner une tache ?", "Envoyer"],
        "Reponse contextuelle SmartLogix",
    )
    pdf.test_case("CHAT-03", "Historique", "Tous",
        ["Envoyer 2 messages", "Rouvrir widget"],
        "Historique conserve session",
    )
    pdf.h2("8.2 Toasts et alertes UI")
    pdf.test_case("UI-01", "Toast succes", "OPERATOR",
        ["Creer commande"],
        "Toast vert 'Commande creee avec succes'",
    )
    pdf.test_case("UI-02", "Toast IA", "MANAGER",
        ["Assigner recommande IA"],
        "Toast info avec message assignation",
    )
    pdf.test_case("UI-03", "Alert banner", "OPERATOR",
        ["/operator/orders/create"],
        "Banniere Delivery Success AI visible",
    )
    pdf.h2("8.3 Parametres")
    pdf.test_case("SET-01", "Settings par role", "Tous",
        ["/manager/settings", "/operator/settings", "/driver/settings", "/client/settings"],
        "Pages parametres chargent",
    )


def ch_api(pdf):
    pdf.h1("9", "TESTS API (POSTMAN / CURL)")
    pdf.p("Collection Postman : Backend Smarttask/SmartTask/postman/SmartTask-API.postman_collection.json")
    pdf.h2("9.1 Sequence API type")
    pdf.step(1, "POST /api/auth/login {\"email\":\"manager@smarttask.com\",\"password\":\"Manager123!\"}")
    pdf.step(2, "Copier token JWT de la reponse")
    pdf.step(3, "Header Authorization: Bearer {token} sur requetes suivantes")
    pdf.step(4, "GET /api/manager/dashboard -> 200 + JSON KPIs")
    pdf.step(5, "GET /api/tasks -> 200 + liste paginee")
    pdf.h2("9.2 Tests securite API")
    pdf.test_case("API-SEC-01", "Sans token", "N/A",
        ["GET /api/manager/dashboard sans Authorization"],
        "401 Unauthorized",
    )
    pdf.test_case("API-SEC-02", "Mauvais role", "CLIENT token",
        ["GET /api/tasks avec token client"],
        "403 Forbidden",
    )
    pdf.test_case("API-SEC-03", "Endpoint public", "N/A",
        ["POST /api/auth/login"],
        "200 avec credentials valides",
    )
    pdf.h2("9.3 Tests service IA direct (backend requis)")
    pdf.table(["Methode", "Endpoint", "Test"],
        [(e[0], e[1], e[2][:50]) for e in PYTHON_ENDPOINTS], [18, 55, 107])
    pdf.test_case("AI-01", "Health Python", "N/A",
        ["GET http://localhost:8000/api/ai/health"],
        "status UP, version affichee",
    )
    pdf.test_case("AI-02", "IA down fallback", "MANAGER",
        ["Arreter uvicorn Python", "Predict delay sur tache"],
        "Fallback rule-based, pas crash 500 backend",
    )


def ch_negatif(pdf):
    pdf.h1("10", "TESTS NEGATIFS ET LIMITES")
    pdf.test_case("NEG-01", "Login email invalide", "N/A",
        ["email: notanemail", "password: x"],
        "Validation formulaire ou 401",
    )
    pdf.test_case("NEG-02", "Commande champs vides", "OPERATOR",
        ["Formulaire create sans adresse"],
        "Bouton submit desactive ou erreur validation",
    )
    pdf.test_case("NEG-03", "Complete sans preuve", "DRIVER",
        ["Terminer sans upload si requis"],
        "Erreur metier ou warning",
    )
    pdf.test_case("NEG-04", "Double avis", "CLIENT",
        ["Review deux fois meme tache"],
        "Erreur contrainte unique",
    )
    pdf.test_case("NEG-05", "Assigner chauffeur BUSY", "MANAGER",
        ["Assigner driver deja surcharge"],
        "Warning ou score IA reduit",
    )


def ch_checklist(pdf):
    pdf.h1("11", "CHECKLIST RECETTE FINALE")
    pdf.p("Cocher chaque item avant validation projet.")
    items = [
        ("Auth", "Login/logout 7 comptes OK"),
        ("Auth", "RBAC : acces refuse hors role"),
        ("Admin", "CRUD users complet"),
        ("Operator", "Create/verify/prepare commande"),
        ("Operator", "Delivery Success AI preview"),
        ("Manager", "Dashboard + tasks CRUD"),
        ("Manager", "Assign manuel + IA"),
        ("Manager", "8 fonctions page IA"),
        ("Manager", "Automation express + logs"),
        ("Manager", "Analytics export CSV"),
        ("Driver", "Workflow accept->complete"),
        ("Driver", "Route optimisee IA"),
        ("Driver", "Preuve livraison"),
        ("Client", "Suivi SSE"),
        ("Client", "Confirm + review"),
        ("Transversal", "Chatbot 3 roles"),
        ("Transversal", "Toasts et alert banners"),
        ("API", "Postman collection 100% 2xx sur happy path"),
        ("IA", "Health UP ou fallback graceful"),
        ("Securite", "401/403 verifies"),
    ]
    pdf.table(["Module", "Critere", "OK", "Date", "Testeur"], [
        [i[0], i[1], "[ ]", "", ""] for i in items
    ], [25, 85, 12, 25, 33])
    pdf.h2("11.1 Synthese comptes par scenario")
    pdf.table(
        ["Scenario", "Compte principal", "Comptes secondaires"],
        [
            ["E2E complet", "operator1", "manager, driver1, client1"],
            ["Automation express", "operator1", "manager"],
            ["Multi chauffeur", "manager", "driver1, driver2"],
            ["Isolation client", "client1 vs client2", ""],
            ["Admin users", "admin", "user test cree"],
            ["IA sans Python", "manager", "service IA arrete"],
        ],
        [45, 55, 80],
    )


def ch_troubleshooting(pdf):
    pdf.h1("12", "DEPANNAGE ET FAQ TESTS")
    pdf.table(
        ["Probleme", "Cause probable", "Solution"],
        [
            ["Login 401", "Backend off ou mauvais MDP", "Verifier bootRun + comptes section 1.3"],
            ["CORS error", "Frontend pas localhost:4200", "CORS_ORIGINS dans application.properties"],
            ["IA 503", "Modeles .pkl absents", "cd smarttask-ai && python -m app.ml.train_all"],
            ["IA timeout", "Python non demarre", "uvicorn port 8000"],
            ["Empty dashboard", "DB vide", "Redemarrer backend pour DataInitializer"],
            ["SSE ne connecte pas", "Pas en IN_DELIVERY", "Driver start livraison d'abord"],
            ["403 access denied", "Mauvais role URL", "Utiliser compte du bon role"],
            ["Automation skip", "Priorite LOW", "Utiliser HIGH ou CRITICAL"],
        ],
        [45, 55, 80],
    )


def ch_matrice_api(pdf):
    pdf.h1("13", "MATRICE TESTS API PAR ENDPOINT")
    pdf.p("Cocher apres test Postman ou curl. Token JWT requis sauf PUBLIC.")
    rows = []
    for i, e in enumerate(ENDPOINTS, 1):
        rows.append((f"API-{i:03d}", e[0], e[1][:42], e[2], "[ ]"))
    for chunk_start in range(0, len(rows), 22):
        chunk = rows[chunk_start:chunk_start + 22]
        pdf.table(["ID", "HTTP", "Endpoint", "Role", "OK"], chunk, [18, 14, 62, 22, 10])


def ch_matrice_routes(pdf):
    pdf.h1("14", "MATRICE TESTS UI PAR ROUTE ANGULAR")
    rows = [(r[0], r[1][:35], r[2], "[ ]") for r in ANGULAR_ROUTES]
    for chunk_start in range(0, len(rows), 20):
        chunk = rows[chunk_start:chunk_start + 20]
        pdf.table(["Route", "Composant", "Role", "OK"], chunk, [55, 75, 22, 10])


def build():
    pdf = GuideTests()
    cover(pdf)
    ch_preambule(pdf)
    ch_scenario_global(pdf)
    ch_auth_admin(pdf)
    ch_manager(pdf)
    ch_operator(pdf)
    ch_driver(pdf)
    ch_client(pdf)
    ch_commun(pdf)
    ch_api(pdf)
    ch_negatif(pdf)
    ch_checklist(pdf)
    ch_troubleshooting(pdf)
    ch_matrice_api(pdf)
    ch_matrice_routes(pdf)
    pdf.output(OUT_PDF)
    print(f"PDF genere : {OUT_PDF} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build()
