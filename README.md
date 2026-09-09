# SmartTask — Intelligent Logistics Platform

**SmartTask** is an intelligent web-based logistics and last-mile delivery platform designed to digitize and optimize the complete order-to-delivery lifecycle.

The platform provides dedicated workspaces for **Admin, Manager, Operator, Driver and Client**, while integrating Artificial Intelligence to support delivery prediction, driver recommendation, route optimization, proactive alerts and automated express delivery workflows.

> **Project name:** SmartLogix
> **Technical repository name:** SmartTask

---

## 🚀 Overview

SmartTask addresses common logistics challenges such as:

* Manual order processing
* Non-optimal driver assignment
* Lack of real-time delivery visibility
* Late detection of delivery delays
* Fragmented communication
* Lack of standardized product types
* Limited decision support for logistics managers

The platform combines classical business management with AI-powered logistics automation.

---

## ✨ Main Features

### 👥 Multi-role management

SmartTask provides five dedicated roles:

| Role         | Main responsibilities                                         |
| ------------ | ------------------------------------------------------------- |
| **ADMIN**    | User management, roles, activation/deactivation               |
| **MANAGER**  | Dashboard, tasks, drivers, analytics, AI and automation       |
| **OPERATOR** | Create, validate and prepare orders                           |
| **DRIVER**   | Accept missions, delivery, GPS, route optimization and alerts |
| **CLIENT**   | Order tracking, delivery confirmation, incidents and reviews  |

---

### 📦 Order management

The platform supports the complete order lifecycle:

```text
PENDING
   ↓
VERIFIED
   ↓
PREPARING
   ↓
READY
   ↓
IN_DELIVERY
   ↓
DELIVERED
   ↓
RECEIVED
```

Orders support standardized product types with an optional **Other** value for custom product descriptions.

---

### 🚚 Delivery management

Drivers can:

* View assigned missions
* Accept a delivery mission
* Start a delivery
* Update delivery status
* Send GPS location
* Upload delivery proof
* Complete a delivery
* View delivery history
* View performance indicators
* Receive proactive AI alerts

The system also maintains task history for traceability.

---

### 🤖 Artificial Intelligence

SmartTask integrates a dedicated **Python FastAPI AI microservice**.

Implemented AI capabilities include:

* Delivery delay prediction
* Estimated delivery time (ETA)
* Task prioritization
* Driver recommendation
* Anomaly detection
* Route optimization
* Proactive driver alerts
* SmartTask Copilot chatbot

Current ML models include:

* `delay_model.pkl`
* `delivery_time_model.pkl`

The project also provides a rule-based fallback when the Python AI service is unavailable.

---

### ⚡ Express Delivery Automation

For **HIGH** and **CRITICAL** priority orders, the system can execute an autonomous 7-step workflow:

```text
1. READ_ORDER
2. AUTO_VERIFY
3. CREATE_TASK
4. AI_PRIORITIZE
5. AI_ASSIGN_DRIVER
6. ESTIMATE_AND_NOTIFY
7. LOG_COMPLETE
```

The automation can be triggered automatically through an order event or manually from the management interface.

---

### 💬 SmartTask Copilot

The platform includes a role-aware chatbot assistant.

The chatbot can:

* Answer business-related questions
* Use contextual information according to the current role
* Maintain conversation history
* Use the Python AI service
* Fall back to a Java-based response service when AI is unavailable

---

### 📡 Real-time delivery tracking

Clients can monitor delivery progress using **Server-Sent Events (SSE)**.

The client can receive real-time updates about:

* Delivery status
* Driver position
* Delivery progress
* Notifications

---

### 🚨 Incidents and reviews

The platform supports:

* Incident reporting by different actors
* Incident management by the manager
* Delivery confirmation
* Customer reviews
* Rating from **1 to 5**
* Customer comments

---

## 🏗️ Architecture

SmartTask uses a distributed three-layer architecture:

```text
                    ┌─────────────────────┐
                    │      Angular 16     │
                    │   Frontend / SPA    │
                    │      Port 4200      │
                    └──────────┬──────────┘
                               │
                          REST + JWT
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Spring Boot      │
                    │      Backend        │
                    │      Port 9090      │
                    └───────┬─────┬───────┘
                            │     │
                     JDBC   │     │ WebClient
                            │     │
                            ▼     ▼
                 ┌────────────┐  ┌──────────────────┐
                 │ PostgreSQL │  │ SmartTask AI     │
                 │ Port 5432  │  │ Python FastAPI   │
                 │            │  │ Port 8000        │
                 └────────────┘  └──────────────────┘
```

### Important architecture principle

The Angular frontend does **not** communicate directly with the Python service.

All AI requests are orchestrated by the Spring Boot backend, which communicates with the FastAPI microservice using HTTP/WebClient.

---

## 🛠️ Technology Stack

### Frontend

* Angular 16
* TypeScript
* RxJS
* Angular Router

### Backend

* Java 17
* Spring Boot 4.x
* Spring Security
* Spring Data JPA
* Hibernate
* WebFlux / WebClient
* JWT
* BCrypt
* Gradle
* SpringDoc / OpenAPI

### AI Microservice

* Python 3.11+
* FastAPI
* scikit-learn
* XGBoost
* Pandas
* Machine Learning models

### Database

* PostgreSQL 14+
* Flyway
* Hibernate / JPA

### Testing

* JUnit 5
* Spring Boot Test
* pytest

### DevOps

* Git
* Docker support for the AI service

---

## 📁 Project Structure

```text
ProjetPidev/
│
├── Backend Smarttask/
│   └── SmartTask/
│       ├── src/main/java/tn/esprit/smarttask/
│       │   ├── controller/
│       │   ├── service/
│       │   ├── repository/
│       │   ├── entity/
│       │   ├── dto/
│       │   ├── security/
│       │   ├── config/
│       │   ├── client/
│       │   ├── event/
│       │   └── exception/
│       │
│       └── src/main/resources/
│           ├── application.properties
│           └── db/migration/
│
├── smarttask-frontend/
│   └── src/app/
│       ├── core/
│       ├── features/
│       │   ├── admin/
│       │   ├── manager/
│       │   ├── operator/
│       │   ├── driver/
│       │   └── client/
│       └── shared/
│
├── smarttask-ai/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── ml/
│   │   ├── models/
│   │   └── data/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
└── docs/
```

The project includes the Spring Boot backend, Angular frontend and Python AI microservice.

---

## 🔐 Security

SmartTask uses:

* JWT stateless authentication
* BCrypt password hashing
* Role-Based Access Control (RBAC)
* Spring Security
* `@PreAuthorize`
* Angular authentication guards
* Angular role guards
* JWT HTTP interceptor
* CORS configuration

Supported roles:

```text
ADMIN
MANAGER
OPERATOR
DRIVER
CLIENT
```

---

## 🗄️ Database

The application uses PostgreSQL with Flyway migrations.

Main database entities include:

```text
User
DriverProfile
Order
Task
TaskHistory
ProductType
Notification
Incident
Review
ChatMessage
AutomationLog
```

Flyway manages the database schema through versioned migrations from **V1 to V10**.

---

## 🔌 Main AI API Endpoints

The Python FastAPI microservice exposes endpoints such as:

```text
GET  /api/ai/health
GET  /api/ai/model/status
GET  /api/ai/metrics

POST /api/ai/predict/delay
POST /api/ai/predict/delivery-time
POST /api/ai/prioritize/task
POST /api/ai/recommend/driver
POST /api/ai/detect/anomaly
POST /api/ai/chat
POST /api/ai/optimize/route
```

---

## ▶️ Getting Started

### 1. Prerequisites

Install:

* Java 17
* Node.js / npm
* Angular CLI
* Python 3.11+
* PostgreSQL 14+
* Git

---

### 2. Database

Create the PostgreSQL database:

```sql
CREATE DATABASE smarttask_db;
```

The backend uses:

```text
Host: localhost
Port: 5432
Database: smarttask_db
```

Flyway automatically manages the database migrations when the backend starts.

---

## ▶️ Run the Backend

Go to the Spring Boot project:

```bash
cd "Backend Smarttask/SmartTask"
```

Run:

### Windows

```cmd
gradlew bootRun
```

Backend:

```text
http://localhost:9090
```

Swagger:

```text
http://localhost:9090/swagger-ui.html
```

---

## ▶️ Run the AI Microservice

Go to:

```bash
cd smarttask-ai
```

Create/activate the virtual environment:

### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

Train the ML models:

```cmd
python -m app.ml.train_all
```

Start FastAPI:

```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

AI documentation:

```text
http://localhost:8000/docs
```

> The generated `.pkl` model files are created locally and should not be committed to Git.

---

## ▶️ Run the Frontend

Go to:

```bash
cd smarttask-frontend
```

Install dependencies:

```bash
npm install
```

Start Angular:

```bash
ng serve
```

Frontend:

```text
http://localhost:4200
```

---

## 🔄 Complete Startup Order

The recommended startup order is:

```text
1. PostgreSQL
       ↓
2. Spring Boot
       ↓
3. SmartTask AI / FastAPI
       ↓
4. Angular
```

Services and ports:

| Service        | Port |
| -------------- | ---: |
| Angular        | 4200 |
| Spring Boot    | 9090 |
| Python FastAPI | 8000 |
| PostgreSQL     | 5432 |

## These ports and startup commands correspond to the project's documented architecture and startup guide.

## 🧪 Testing

### Backend

```cmd
gradlew test
```

### Frontend

```cmd
ng test
```

### AI Microservice

```cmd
pytest
```

The project includes JUnit tests for the backend and pytest tests for the Python service.

---

## 📊 Delivery Workflow

A typical delivery follows:

```text
Client / Operator
       ↓
Create Order
       ↓
Order Verification
       ↓
Preparation
       ↓
Driver Assignment
       ↓
Driver Accepts Mission
       ↓
Delivery Started
       ↓
GPS Tracking
       ↓
Delivery Proof
       ↓
Delivered
       ↓
Client Confirms Reception
       ↓
Customer Review
```

---

## 🤖 AI Delivery Workflow

For urgent orders:

```text
HIGH / CRITICAL ORDER
        ↓
READ_ORDER
        ↓
AUTO_VERIFY
        ↓
CREATE_TASK
        ↓
AI_PRIORITIZE
        ↓
AI_ASSIGN_DRIVER
        ↓
ETA + NOTIFICATION
        ↓
LOG_COMPLETE
```

---

## 📌 Project Objectives

The main objectives of SmartTask are:

* Digitize logistics operations
* Centralize orders and delivery tasks
* Improve driver assignment
* Predict delivery delays
* Estimate delivery time
* Optimize driver routes
* Automate urgent deliveries
* Improve real-time visibility
* Provide role-based assistance through Copilot
* Improve security and traceability

---

## 🔮 Future Improvements

Potential future developments include:

* Complete CI/CD pipeline
* Docker Compose for the entire platform
* Kubernetes deployment
* Mobile application for drivers
* Training ML models with real-world datasets
* Additional automation chains
* Advanced incident recovery
* More advanced delivery proof mechanisms

These perspectives are identified in the project documentation.

---

## 🎓 Academic Context

**SmartTask / SmartLogix** was developed as a **Final Year Project (PFE)** focused on intelligent logistics and last-mile delivery.

The project demonstrates the integration of:

* Web development
* Microservices architecture
* Artificial Intelligence
* Machine Learning
* Secure REST APIs
* Real-time communication
* Workflow automation
* Database migrations
* Software testing

---

## 👨‍💻 Project

**SmartLogix — Intelligent Logistics Management Platform**

**Technical repository:** `smarttask-logistics-platform`

Built with:

```text
Angular + Spring Boot + PostgreSQL + Python FastAPI + Machine Learning
```

---

## 📄 License

This project is developed for academic and educational purposes as part of a Final Year Project (PFE).
# smarttask-logistics-platform
SmartTask is an intelligent logistics and last-mile delivery platform built with Angular, Spring Boot, PostgreSQL and a Python FastAPI AI microservice.
