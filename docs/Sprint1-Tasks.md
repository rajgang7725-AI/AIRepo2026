# Sprint 1 — Core Platform: Granular Tasks & Prioritized Board

Estimate assumptions: 1 dev = 8 hours/day. Estimates are in hours.

Priority legend: P0 = must have in Sprint 1, P1 = important but can slip to next sprint.

## Sprint 1 Goal
Implement authentication, tenant model, login/session tenant flow, middleware, tenant Admin UI (minimal), and role enforcement decorators.

## Tasks (ticket-style)

### T1: Create `Tenant` and `TenantUser` models
- Owner: Dev
- Estimate: 8h
- Priority: P0
- Description: Implement models with fields:
  - `Tenant`: `name`, `created_at`
  - `TenantUser`: FK to `auth.User`, FK to `Tenant`, `role` (choices: ADMIN, PM, MEMBER, VIEWER), `is_active`
- Dependencies: Sprint 0 completed
- Acceptance: migrations created and models unit-tested

### T2: Configure Django auth and login flow
- Owner: Dev
- Estimate: 6h
- Priority: P0
- Description: Configure login/logout views and templates using Django auth. Ensure secure sessions.
- Acceptance: users can log in; unauthorized pages redirect to login

### T3: Implement session flow on login
- Owner: Dev
- Estimate: 4h
- Priority: P0
- Description: On successful login, set `request.session['tenant_id'] = TenantUser.tenant.id` (users single-tenant). If user has no TenantUser record, deny login with helpful message.
- Acceptance: session contains `tenant_id` and middleware can read it

### T4: Implement `TenantMiddleware`
- Owner: Dev
- Estimate: 6h
- Priority: P0
- Description: Middleware reads `request.session['tenant_id']`, loads `Tenant` and sets `request.tenant`. Rejects requests without valid tenant in session for protected pages.
- Dependencies: T1, T3
- Acceptance: `request.tenant` available in views; tenant-scoped queries use it

### T5: Implement role decorators (`@tenant_required`, `@role_required`)
- Owner: Dev
- Estimate: 6h
- Priority: P0
- Description: Create decorators to enforce tenant membership and role-based access. Raise `HttpResponseForbidden` for unauthorized access.
- Dependencies: T1, T4
- Acceptance: protected views enforce role checks in unit tests

### T6: Tenant Admin UI (minimal)
- Owner: Dev/FE
- Estimate: 12h
- Priority: P0
- Description: Build simple tenant Admin pages (list users within tenant, create/edit user with username/email, role, is_active). Use Bootstrap for forms.
- Dependencies: T1-T5
- Acceptance: Tenant Admin can create users and set roles; created users are linked to tenant

### T7: Superuser verification in Django admin
- Owner: Dev
- Estimate: 4h
- Priority: P0
- Description: Ensure superusers can create `Tenant` and initial Tenant Admin via Django admin. Add admin registrations for `Tenant` and `TenantUser`.
- Acceptance: superuser can create Tenant and TenantUser via admin and login as Tenant Admin

### T8: Basic tests (login, tenant middleware, user creation)
- Owner: QA/Dev
- Estimate: 8h
- Priority: P0
- Description: Unit tests for models, middleware behavior, and auth/session flow. Simple functional tests for Tenant Admin UI.
- Acceptance: Tests pass locally

## Prioritized Task Board (Markdown)

### To Do
- T1: Create `Tenant` and `TenantUser` models (P0)
- T2: Configure Django auth and login flow (P0)
- T3: Implement session flow on login (P0)
- T4: Implement `TenantMiddleware` (P0)
- T5: Implement role decorators (P0)
- T6: Tenant Admin UI (minimal) (P0)
- T7: Superuser verification in Django admin (P0)
- T8: Basic tests (P0)

### In Progress
- (move tasks here when work starts)

### Done
- (move tasks here when completed)

## Notes and Dependencies
- `T1` must complete before `T3` and `T4`.
- UI work (T6) can start once model migrations from `T1` are available; frontend templates can be scaffolded earlier.
- Tests (T8) should be written alongside implementations to avoid last-minute test debt.

## Estimates Summary
- Total estimated hours: 64h (approx. 8 developer-days)

## Next actions after Sprint 1
- Begin Sprint 2 tasks for Project and Task models and views once Sprint 1 acceptance criteria are met.
