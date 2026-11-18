# FinPilot – UML Diagrams

**Project:** Smart Personal Finance & Expense Tracker with Budget Insights  
**Version:** 1.0  
**SDLC Model:** Incremental Model

---

## 1. Use Case Diagram

This diagram represents the interactions between a registered user and the FinPilot system.

```mermaid
flowchart LR
    User([Registered User])

    subgraph FinPilot["FinPilot System"]
        UC1([Register])
        UC2([Login])
        UC3([View Profile])
        UC4([Update Profile])
        UC5([Manage Transactions])
        UC6([Manage Categories])
        UC7([Manage Budgets])
        UC8([View Budget Progress])
        UC9([View Dashboard])
        UC10([View Analytics])
        UC11([Export Transactions])
        UC12([View Financial Insights])
    end

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
    User --> UC10
    User --> UC11
    User --> UC12
```

**Explanation:** The registered user interacts with the system to manage personal financial information. Some use cases depend on features being completed in the final application.

---

## 2. Class Diagram

This diagram shows the main data entities and their relationships.

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string hashed_password
        +string full_name
        +string phone_number
    }

    class Category {
        +int id
        +string name
        +string category_type
        +int user_id
        +bool is_default
    }

    class Transaction {
        +int id
        +int user_id
        +int category_id
        +decimal amount
        +string transaction_type
        +date transaction_date
        +string description
    }

    class Budget {
        +int id
        +int user_id
        +int category_id
        +decimal amount
        +int month
        +int year
    }

    User "1" --> "0..*" Transaction : owns
    User "1" --> "0..*" Budget : creates
    Category "1" --> "0..*" Transaction : classifies
    Category "1" --> "0..*" Budget : assigned to
```

**Explanation:** A user can own multiple transactions and budgets. Categories classify transactions and are used to define budgets.

---

## 3. Activity Diagram – User Authentication

```mermaid
flowchart TD
    A([Start]) --> B[Open Login Page]
    B --> C[Enter Email and Password]
    C --> D[Submit Login Request]
    D --> E{Credentials Valid?}
    E -- No --> F[Display Error Message]
    F --> C
    E -- Yes --> G[Generate Authentication Token]
    G --> H[Open User Dashboard]
    H --> I([End])
```

**Explanation:** The user enters login credentials. The backend validates the credentials and provides an authentication token when login succeeds.

---

## 4. Activity Diagram – Transaction Management

```mermaid
flowchart TD
    A([Start]) --> B[Open Transaction Page]
    B --> C[Choose Transaction Operation]
    C --> D{Operation}
    D --> E[Create Transaction]
    D --> F[View Transactions]
    D --> G[Update Transaction]
    D --> H[Delete Transaction]
    E --> I[Validate Transaction Data]
    G --> I
    I --> J{Data Valid?}
    J -- No --> K[Display Validation Error]
    K --> B
    J -- Yes --> L[Save Changes to Database]
    F --> M[Retrieve User Transactions]
    H --> N[Delete Selected Transaction]
    L --> O[Display Updated Information]
    M --> O
    N --> O
    O --> P([End])
```

**Explanation:** Users can create, view, update, or delete transactions. The system validates submitted information before saving changes.

---

## 5. Component Diagram

This diagram shows the major software components and their dependencies.

```mermaid
flowchart TB
    User([User])

    subgraph Frontend["Frontend - React + Vite"]
        Pages[Application Pages]
        Components[Reusable UI Components]
        APIClient[API Client]
    end

    subgraph Backend["Backend - FastAPI"]
        Routes[API Routes]
        Auth[Authentication Module]
        Schemas[Pydantic Schemas]
        Services[Service Layer]
        Models[SQLAlchemy Models]
    end

    subgraph Database["PostgreSQL Database"]
        UserTable[(Users)]
        CategoryTable[(Categories)]
        TransactionTable[(Transactions)]
        BudgetTable[(Budgets)]
    end

    User --> Pages
    Pages --> Components
    Components --> APIClient
    APIClient --> Routes
    Routes --> Auth
    Routes --> Schemas
    Routes --> Services
    Services --> Models
    Models --> UserTable
    Models --> CategoryTable
    Models --> TransactionTable
    Models --> BudgetTable
```

**Explanation:** The frontend sends requests to backend API routes. The backend uses authentication, schemas, services, and SQLAlchemy models to process operations and communicate with PostgreSQL.

---

## 6. Sequence Diagram – Budget Creation

```mermaid
sequenceDiagram
    actor User
    participant UI as React Frontend
    participant API as FastAPI
    participant Service as Budget Service
    participant DB as PostgreSQL

    User->>UI: Enter budget details
    UI->>API: POST budget request
    API->>API: Verify authentication
    API->>Service: Validate budget
    Service->>DB: Check category and duplicate
    DB-->>Service: Validation result
    Service->>DB: Save budget
    DB-->>Service: Saved budget
    Service-->>API: Budget response
    API-->>UI: Return response
    UI-->>User: Display created budget
```

**Explanation:** The budget is validated, stored, and returned to the frontend after the request is authenticated.

---

## 7. Sequence Diagram – Budget Spending Calculation

```mermaid
sequenceDiagram
    actor User
    participant UI as React Frontend
    participant API as FastAPI
    participant Service as Budget Service
    participant DB as PostgreSQL

    User->>UI: Request budget progress
    UI->>API: GET budget details
    API->>Service: Retrieve budget
    Service->>DB: Fetch budget and expenses
    DB-->>Service: Budget and expense records
    Service->>Service: Calculate spent amount
    Service->>Service: Calculate remaining amount
    Service->>Service: Calculate percentage used
    Service-->>API: Return budget progress
    API-->>UI: Return progress response
    UI-->>User: Display budget status
```

**Explanation:** The budget service calculates spending progress using the expenses associated with the budget's category and period.

---

## 8. Diagram Summary

| Diagram | Purpose |
|---|---|
| Use Case Diagram | Shows user interactions with the system |
| Class Diagram | Shows entities and relationships |
| Activity Diagram – Authentication | Describes the login workflow |
| Activity Diagram – Transactions | Describes transaction operations |
| Component Diagram | Shows the application architecture |
| Sequence Diagram – Budget Creation | Shows budget creation interactions |
| Sequence Diagram – Budget Progress | Shows spending calculation interactions |

---

**Note:** These diagrams represent the intended logical design. Before final submission, verify class attributes, API operations, and frontend use cases against the final source code. Features not yet implemented should be labelled as planned rather than completed.

**End of UML Diagrams**
