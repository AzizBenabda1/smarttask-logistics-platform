# -*- coding: utf-8 -*-
"""Generate SmartTask complete project report PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date
import os

OUT = os.path.join(os.path.dirname(__file__), "Rapport_SmartTask_Complet.pdf")


class RapportPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"SmartTask - Rapport Projet PFE | Page {self.page_no()}", align="C")

    def chapter_title(self, num, title):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(15, 76, 129)
        self.cell(0, 10, f"{num}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)
        self.set_draw_color(15, 76, 129)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def section(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, f"  - {text}")
        self.ln(0.5)

    def diagram_box(self, title, content):
        self.section(title)
        self.set_font("Courier", "", 8)
        self.set_fill_color(245, 247, 250)
        self.set_text_color(20, 20, 20)
        for line in content.strip().split("\n"):
            self.cell(0, 4.5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.ln(3)

    def table_simple(self, headers, rows, col_widths=None):
        if not col_widths:
            w = 190 / len(headers)
            col_widths = [w] * len(headers)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(15, 76, 129)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True)
        self.ln()
        self.set_font("Helvetica", "", 8)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in rows:
            if self.get_y() > 270:
                self.add_page()
            if fill:
                self.set_fill_color(240, 244, 248)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6, str(cell)[:60], border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(3)


def build():
    pdf = RapportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(10, 10, 10)

    # === PAGE DE GARDE ===
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(15, 76, 129)
    pdf.ln(40)
    pdf.cell(0, 15, "SmartTask", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "Plateforme Logistique Intelligente", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Rapport Complet du Projet PFE", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "Projet de Fin d'Etudes (PFE)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, f"Date : {date.today().strftime('%d/%m/%Y')}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(0, 6,
        "Ce document presente l'ensemble du projet SmartTask : problematique, solution, "
        "methodologie, architecture, technologies, diagrammes UML, backend, frontend, "
        "microservice IA et chaine d'automation.", align="C")

    # === SOMMAIRE ===
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(0, 10, "Table des matieres", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    toc = [
        "1. Introduction et contexte",
        "2. Problematique",
        "3. Solution proposee",
        "4. Methodologie de developpement",
        "5. Architecture globale",
        "6. Technologies et langages utilises",
        "7. Diagramme de cas d'utilisation",
        "8. Diagramme de classes",
        "9. Diagrammes de sequence",
        "10. Base de donnees",
        "11. Backend (Spring Boot) - detail",
        "12. Frontend (Angular) - detail",
        "13. Microservice IA (Python FastAPI)",
        "14. Chaine d'automation IA",
        "15. Securite et gestion des roles",
        "16. Tests et validation",
        "17. Guide de demarrage",
        "18. Conclusion",
    ]
    pdf.set_font("Helvetica", "", 11)
    for item in toc:
        pdf.cell(0, 7, item, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # === 1 INTRODUCTION ===
    pdf.chapter_title("1", "Introduction et contexte")
    pdf.body(
        "SmartTask est une plateforme web de gestion logistique destinee aux entreprises de "
        "livraison. Elle permet de gerer les commandes, les taches de livraison, les chauffeurs, "
        "les clients et les incidents, tout en integrant l'intelligence artificielle pour "
        "predire les retards, recommander les chauffeurs et automatiser les livraisons express."
    )
    pdf.body(
        "Le projet est developpe selon une architecture en trois couches : une interface "
        "Angular, un backend Java Spring Boot et un microservice Python dedie a l'IA."
    )

    # === 2 PROBLEMATIQUE ===
    pdf.chapter_title("2", "Problematique")
    pdf.body(
        "Les entreprises de logistique font face a plusieurs defis majeurs dans la gestion "
        "quotidienne de leurs operations :"
    )
    pdf.bullet("Traitement manuel des commandes : validation, preparation et assignation prennent du temps.")
    pdf.bullet("Manque de visibilite : managers et clients ne suivent pas facilement l'etat des livraisons.")
    pdf.bullet("Assignation non optimale : choix du chauffeur base sur l'experience, pas sur des donnees.")
    pdf.bullet("Retards non anticipes : pas d'alerte precoce avant qu'un retard ne se produise.")
    pdf.bullet("Communication fragmentee : pas d'assistant centralise pour repondre aux questions.")
    pdf.bullet("Typage des produits : saisie libre des produits sans standardisation.")
    pdf.ln(2)
    pdf.body(
        "Question centrale : Comment concevoir une plateforme intelligente qui automatise "
        "les livraisons urgentes, assiste les decideurs par l'IA et offre une experience "
        "multi-acteurs (admin, manager, operateur, chauffeur, client) ?"
    )

    # === 3 SOLUTION ===
    pdf.chapter_title("3", "Solution proposee")
    pdf.body("SmartTask repond a la problematique par les modules suivants :")
    pdf.table_simple(
        ["Module", "Description"],
        [
            ["Gestion multi-roles", "5 espaces dedies : Admin, Manager, Operateur, Chauffeur, Client"],
            ["Cycle commande/livraison", "Workflow complet de la commande a la reception client"],
            ["Types de produits", "Liste standardisee + option Autre pour saisie libre"],
            ["IA predictive", "Retard, ETA, priorisation, recommandation chauffeur"],
            ["Automation express", "Chaine autonome 7 etapes pour commandes HIGH/CRITICAL"],
            ["Chatbot Copilot", "Assistant contextuel par role avec historique"],
            ["Incidents & avis", "Signalement et evaluation post-livraison"],
            ["Notifications", "Alertes temps reel pour tous les acteurs"],
        ],
        [55, 135],
    )

    # === 4 METHODOLOGIE ===
    pdf.chapter_title("4", "Methodologie de developpement")
    pdf.section("Approche adoptee")
    pdf.body(
        "Developpement iteratif et incremental, organise en phases fonctionnelles :"
    )
    pdf.bullet("Phase 1 : Authentification JWT et gestion utilisateurs (5 roles)")
    pdf.bullet("Phase 2 : Entites metier (commandes, taches, chauffeurs, notifications)")
    pdf.bullet("Phase 3 : Interfaces Angular par role avec design system")
    pdf.bullet("Phase 4 : Microservice Python IA (predictions ML)")
    pdf.bullet("Phase 5 : Integration Spring Boot <-> Python via WebClient")
    pdf.bullet("Phase 6 : Chatbot SmartTask Copilot")
    pdf.bullet("Phase 7 : Chaine Livraison Express Autonome (automation)")
    pdf.bullet("Phase 8 : Types de produits avec option Autre")
    pdf.section("Outils")
    pdf.bullet("IDE : Cursor / IntelliJ / VS Code")
    pdf.bullet("Versionnement : Git")
    pdf.bullet("Migrations BDD : Flyway (V1 a V10)")
    pdf.bullet("API docs : Swagger OpenAPI (SpringDoc)")
    pdf.bullet("Tests : JUnit 5 + Spring Boot Test")

    # === 5 ARCHITECTURE ===
    pdf.chapter_title("5", "Architecture globale")
    pdf.diagram_box("Architecture 3 tiers", """
+-------------------------------------------------------------------+
|                    NAVIGATEUR (Utilisateur)                        |
|                    Angular 16 - Port 4200                          |
+----------------------------+--------------------------------------+
                             | HTTP REST + JWT
                             v
+-------------------------------------------------------------------+
|              BACKEND Spring Boot - Port 9090                       |
|  Controllers | Services | Security JWT | JPA | Events | Flyway    |
+--------+----------------------------+-----------------------------+
         |                            |
         | JDBC                       | WebClient HTTP
         v                            v
+------------------+         +------------------------+
|   PostgreSQL     |         |  SmartTask AI (Python) |
|   smarttask_db   |         |  FastAPI - Port 8000   |
|   Port 5432      |         |  ML Models + Chatbot   |
+------------------+         +------------------------+
    """)
    pdf.body(
        "Principe cle : le frontend Angular ne communique JAMAIS directement avec Python. "
        "Toutes les requetes passent par Spring Boot qui orchestre la logique metier et "
        "delegue les calculs IA au microservice Python."
    )

    # === 6 TECHNOLOGIES ===
    pdf.chapter_title("6", "Technologies et langages utilises")
    pdf.table_simple(
        ["Couche", "Technologie", "Version", "Role"],
        [
            ["Frontend", "Angular + TypeScript", "16.2", "Interface utilisateur SPA"],
            ["Frontend", "RxJS", "7.8", "Programmation reactive"],
            ["Backend", "Java + Spring Boot", "17 / 4.x", "API REST, securite, metier"],
            ["Backend", "Spring Security + JWT", "jjwt 0.12", "Authentification stateless"],
            ["Backend", "Spring Data JPA", "-", "ORM Hibernate"],
            ["Backend", "Flyway", "-", "Migrations SQL versionnees"],
            ["IA", "Python + FastAPI", "3.11+", "Microservice predictions ML"],
            ["IA", "scikit-learn / XGBoost", "-", "Modeles ML"],
            ["BDD", "PostgreSQL", "14+", "Stockage persistant"],
            ["Build", "Gradle / npm", "-", "Compilation et dependances"],
        ],
        [30, 45, 30, 85],
    )

    # === 7 CAS D'UTILISATION ===
    pdf.chapter_title("7", "Diagramme de cas d'utilisation")
    pdf.diagram_box("Acteurs et cas d'utilisation principaux", """
                        +------------------+
                        |     SmartTask    |
                        +------------------+
    +----------+      |                  |      +----------+
    |  Admin   |------| Gerer utilisat.  |      | Manager  |
    +----------+      | Tableau de bord  |------+----------+
                      | Gerer taches     |      | Assigner |
    +----------+      | Voir analytics   |      | chauffeur|
    | Operateur|------| Creer commande   |      | IA Auto. |
    +----------+      | Valider/Preparer |      +----------+
                      | Choisir type prod|
    +----------+      |                  |      +----------+
    | Chauffeur|------| Accepter mission |      |  Client  |
    +----------+      | Livrer + preuve  |------+----------+
                      | Signaler incident|      | Suivre   |
                      | Chatbot Copilot  |      | Confirmer|
                      +------------------+      +----------+
    """)
    pdf.table_simple(
        ["Acteur", "Cas d'utilisation principaux"],
        [
            ["Admin", "CRUD utilisateurs, activer/desactiver, changer roles"],
            ["Manager", "Dashboard KPIs, taches, chauffeurs, retards, IA, automation"],
            ["Operateur", "Creer commande (type produit), valider, preparer, incidents"],
            ["Chauffeur", "Accepter mission, demarrer, livrer, preuve, GPS"],
            ["Client", "Voir commandes, suivi livraison SSE, confirmer, avis"],
            ["Systeme IA", "Predire retard, ETA, prioriser, recommander chauffeur"],
            ["Automation", "Chaine express 7 etapes (auto HIGH/CRITICAL)"],
        ],
        [35, 155],
    )

    # === 8 CLASSES ===
    pdf.chapter_title("8", "Diagramme de classes (simplifie)")
    pdf.diagram_box("Entites principales et relations", """
+----------------+       +----------------+       +----------------+
|     User       |       |     Order      |       |  ProductType   |
+----------------+       +----------------+       +----------------+
| id             |<------| client_id      |       | id             |
| email          |       | operator_id    |------>| product_type_id|
| role (enum)    |       | products       |       | name           |
| password       |       | priority       |       | code           |
+----------------+       | status         |       +----------------+
        |                | task_id        |
        |                +----------------+
        |                        |
        v                        v
+----------------+       +----------------+       +----------------+
| DriverProfile  |       |     Task       |       | AutomationLog  |
+----------------+       +----------------+       +----------------+
| user_id        |       | client_id      |       | run_id         |
| status, zone   |       | driver_id      |       | step_number    |
| performance    |       | order_id       |       | step_name      |
+----------------+       | status         |       | status         |
                         | deadline       |       +----------------+
                         +----------------+
        |                        |
        v                        v
+----------------+       +----------------+       +----------------+
|  Notification  |       |   Incident     |       |  ChatMessage   |
+----------------+       +----------------+       +----------------+
| user_id        |       | reporter_id    |       | user_id        |
| type, message  |       | task_id        |       | session_id     |
+----------------+       +----------------+       +----------------+
    """)
    pdf.body("Enums principaux : Role, TaskStatus, OrderStatus, Priority, DriverStatus, IncidentStatus")

    # === 9 SEQUENCE ===
    pdf.chapter_title("9", "Diagrammes de sequence")
    pdf.section("9.1 Authentification")
    pdf.diagram_box("Sequence - Login JWT", """
Utilisateur    Angular         Spring Boot       PostgreSQL
    |              |                 |                |
    |-- login ---->|                 |                |
    |              |-- POST /auth/login ------------->|
    |              |                 |-- verify pwd ->|
    |              |                 |<-- user -------|
    |              |<-- JWT token ---|                |
    |<-- redirect -|                 |                |
    |              |-- requetes + Bearer token ------->|
    """)
    pdf.section("9.2 Creation commande + Automation")
    pdf.diagram_box("Sequence - Commande HIGH + Chaine IA", """
Operateur   Angular    Spring Boot    EventListener   Python IA    PostgreSQL
   |           |            |               |             |            |
   |-- creer ->|            |               |             |            |
   |           |-- POST order ----------->  |             |            |
   |           |            |-- save ------------------------------->|
   |           |            |-- publish OrderCreatedEvent ->|        |
   |           |            |               |-- execute chain ----->|
   |           |            |               |-- AUTO_VERIFY ------->|
   |           |            |               |-- CREATE_TASK ------->|
   |           |            |               |-- AI_PRIORITIZE ----->|
   |           |            |               |<-- score -------------|
   |           |            |               |-- AI_ASSIGN_DRIVER -->|
   |           |            |               |-- NOTIFY client ---->|
   |           |            |               |-- LOG_COMPLETE ----->|
   |<- OK -----|<-----------|               |             |            |
    """)
    pdf.section("9.3 Prediction IA")
    pdf.diagram_box("Sequence - Prediction retard", """
Manager    Angular    Spring Boot    SmartTaskAIClient    Python IA
  |          |            |                 |                |
  |-- click->|            |                 |                |
  |          |-- POST predict-delay ------> |                |
  |          |            |-- WebClient POST /predict/delay ->|
  |          |            |                 |<-- ML result --|
  |          |<-- JSON ---|<----------------|                |
  |<- affiche|            |                 |                |
    """)

    # === 10 BDD ===
    pdf.chapter_title("10", "Base de donnees")
    pdf.body("PostgreSQL avec 10 migrations Flyway (V1 a V10) :")
    pdf.table_simple(
        ["Migration", "Contenu"],
        [
            ["V1", "Table users (5 roles)"],
            ["V2", "driver_profiles, tasks, task_history, notifications"],
            ["V3", "orders, incidents, reviews"],
            ["V4", "Statut RECEIVED pour commandes"],
            ["V5", "Seed commande DELIVERED pour tests client"],
            ["V6", "Index de performance"],
            ["V7", "Preuve de livraison (image)"],
            ["V8", "chat_messages (chatbot)"],
            ["V9", "automation_logs (chaine IA)"],
            ["V10", "product_types + lien orders"],
        ],
        [25, 165],
    )

    # === 11 BACKEND ===
    pdf.chapter_title("11", "Backend (Spring Boot) - Detail")
    pdf.section("Structure des packages")
    pdf.bullet("controller/ : 12 controleurs REST (Auth, User, Task, Manager, Operator, Driver, Client, Automation, Chat, ProductType...)")
    pdf.bullet("service/ : logique metier (OperatorService, TaskService, ManagerService...)")
    pdf.bullet("service/automation/ : ExpressDeliveryAutomationService (7 etapes)")
    pdf.bullet("service/chat/ : ChatService, ChatContextBuilder, ChatFallback")
    pdf.bullet("service/ai/ : CompositeAIRecommendationService (Python + fallback regles)")
    pdf.bullet("entity/ : 11 entites JPA + enums")
    pdf.bullet("security/ : JwtAuthenticationFilter, CustomUserDetailsService")
    pdf.bullet("event/ : OrderCreatedEvent + AutomationEventListener (@Async)")
    pdf.section("Controleurs principaux")
    pdf.table_simple(
        ["Controller", "Prefixe", "Role"],
        [
            ["AuthenticationController", "/api/auth", "Public"],
            ["UserController", "/api/users", "ADMIN"],
            ["TaskController", "/api/tasks", "MANAGER"],
            ["ManagerController", "/api/manager", "MANAGER"],
            ["OperatorController", "/api/operator", "OPERATOR"],
            ["DriverController", "/api/driver", "DRIVER"],
            ["ClientController", "/api/client", "CLIENT"],
            ["AutomationController", "/api/automation", "MANAGER/OPERATOR"],
            ["ChatController", "/api/chat", "Authentifie"],
            ["ProductTypeController", "/api/product-types", "Authentifie"],
        ],
        [55, 55, 80],
    )
    pdf.section("Cycle de vie commande")
    pdf.body("PENDING -> VERIFIED -> PREPARING -> READY -> IN_DELIVERY -> DELIVERED -> RECEIVED")
    pdf.section("Cycle de vie tache")
    pdf.body("PENDING/PREPARED -> ASSIGNED -> ACCEPTED -> IN_PROGRESS -> IN_DELIVERY -> COMPLETED")

    # === 12 FRONTEND ===
    pdf.chapter_title("12", "Frontend (Angular) - Detail")
    pdf.section("Organisation")
    pdf.bullet("core/ : auth (guard, interceptor JWT), services HTTP, modeles TypeScript")
    pdf.bullet("features/ : composants par role (admin, manager, operator, driver, client)")
    pdf.bullet("shared/ : chat-widget, design system, styles globaux")
    pdf.bullet("Routes lazy-loaded pour performance")
    pdf.section("Pages par role")
    pdf.table_simple(
        ["Role", "Pages principales"],
        [
            ["Manager", "Dashboard, Taches, Planning, Carte, Chauffeurs, Retards, IA, Automation, Analytics"],
            ["Operateur", "Dashboard, Commandes, Nouvelle commande (types produit), Taches, Suivi"],
            ["Chauffeur", "Dashboard, Missions, Route, Historique, Performance"],
            ["Client", "Dashboard, Commandes, Suivi livraison, Avis, Notifications"],
            ["Admin", "Dashboard, Gestion utilisateurs"],
        ],
        [35, 155],
    )
    pdf.section("Services Angular cles")
    pdf.bullet("AuthService : login/logout, stockage JWT localStorage")
    pdf.bullet("AutomationService : status, logs, lancer chaine express")
    pdf.bullet("ProductTypeService : liste types de produits")
    pdf.bullet("ChatService : init session, envoyer message, historique")
    pdf.bullet("AiService : predictions via backend (pas d'appel direct Python)")

    # === 13 IA ===
    pdf.chapter_title("13", "Microservice IA (Python FastAPI)")
    pdf.body("Microservice independant sur le port 8000. Spring Boot l'appelle via WebClient.")
    pdf.table_simple(
        ["Endpoint", "Description"],
        [
            ["GET /api/ai/health", "Sante du service"],
            ["POST /api/ai/predict/delay", "Prediction risque de retard"],
            ["POST /api/ai/predict/delivery-time", "Estimation ETA (minutes)"],
            ["POST /api/ai/prioritize/task", "Score de priorite"],
            ["POST /api/ai/recommend/driver", "Recommandation chauffeur"],
            ["POST /api/ai/detect/anomaly", "Detection anomalies"],
            ["POST /api/ai/chat", "Reponse chatbot Copilot"],
        ],
        [70, 120],
    )
    pdf.section("Modeles ML")
    pdf.bullet("delay_model.pkl : classification retard (Logistic Regression / Random Forest / XGBoost)")
    pdf.bullet("delivery_time_model.pkl : regression temps livraison (XGBoost)")
    pdf.bullet("Fallback rule-based si Python indisponible")

    # === 14 AUTOMATION ===
    pdf.chapter_title("14", "Chaine d'automation IA")
    pdf.body(
        "La chaine « Livraison Express Autonome » execute 7 instructions automatiquement "
        "lorsqu'une commande HIGH ou CRITICAL est creee."
    )
    pdf.table_simple(
        ["Etape", "Nom", "Action"],
        [
            ["1", "READ_ORDER", "Lire les details de la commande"],
            ["2", "AUTO_VERIFY", "Valider automatiquement (PENDING -> VERIFIED)"],
            ["3", "CREATE_TASK", "Creer tache PREPARED, commande -> READY"],
            ["4", "AI_PRIORITIZE", "Prioriser via microservice Python"],
            ["5", "AI_ASSIGN_DRIVER", "Assigner chauffeur si score >= 70%"],
            ["6", "ESTIMATE_AND_NOTIFY", "Calculer ETA + notifier client/chauffeur"],
            ["7", "LOG_COMPLETE", "Ecrire journal dans automation_logs"],
        ],
        [15, 45, 130],
    )
    pdf.section("Declenchement")
    pdf.bullet("Automatique : OrderCreatedEvent + priorite HIGH/CRITICAL")
    pdf.bullet("Manuel : POST /api/automation/express/{orderId}")
    pdf.bullet("Visualisation : page Manager > IA Automation")

    # === 15 SECURITE ===
    pdf.chapter_title("15", "Securite et gestion des roles")
    pdf.bullet("Authentification JWT stateless (24h expiration)")
    pdf.bullet("Mots de passe hashes BCrypt")
    pdf.bullet("5 roles : ADMIN, MANAGER, OPERATOR, DRIVER, CLIENT")
    pdf.bullet("Controle d'acces par URL (@PreAuthorize + SecurityFilterChain)")
    pdf.bullet("Frontend : authGuard + roleGuard + jwt.interceptor")
    pdf.section("Comptes de test")
    pdf.table_simple(
        ["Email", "Mot de passe", "Role"],
        [
            ["admin@smarttask.com", "Admin123!", "ADMIN"],
            ["manager@smarttask.com", "Manager123!", "MANAGER"],
            ["operator1@smarttask.com", "Operator123!", "OPERATOR"],
            ["driver1@smarttask.com", "Driver123!", "DRIVER"],
            ["client1@smarttask.com", "Client123!", "CLIENT"],
        ],
        [65, 45, 80],
    )

    # === 16 TESTS ===
    pdf.chapter_title("16", "Tests et validation")
    pdf.bullet("Tests JUnit : AuthenticationController, ManagerAI, AutomationController, Security")
    pdf.bullet("Profil test : H2 in-memory, Flyway desactive")
    pdf.bullet("Build Angular : ng build (production OK)")
    pdf.bullet("Build Backend : gradlew compileJava / test")
    pdf.section("Scenarios de test manuels")
    pdf.bullet("Login par role et verification acces pages")
    pdf.bullet("Creer commande avec type produit + option Autre")
    pdf.bullet("Creer commande HIGH -> verifier chaine automation (7 logs)")
    pdf.bullet("Manager : assigner chauffeur, voir analytics")
    pdf.bullet("Chauffeur : accepter et completer mission")
    pdf.bullet("Client : confirmer reception et laisser avis")

    # === 17 DEMARRAGE ===
    pdf.chapter_title("17", "Guide de demarrage")
    pdf.table_simple(
        ["Service", "Commande", "Port"],
        [
            ["PostgreSQL", "Demarrer service + creer smarttask_db", "5432"],
            ["Backend", "gradlew bootRun", "9090"],
            ["Python IA", "uvicorn app.main:app --port 8000", "8000"],
            ["Frontend", "ng serve", "4200"],
        ],
        [35, 100, 55],
    )
    pdf.body("URLs : Frontend http://localhost:4200 | Swagger http://localhost:9090/swagger-ui.html | IA http://localhost:8000/docs")

    # === 18 CONCLUSION ===
    pdf.chapter_title("18", "Conclusion")
    pdf.body(
        "SmartTask est une plateforme logistique complete integrant gestion multi-acteurs, "
        "intelligence artificielle et automation. Le projet demontre la maitrise d'une "
        "architecture microservices (Angular + Spring Boot + Python), la securite JWT, "
        "les migrations de base de donnees, et l'automatisation metier via la chaine "
        "Livraison Express Autonome."
    )
    pdf.body(
        "Perspectives d'evolution : chaines automation supplementaires (gardien anti-retard, "
        "recovery incident), deploiement Docker, application mobile chauffeur, et "
        "apprentissage ML sur donnees reelles."
    )

    pdf.output(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"PDF genere : {path}")
