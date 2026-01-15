# DermaAI: Intelligent Dermatological Diagnosis & Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![MySQL](https://img.shields.io/badge/Database-MySQL%208.0-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**DermaAI** is a secure, monolithic web platform designed to assist in the early detection of skin diseases using Deep Learning. It combines a high-performance **Convolutional Neural Network (CNN)** with a robust **Hospital Management System**, providing a seamless bridge between AI diagnosis and professional medical consultation.

---

## 🚀 Key Features

### 🧠 **AI-Powered Diagnostics**
* **Instant Analysis:** Uses a custom-trained **EfficientNetB0** model to classify skin lesions (e.g., Melanoma, Eczema, Benign) in under 200ms.
* **Singleton Inference Engine:** Custom-built model loader ensures the AI model is loaded into memory only once, optimizing RAM usage and response time.

### 🔒 **Enterprise-Grade Security**
* **HIPAA-Compliant Patterns:** Sensitive patient data (symptoms, history) is encrypted at rest using **AES-128 (Fernet)** via `django-cryptography`.
* **Stateless Authentication:** Secure API access using **JWT (JSON Web Tokens)** via `SimpleJWT`.
* **Role-Based Access Control (RBAC):** Distinct permissions for Patients, Doctors, and Administrators.

### 🏥 **Appointment Management**
* **Doctor Discovery:** Advanced filtering by specialty and location.
* **Secure Booking:** Encrypted appointment records ensuring patient privacy.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | Django 5 | Monolithic architecture for rapid development and unified security. |
| **API** | Django Rest Framework (DRF) | RESTful API design with scoped throttling. |
| **ML Engine** | TensorFlow / Keras | EfficientNet model execution on CPU. |
| **Database** | MySQL 8.0 | Relational storage for users, doctors, and encrypted appointments. |
| **Security** | Djoser + Cryptography | JWT Auth and Field-level encryption. |
| **Environment** | Pipenv | Deterministic dependency management. |

---

## 🏗️ System Architecture

The project follows a **Modular Monolith** pattern to balance simplicity with scalability:

```text
DermaAI_Solution/
├── ml_engine/        # The "Brain"
│   ├── predictor.py  # Singleton Logic for Model Loading & Inference
│   └── models/       # Versioned .h5 Files (Git-ignored)
├── web_app/          # The "Interface"
│   └── views.py      # Handles Image Uploads & API Throttling
├── appointments/     # The "Business Logic"
│   └── models.py     # Encrypted Patient Data Models
└── DermaAI_Project/  # Core Configuration
    └── settings.py   # JWT, Database, & Middleware Config

⚡ Installation & Setup
Follow these steps to run the project locally.

Prerequisites
Python 3.10+

MySQL Server

Git

1. Clone the Repository
git clone https://github.com/Spectre206/DermaAI.git
cd DermaAI

2. Install Dependencies
We use Pipenv for virtual environment management.
pip install pipenv
pipenv install
pipenv shell

3. Configure Database
Create a MySQL database and user.
CREATE DATABASE derma_ai_db;
CREATE USER 'derma_user'@'localhost' IDENTIFIED BY 'strongpassword123';
GRANT ALL PRIVILEGES ON derma_ai_db.* TO 'derma_user'@'localhost';
FLUSH PRIVILEGES;

4. Setup AI Model
Place your trained model file (e.g., skin_model_v1.h5) into ml_engine/models/.

Ensure the filename matches ACTIVE_MODEL_FILENAME in DermaAI_Project/settings.py.

Here is a professional, Portfolio-Grade README.md.

This document is designed to impress recruiters. It highlights not just what the app does, but the engineering decisions behind it (Security, Architecture, Scalability).

Action Plan
Create a file named README.md in your root folder (D:\DermaAI\README.md).

Paste the code below into it.

(Optional) Later, you can add screenshots of your app to the "Screenshots" section to make it pop.

Markdown

# DermaAI: Intelligent Dermatological Diagnosis & Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![MySQL](https://img.shields.io/badge/Database-MySQL%208.0-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**DermaAI** is a secure, monolithic web platform designed to assist in the early detection of skin diseases using Deep Learning. It combines a high-performance **Convolutional Neural Network (CNN)** with a robust **Hospital Management System**, providing a seamless bridge between AI diagnosis and professional medical consultation.

---

## 🚀 Key Features

### 🧠 **AI-Powered Diagnostics**
* **Instant Analysis:** Uses a custom-trained **EfficientNetB0** model to classify skin lesions (e.g., Melanoma, Eczema, Benign) in under 200ms.
* **Singleton Inference Engine:** Custom-built model loader ensures the AI model is loaded into memory only once, optimizing RAM usage and response time.

### 🔒 **Enterprise-Grade Security**
* **HIPAA-Compliant Patterns:** Sensitive patient data (symptoms, history) is encrypted at rest using **AES-128 (Fernet)** via `django-cryptography`.
* **Stateless Authentication:** Secure API access using **JWT (JSON Web Tokens)** via `SimpleJWT`.
* **Role-Based Access Control (RBAC):** Distinct permissions for Patients, Doctors, and Administrators.

### 🏥 **Appointment Management**
* **Doctor Discovery:** Advanced filtering by specialty and location.
* **Secure Booking:** Encrypted appointment records ensuring patient privacy.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | Django 5 | Monolithic architecture for rapid development and unified security. |
| **API** | Django Rest Framework (DRF) | RESTful API design with scoped throttling. |
| **ML Engine** | TensorFlow / Keras | EfficientNet model execution on CPU. |
| **Database** | MySQL 8.0 | Relational storage for users, doctors, and encrypted appointments. |
| **Security** | Djoser + Cryptography | JWT Auth and Field-level encryption. |
| **Environment** | Pipenv | Deterministic dependency management. |

---

## 🏗️ System Architecture

The project follows a **Modular Monolith** pattern to balance simplicity with scalability:

```text
DermaAI_Solution/
├── ml_engine/        # The "Brain"
│   ├── predictor.py  # Singleton Logic for Model Loading & Inference
│   └── models/       # Versioned .h5 Files (Git-ignored)
├── web_app/          # The "Interface"
│   └── views.py      # Handles Image Uploads & API Throttling
├── appointments/     # The "Business Logic"
│   └── models.py     # Encrypted Patient Data Models
└── DermaAI_Project/  # Core Configuration
    └── settings.py   # JWT, Database, & Middleware Config
⚡ Installation & Setup
Follow these steps to run the project locally.

Prerequisites
Python 3.10+

MySQL Server

Git

1. Clone the Repository
Bash

git clone [https://github.com/YourUsername/DermaAI.git](https://github.com/YourUsername/DermaAI.git)
cd DermaAI
2. Install Dependencies
We use Pipenv for virtual environment management.

Bash

pip install pipenv
pipenv install
pipenv shell
3. Configure Database
Create a MySQL database and user.

SQL

CREATE DATABASE derma_ai_db;
CREATE USER 'derma_user'@'localhost' IDENTIFIED BY 'strongpassword123';
GRANT ALL PRIVILEGES ON derma_ai_db.* TO 'derma_user'@'localhost';
FLUSH PRIVILEGES;
4. Setup AI Model
Place your trained model file (e.g., skin_model_v1.h5) into ml_engine/models/.

Ensure the filename matches ACTIVE_MODEL_FILENAME in DermaAI_Project/settings.py.

5. Run Migrations
python manage.py migrate

6. Start the Server
python manage.py runserver
Access the API at http://127.0.0.1:8000/.

🔌 API Documentation
Method,Endpoint,Description,Auth Required
POST,/auth/users/,Register a new user,❌ No
POST,/auth/jwt/create/,Login & Obtain Token,❌ No
POST,/api/predict/,Upload image for skin diagnosis,✅ Yes (Bearer)
GET,/api/doctors/,List available doctors,❌ No
POST,/api/book/,Book an appointment (Encrypted),✅ Yes (Bearer)

🛡️ Security Implementation Details
For interviewers and auditors:

Why Monolith? To eliminate network latency between the User Service and the AI Inference Engine, ensuring sub-second response times on free-tier hosting.

Why AES Encryption? Medical data is sensitive. Even if the database is leaked, the patient's specific symptoms and history remain unreadable without the Django SECRET_KEY.

🤝 Contributing
Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.

