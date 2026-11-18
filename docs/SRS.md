# Software Requirements Specification (SRS)

## FinPilot – Smart Personal Finance & Expense Tracker with Budget Insights

**Version:** 1.0  
**Date:** 18 November 2026  
**Project:** FinPilot  
**SDLC Model:** Incremental Model

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document defines the functional and non-functional requirements of FinPilot, a smart personal finance and expense tracking application.

It serves as a reference for developers, testers, project reviewers, and other stakeholders during software development, testing, and maintenance.

### 1.2 Scope

FinPilot is designed to help individuals manage their personal finances by recording income and expenses, organizing transactions into categories, setting monthly budgets, and monitoring spending.

The system follows a client-server architecture. Users interact with a React-based frontend, which communicates with a FastAPI backend. PostgreSQL is used for persistent data storage.

The planned system capabilities include:

- User registration and authentication.
- User profile management.
- Income and expense management.
- Transaction categorization.
- Monthly budget creation and monitoring.
- Dashboard and financial summaries.
- Spending analytics and visualizations.
- Financial insights and CSV export.

Features will be delivered incrementally. The implementation status of each feature will be verified against the final application.

### 1.3 Intended Audience

This document is intended for:

- Project developers.
- Software testers.
- Project guides and evaluators.
- Academic reviewers.
- Future maintainers of the application.

### 1.4 Definitions and Abbreviations

| Term | Description |
|---|---|
| SRS | Software Requirements Specification |
| API | Application Programming Interface |
| JWT | JSON Web Token |
| CRUD | Create, Read, Update and Delete |
| DBMS | Database Management System |
| UI | User Interface |
| SQL | Structured Query Language |
| SDLC | Software Development Life Cycle |

---

## 2. Overall Description

### 2.1 Product Perspective

FinPilot is a web-based application based on a three-layer architecture:

1. Presentation Layer – React frontend.
2. Application Layer – FastAPI backend containing APIs and business logic.
3. Data Layer – PostgreSQL database.

The frontend communicates with the backend through REST APIs. The backend validates requests, performs business operations, and interacts with the database.

### 2.2 Product Functions

The major functions of the system are:

- Registering and authenticating users.
- Managing user profile information.
- Recording income and expense transactions.
- Organizing transactions using categories.
- Creating monthly budgets.
- Calculating spending against budget limits.
- Displaying financial summaries and analytics.
- Providing financial insights and exporting data, where implemented.

### 2.3 User Classes

**Registered User**

A registered user can log in, manage their profile, create and manage transactions, and manage their personal budgets.

**Administrator / Project Maintainer**

The project maintainer is responsible for application configuration, database maintenance, deployment, and software updates. An administrator-facing application role is not assumed unless implemented.

### 2.4 Operating Environment

| Component | Technology |
|---|---|
| Frontend | React |
| Frontend build tool | Vite |
| Backend | Python with FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database migrations | Alembic |
| Authentication | JWT |
| Password hashing | Argon2 |
| Backend testing | Pytest |
| API testing | HTTPX |
| Data visualization | Recharts |

### 2.5 Design and Implementation Constraints

- The backend shall use FastAPI.
- The frontend shall use React.
- PostgreSQL shall be used for persistent storage.
- Passwords shall not be stored in plaintext.
- Protected operations shall require authentication.
- Users shall only access their own financial records.
- Backend business logic shall be separated into service modules.
- Database schema changes shall be managed through migrations.

### 2.6 Assumptions and Dependencies

- Users have access to a modern web browser.
- The application server and PostgreSQL database are available.
- Users provide valid information during registration and transaction creation.
- Frontend and backend services can communicate over HTTP.
- Required environment variables are configured before deployment.

---

## 3. Functional Requirements

### FR-01: User Registration

The system shall allow a new user to create an account by providing the required registration details.

The system shall validate registration data and prevent duplicate accounts according to the configured uniqueness rules.

### FR-02: User Authentication

The system shall allow registered users to log in using their credentials.

The system shall verify passwords securely and issue an authentication token after successful login.

Invalid credentials shall result in an appropriate error response.

### FR-03: User Profile Management

The system shall allow authenticated users to retrieve and update their profile information.

A user shall not be allowed to access another user's profile.

### FR-04: Transaction Management

The system shall allow authenticated users to:

- Create income transactions.
- Create expense transactions.
- View their transactions.
- Update existing transactions.
- Delete transactions.

The system shall validate transaction details before saving them.

### FR-05: Category Management

The system shall organize transactions using categories.

Transactions shall reference valid categories. Category type shall be considered when validating transaction or budget operations.

### FR-06: Budget Management

The system shall allow authenticated users to create monthly budgets for expense categories.

The system shall:

- Validate the budget amount.
- Validate the selected category.
- Prevent duplicate budgets for the same user, category, month, and year.
- Display the user's budgets.
- Allow budget updates and deletion.
- Restrict access to budgets belonging to the authenticated user.

### FR-07: Budget Monitoring

The system shall calculate the total expenses associated with a budget's category and month.

The system shall calculate:

- Total amount spent.
- Remaining budget.
- Percentage of budget used.
- Whether the budget has been exceeded.

### FR-08: Dashboard

The system shall provide a dashboard containing relevant financial summaries, subject to the implemented frontend and backend integration.

### FR-09: Analytics

The system shall support financial analysis through summaries and visual representations of transaction data, subject to implementation.

### FR-10: Financial Insights

The system may provide spending insights based on recorded financial activity. Such insights shall be based on available transaction and budget data.

### FR-11: CSV Export

The system may allow users to export their financial transaction data in CSV format, subject to implementation.

---

## 4. Non-Functional Requirements

### NFR-01: Security

- Passwords shall be hashed using a secure password-hashing mechanism.
- Authentication shall be required for protected APIs.
- JWT-based authentication shall be used.
- Users shall not be able to access other users' private financial records.

### NFR-02: Performance

The application should respond to normal user operations within an acceptable time under expected project demonstration workloads.

Database queries should avoid unnecessary data retrieval.

### NFR-03: Reliability

The system should validate user input and handle invalid requests without unexpected application crashes.

### NFR-04: Usability

The frontend should provide clear navigation, readable information, and understandable error messages.

### NFR-05: Maintainability

The application should use modular code organization.

API routes, schemas, database models, and business logic should be separated into appropriate modules.

### NFR-06: Testability

The backend should support automated unit and integration testing using Pytest and HTTPX.

### NFR-07: Data Integrity

The system shall maintain valid relationships between users, transactions, categories, and budgets using database constraints and application-level validation.

---

## 5. External Interface Requirements

### 5.1 User Interface

The React frontend shall provide interfaces for registration, login, profile management, transaction management, and budget management.

Additional screens shall be included as corresponding features are implemented.

### 5.2 Software Interface

The frontend shall communicate with the backend using REST API requests.

The backend shall communicate with PostgreSQL using SQLAlchemy.

### 5.3 Communication Interface

The system shall use HTTP-based communication between the frontend and backend during development. HTTPS should be configured for production deployment.

---

## 6. Data Requirements

The database shall store information required for user accounts and financial management.

The principal entities include:

| Entity | Purpose |
|---|---|
| User | Stores account and profile information |
| Category | Organizes income and expense records |
| Transaction | Stores financial transactions |
| Budget | Stores monthly category-wise budget limits |

Relationships:

- A user can own multiple transactions.
- A user can own multiple budgets.
- Transactions are associated with categories.
- Budgets are associated with expense categories.
- User-owned financial records must be isolated by user identity.

---

## 7. System Constraints

- The system requires a running PostgreSQL database.
- Backend API access depends on correct environment configuration.
- Database changes must be managed carefully through Alembic migrations.
- Protected endpoints require valid authentication.
- The frontend depends on the backend API for persistent financial data.

---

## 8. Acceptance Criteria

The system shall be considered acceptable when:

1. Users can register and authenticate successfully.
2. Protected APIs reject unauthenticated requests.
3. Users can perform supported transaction operations.
4. Users can create, retrieve, update, and delete budgets.
5. Budget calculations correctly reflect recorded expenses.
6. Users cannot access another user's protected financial records.
7. Automated unit and integration tests pass.
8. Frontend and backend integration works for the implemented features.
9. Required software documentation is completed and consistent with the delivered application.

---

## 9. Software Development Life Cycle Model

### 9.1 Selected Model: Incremental Model

FinPilot follows the Incremental Software Development Life Cycle Model.

The application is developed and delivered in smaller functional increments. Each increment adds a set of related features to the existing system.

### 9.2 Planned Increments

| Increment | Main Deliverables |
|---|---|
| Increment 1 | Project foundation, database and backend setup |
| Increment 2 | Authentication and user profile |
| Increment 3 | Transaction management |
| Increment 4 | Budget management and spending calculations |
| Increment 5 | Frontend integration and remaining financial features |
| Increment 6 | Testing, documentation and final integration |

### 9.3 Benefits of the Selected Model

- Enables gradual feature development.
- Supports testing after each increment.
- Makes integration issues easier to identify.
- Allows modules to be developed and verified independently.
- Supports continuous improvement of the application.

---

## 10. Future Enhancements

Possible future enhancements include:

- Recurring transactions.
- Advanced spending recommendations.
- Multiple account support.
- Improved financial reports.
- Data backup and restoration.
- Notifications for budget thresholds.

These enhancements are not considered implemented unless verified in the final application.

---

**End of Software Requirements Specification**
