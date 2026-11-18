# FinPilot – Test Plan and Test Report

**Project:** Smart Personal Finance & Expense Tracker with Budget Insights  
**Document Version:** 1.0  
**Date:** 18 November 2026  
**Testing Framework:** Pytest  
**API Testing:** HTTPX  
**SDLC Model:** Incremental Model

---

# Part A – Test Plan

## 1. Introduction

### 1.1 Purpose

This document defines the testing strategy, test environment, test types, and test results for FinPilot.

The objective is to verify that individual modules and their interactions work correctly and meet the requirements specified in the Software Requirements Specification.

### 1.2 Scope

Testing covers the backend components implemented in FinPilot, including:

- Authentication.
- User profile management.
- Database operations.
- Transaction management.
- Budget management.
- API validation and authorization.

Frontend and end-to-end testing will be documented separately after final integration and verification.

### 1.3 Testing Objectives

- Verify correctness of individual backend components.
- Verify interactions between API routes, services, and the database.
- Verify authentication and authorization.
- Verify data validation and integrity.
- Verify transaction and budget operations.
- Identify defects before final project delivery.

---

## 2. Testing Strategy

FinPilot follows a combination of unit testing and integration testing.

### 2.1 Unit Testing

Unit testing verifies individual functions or components independently.

The objective is to ensure that each tested unit produces the expected result for valid and invalid inputs.

### 2.2 Integration Testing

Integration testing verifies the interaction between multiple components.

In FinPilot, integration testing covers interactions among:

- FastAPI endpoints.
- Authentication dependencies.
- Service-layer logic.
- SQLAlchemy database operations.
- PostgreSQL test database.

### 2.3 Regression Testing

Regression testing is performed by rerunning the backend test suite after changes or new feature integrations.

This helps verify that existing functionality continues to work after new increments are added.

---

## 3. Test Environment

| Component | Configuration |
|---|---|
| Operating System | Windows |
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Testing Framework | Pytest |
| API Test Client | HTTPX |
| Database Migration Tool | Alembic |
| Development Environment | Visual Studio Code |

### 3.1 Test Database

A separate PostgreSQL test database, `finpilot_test_db`, is used for automated backend tests to isolate test data from the development database.

### 3.2 Test Execution Command

The backend tests are executed using:

```powershell
python -m pytest -q
```

---

## 4. Test Cases

The following are representative test scenarios covered by the backend test suite. The exact test names and assertions should be cross-checked against the test source files.

### 4.1 Authentication and User Management

| ID | Test Scenario | Expected Result |
|---|---|---|
| AUTH-01 | Register a new user | User is registered successfully |
| AUTH-02 | Register with invalid details | Validation error is returned |
| AUTH-03 | Login with valid credentials | Authentication succeeds |
| AUTH-04 | Login with invalid credentials | Authentication is rejected |
| AUTH-05 | Access protected API without authentication | Access is rejected |
| USER-01 | Retrieve authenticated user's profile | User profile is returned |
| USER-02 | Update supported profile information | Profile is updated |

### 4.2 Transaction Management

| ID | Test Scenario | Expected Result |
|---|---|---|
| TRANS-01 | Create an income transaction | Transaction is created |
| TRANS-02 | Create an expense transaction | Transaction is created |
| TRANS-03 | Retrieve user transactions | User's transactions are returned |
| TRANS-04 | Update a transaction | Transaction is updated |
| TRANS-05 | Delete a transaction | Transaction is deleted |
| TRANS-06 | Submit invalid transaction data | Validation error is returned |

### 4.3 Budget Management

| ID | Test Scenario | Expected Result |
|---|---|---|
| BUD-01 | Create a valid budget | Budget is created |
| BUD-02 | Create a duplicate budget | Duplicate is rejected |
| BUD-03 | Create a budget using an income category | Request is rejected |
| BUD-04 | Create a budget using an invalid category | Request is rejected |
| BUD-05 | List user budgets | User's budgets are returned |
| BUD-06 | Calculate budget spending progress | Spending values are calculated correctly |
| BUD-07 | Update an existing budget | Budget is updated |
| BUD-08 | Delete an existing budget | Budget is deleted |
| BUD-09 | Access another user's budget | Access is rejected |
| BUD-10 | Access budget API without authentication | Access is rejected |

---

## 5. Entry and Exit Criteria

### 5.1 Entry Criteria

Testing can begin when:

- The relevant module has been implemented.
- Dependencies are installed.
- Database configuration is available.
- The test database is accessible.
- Test cases are prepared.

### 5.2 Exit Criteria

A testing increment is considered complete when:

- All applicable test cases have been executed.
- No unresolved critical test failures remain.
- Relevant unit and integration tests pass.
- Results are recorded.

---

## 6. Defect Management

When a test fails:

1. Record the failure and its output.
2. Identify the affected module.
3. Investigate the cause.
4. Correct the implementation.
5. Rerun the relevant test.
6. Rerun the full suite to check for regressions.

---

# Part B – Test Report

## 7. Test Execution Summary

The complete backend test suite was executed after the Budget Management module was merged into the main branch.

### 7.1 Execution Details

**Command:**

```powershell
python -m pytest -q
```

**Observed Result:**

```text
........................................................ [ 93%]
....                                                     [100%]

60 passed, 1 warning in 27.48s
```

### 7.2 Test Summary

| Metric | Result |
|---|---:|
| Total tests passed | 60 |
| Failed tests | 0 |
| Warnings | 1 |
| Execution time | 27.48 seconds |
| Overall result | PASS |

### 7.3 Budget Integration Test Results

The budget module includes 10 integration tests covering:

- Budget creation.
- Duplicate budget prevention.
- Category validation.
- Budget listing.
- Spending calculations.
- Budget updates.
- Budget deletion.
- User-level access restrictions.
- Authentication requirements.

**Observed result:** 10 budget integration tests passed.

### 7.4 Warning Details

One deprecation warning was reported by Starlette concerning its use of HTTPX through `starlette.testclient`.

The warning did not cause any test failures. It should be reviewed during dependency maintenance.

---

## 8. Testing Conclusion

The backend test suite completed successfully with 60 passing tests and zero failures.

The result provides evidence that the tested backend modules and their tested integrations are functioning as expected in the configured test environment.

Further frontend integration and end-to-end testing are required to verify the complete application workflow.

---

## 9. Future Testing Activities

The following testing activities should be performed before final submission:

- Frontend component testing.
- Frontend-to-backend integration testing.
- Registration and login end-to-end testing.
- Profile update workflow verification.
- Transaction management through the user interface.
- Budget management through the user interface.
- Dashboard and analytics verification.
- CSV export verification, if implemented.
- Final regression testing.

---

**End of Test Plan and Test Report**
