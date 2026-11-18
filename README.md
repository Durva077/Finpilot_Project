# Finpilot_Projec
# FinPilot – Smart Personal Finance & Expense Tracker

## 1. Project Overview

FinPilot is a web-based personal finance management application designed to help users record, organize, and monitor their income and expenses. It aims to provide users with a clear understanding of their spending habits and support better financial planning through budget monitoring and financial insights.

The project follows a client-server architecture with a React frontend, FastAPI backend, and PostgreSQL database.

## 2. Objectives

- Provide secure user registration and login.
- Allow users to manage personal profile information.
- Enable users to add, view, update, and delete financial transactions.
- Organize transactions using categories.
- Allow users to create and monitor budgets.
- Present financial summaries and insights.
- Support better personal financial management.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js, Vite |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database migrations | Alembic |
| Authentication | JWT |
| Password hashing | Argon2 |
| Testing | Pytest, HTTPX |
| Charts | Recharts |
| Version control | Git and GitHub |

## 4. System Architecture

FinPilot follows a three-layer client-server architecture:

1. **Presentation Layer:** React frontend provides the user interface.
2. **Application Layer:** FastAPI handles API requests, authentication, validation, and business logic.
3. **Data Layer:** PostgreSQL stores user, transaction, category, and budget information.

The frontend communicates with the backend through REST APIs. The backend interacts with PostgreSQL using SQLAlchemy.

## 5. Main Modules

- **Authentication Module:** User registration, login, and JWT-based authentication.
- **User Profile Module:** User profile information management.
- **Transaction Module:** Financial transaction management.
- **Budget Module:** Budget creation, monitoring, and spending calculations.
- **Dashboard and Analytics:** Financial summaries and visual representations.
- **Insights Module:** Spending observations and budget-related insights.

*Note: Dashboard, analytics, insights, and other frontend-dependent functionality should be marked as complete only after end-to-end verification.*

## 6. Project Structure

```text
Finpilot_Project/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docs/
│   ├── SRS.md
│   ├── Software_Design_Document.md
│   ├── UML_Diagrams.md
│   └── Test_Plan_and_Report.md
│
└── README.md
```

## 7. Requirements

Install the following before running the application:

- Python 3.10 or later
- Node.js and npm
- PostgreSQL
- Git

## 8. Backend Setup

Open a terminal and navigate to the backend directory:

```powershell
cd backend
```

Create a virtual environment if one does not already exist:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure the database connection using the environment variables required by the backend configuration. Do not commit passwords or secret keys to GitHub.

Run database migrations:

```powershell
alembic upgrade head
```

Start the backend server:

```powershell
uvicorn app.main:app --reload
```

Backend API documentation is available at:

`http://127.0.0.1:8000/docs`

## 9. Frontend Setup

Open another terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Open the local URL displayed in the terminal to access the application.

## 10. Testing

FinPilot uses Pytest for backend unit and integration testing.

Navigate to the backend directory and activate its virtual environment. Run:

```powershell
python -m pytest -q
```

**Latest recorded backend test result:**

- 60 tests passed
- 0 tests failed
- 1 non-blocking deprecation warning

The test suite includes authentication, database, transaction, and budget-related tests.

## 11. Software Development Life Cycle

The project follows the **Incremental Model**.

Development is divided into smaller increments. Each increment adds and integrates a set of related functionalities, allowing individual modules to be implemented and tested progressively.

## 12. Project Documentation

The following documents are available in the `docs/` directory:

- [Software Requirements Specification](docs/SRS.md)
- [Software Design Document](docs/Software_Design_Document.md)
- [UML Diagrams](docs/UML_Diagrams.md)
- [Test Plan and Test Report](docs/Test_Plan_and_Report.md)

## 13. Future Enhancements

- Advanced spending analytics.
- More detailed financial insights.
- Additional reporting and export options.
- Improved dashboard visualizations.
- Enhanced financial planning features.

## 14. Contributors
Durva Mhamal – Backend Development, Database Management, Testing, and Project Documentation.

Sunidhi Nagvekar – Frontend Development and Frontend–Backend Integration.
