# 🩺 DermaAI — AI-Powered Skin Disease Detection Platform

**DermaAI** is a secure, modular web platform that combines **Deep Learning–based skin disease classification** with a **Django-based healthcare management system**.

The platform allows users to upload skin lesion images for AI-assisted analysis while providing authentication, role-based access control, doctor discovery, and appointment management through a unified backend.

> **Note:** DermaAI is an academic/software engineering project and is intended for research and educational purposes. Its predictions are not a substitute for professional medical diagnosis.

---

## 🚀 Features

### 🧠 AI-Powered Skin Disease Classification

* Custom-trained **EfficientNetB0** model for skin lesion classification.
* TensorFlow/Keras-based inference pipeline.
* CPU-compatible inference for deployment on commodity hardware.
* Singleton inference engine to avoid repeatedly loading the model into memory.
* Image preprocessing and model inference integrated directly into the Django backend.
* Model files are kept outside version control.

### 🔐 Authentication & Authorization

* JWT-based authentication using **Django REST Framework SimpleJWT**.
* Role-based access control for:

  * Patients
  * Doctors
  * Administrators
* Protected API endpoints using DRF permissions.
* Scoped API throttling for sensitive endpoints.
* Environment-based configuration for secrets and deployment settings.

### 🏥 Healthcare Management

* Doctor discovery and filtering.
* Doctor specialization management.
* Patient-doctor appointment workflow.
* Secure storage of sensitive patient information.
* Appointment records associated with authenticated users.
* Separation of application responsibilities through Django apps.

### ⚡ Performance-Oriented Design

* Singleton model loading to minimize repeated initialization overhead.
* Monolithic deployment keeps AI inference and application logic within the same backend process.
* Designed for low-latency inference on CPU-based systems.
* REST API architecture allows the backend to be consumed by web or mobile clients.

---

## 🏗️ Architecture

DermaAI follows a **Modular Monolith** architecture.

Rather than splitting the system into multiple microservices, related components are organized into separate Django applications while sharing a single deployment and database.

```text
                         ┌─────────────────────┐
                         │      Client         │
                         │  Web / API Consumer │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Django + DRF    │
                         │                     │
                         │ Authentication      │
                         │ Permissions         │
                         │ API Endpoints       │
                         │ Throttling          │
                         └───────┬─────┬───────┘
                                 │     │
                    ┌────────────┘     └─────────────┐
                    ▼                                ▼
          ┌──────────────────┐              ┌──────────────────┐
          │   ML Engine      │              │ Healthcare Logic │
          │                  │              │                  │
          │ EfficientNetB0   │              │ Doctors          │
          │ Preprocessing    │              │ Appointments     │
          │ Inference        │              │ Patient Data     │
          └────────┬─────────┘              └────────┬─────────┘
                   │                                 │
                   └──────────────┬──────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │     MySQL       │
                         │                 │
                         │ Users           │
                         │ Doctors         │
                         │ Appointments    │
                         │ Application Data│
                         └─────────────────┘
```

### Project Structure

```text
DermaAI/
│
├── ml_engine/
│   ├── predictor.py
│   └── models/
│       └── *.h5
│
├── web_app/
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── appointments/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
├── users/
│   ├── models.py
│   ├── permissions.py
│   └── serializers.py
│
├── DermaAI_Project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── Pipfile
└── README.md
```

---

## 🛠️ Tech Stack

| Category              | Technology                       |
| --------------------- | -------------------------------- |
| Backend               | **Django 5**                     |
| API                   | **Django REST Framework**        |
| Authentication        | **SimpleJWT / JWT**              |
| Machine Learning      | **TensorFlow / Keras**           |
| CNN Architecture      | **EfficientNetB0**               |
| Database              | **MySQL 8**                      |
| Encryption            | **Fernet / django-cryptography** |
| Dependency Management | **Pipenv**                       |
| Language              | **Python**                       |

---

## 🔬 Machine Learning Pipeline

The diagnostic workflow follows a simple inference pipeline:

```text
Skin Image
    │
    ▼
Image Upload
    │
    ▼
Validation & Preprocessing
    │
    ▼
EfficientNetB0
    │
    ▼
Class Probabilities
    │
    ▼
Predicted Skin Condition
    │
    ▼
API Response
```

The trained model is loaded through a singleton inference component so that multiple API requests can reuse the same model instance rather than repeatedly loading the `.h5` file.

This reduces unnecessary initialization overhead and is particularly useful when deploying the application on memory-constrained systems.

---

## 🔐 Security

Security is implemented at the application and API layers.

### Authentication

JWT authentication is used for protected API resources.

```text
Client
  │
  │ Login
  ▼
JWT Authentication
  │
  ▼
Access Token
  │
  ▼
Protected API
```

### Authorization

Different user roles receive different permissions:

| Role          | Example Capabilities                             |
| ------------- | ------------------------------------------------ |
| Patient       | AI prediction, doctor discovery, appointments    |
| Doctor        | Manage professional information and appointments |
| Administrator | Manage users and system resources                |

### Sensitive Data

Selected sensitive patient information is encrypted at the application/database field level rather than being stored as plain text.

> Encryption protects stored data, but production healthcare systems would require additional controls such as proper key management, auditing, access policies, infrastructure security, backups, and regulatory compliance.

---

## 🔌 API

| Method | Endpoint            | Description                    | Authentication |
| ------ | ------------------- | ------------------------------ | -------------- |
| `POST` | `/auth/users/`      | Register a user                | No             |
| `POST` | `/auth/jwt/create/` | Obtain JWT tokens              | No             |
| `POST` | `/api/predict/`     | Submit image for AI prediction | Yes            |
| `GET`  | `/api/doctors/`     | Retrieve available doctors     | No             |
| `POST` | `/api/book/`        | Create an appointment          | Yes            |

---

## ⚙️ Installation

### Prerequisites

* Python 3.10+
* MySQL 8+
* Git
* Pipenv

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/DermaAI.git
cd DermaAI
```

### 2. Create the Environment

```bash
pip install pipenv
pipenv install
pipenv shell
```

### 3. Configure MySQL

Create a database:

```sql
CREATE DATABASE derma_ai_db;
```

Configure the database credentials through environment variables or your Django settings.

> Do not commit database passwords, API keys, Django `SECRET_KEY`, or other credentials to Git.

### 4. Add the Trained Model

Place the trained model inside:

```text
ml_engine/models/
```

For example:

```text
ml_engine/models/skin_model_v1.h5
```

Configure the active model filename in the Django settings.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create an Administrator

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## 📊 Engineering Highlights

This project demonstrates practical experience with:

* Designing a **Django modular monolith**
* Building REST APIs with **Django REST Framework**
* Implementing **JWT authentication**
* Designing **role-based permissions**
* Integrating a trained Deep Learning model into a backend application
* Optimizing model loading through a **singleton inference engine**
* Working with relational databases and Django ORM
* Handling sensitive application data
* API throttling and request validation
* Separating ML inference from healthcare business logic
* Managing Python dependencies with Pipenv

---

## 🎯 Why a Modular Monolith?

For this project, a modular monolith was preferable to microservices because the application is relatively small and the AI inference engine is tightly coupled with the backend workflow.

Keeping the components within one Django deployment provides:

* Simpler development and deployment
* Lower operational complexity
* Fewer network boundaries
* Easier debugging
* Direct integration between API logic and ML inference

The internal module boundaries also leave room for individual components to be extracted into separate services later if the system grows.

---

## 🔮 Future Improvements

Potential improvements include:

* [ ] PostgreSQL support
* [ ] Dockerized development and deployment
* [ ] Background inference using Celery
* [ ] Redis for caching and task brokering
* [ ] Object storage for uploaded images
* [ ] Automated API tests
* [ ] CI/CD pipeline
* [ ] Production-grade logging and monitoring
* [ ] Model versioning and experiment tracking
* [ ] Improved model explainability
* [ ] Deployment with a production WSGI/ASGI server and reverse proxy
* [ ] Comprehensive audit logging

---

## ⚠️ Disclaimer

DermaAI is an **academic and engineering project** demonstrating the integration of Deep Learning with a Django-based healthcare platform.

AI predictions should **not be considered a medical diagnosis**. Users should consult qualified healthcare professionals for medical evaluation and treatment decisions.

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/AmazingFeature
git add .
git commit -m "Add AmazingFeature"
git push origin feature/AmazingFeature
```

Then open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
