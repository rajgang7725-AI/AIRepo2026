# WorkSync MVP System Architecture (Draft)

## 1. Purpose
This document defines the MVP-focused system architecture for WorkSync using the PRD as the source of truth. It describes the key components, data flow, architectural boundaries, and areas that require additional input before finalization.

## 2. System Overview
WorkSync is a modular monolith built on Django for local development only. The application supports multi-tenant project and resource management with role-based access, dashboards, and weekly utilization tracking.

### Selected stack
- Frontend: Django templates + Bootstrap + Chart.js
- Backend: Django
- Database: SQLite for local MVP, PostgreSQL later
- Authentication: Django auth with role-based access
- Architecture: Modular monolith
- Deployment: Local development only

## 3. High-level Architecture

### 3.1 Application Layers
- **Presentation layer**: Django templates render UI pages using Bootstrap for layout and Chart.js for dashboard charts.
- **Application layer**: Django views and forms handle requests, enforce permissions, and coordinate business logic.
- **Domain layer**: Django models represent Tenant, TenantUser, Project, Task, and workload entities.
- **Data access layer**: Django ORM persists data to SQLite, with tenant filtering enforced through middleware and model managers.

### 3.2 Django App Structure
The application should be split into domain-specific Django apps:
- `tenants` — tenant records, onboarding, tenant context
- `users` — user profiles, user-tenant relationships, roles
- `projects` — project CRUD and project logic
- `tasks` — task CRUD, assignment, status, effort tracking
- `resources` — workload data, utilization calculations
- `dashboard` — aggregated metrics and chart data
- `common` — shared decorators, middleware, utilities

### 3.3 Tenant Context and Isolation
- Tenant context is resolved via middleware on each request.
- Users are single-tenant in MVP; do not support multi-tenant membership or tenant selection.
- On login, the application must set `request.session['tenant_id'] = TenantUser.tenant.id` and middleware must use this value to scope queries.
- All shared models include a `tenant` foreign key to ensure isolation.
- Tenant records are created only by superusers via Django admin; superusers also create the initial Tenant Admin. No tenant self-registration in MVP.

## 4. Core Architectural Components

### 4.1 Authentication & Authorization
- Use Django built-in authentication for login/logout and session management.
- Role enforcement uses a custom `role` field on `TenantUser`, combined with helper decorators to check roles (Admin, Project Manager, Team Member, Viewer).
- `TenantUser` is the canonical mapping between `auth.User` and a single `Tenant` including a `role` field and `is_active` flag.

### 4.2 Project and Task Management
- Projects: name, description, start/end dates, status values, and tenant association.
- Tasks: title, description, owner (tenant user), status, estimated effort (informational), actual effort, due date, and project association.
- Task creation is limited to `Admin` and `Project Manager` roles; `Team Member` may update only assigned task status and actual effort.

### 4.3 Resource and Workload Management
- Weekly utilization is based on explicit `ResourceAllocation.allocated_hours` and a global constant `settings.DEFAULT_WEEKLY_HOURS = 40`.
- Over-allocation is defined as utilization > 100%.
- `ResourceAllocation` records are independent planned allocations by user/week for MVP; optional task context may be added later but is not required.
- Display task effort as reference only; do not use task effort as the authoritative allocation source for utilization.

### 4.4 Dashboard and Reporting
- Dashboard displays tenant-level metrics:
  - Project count by status
  - Task status distribution
  - Overdue tasks
  - Team utilization percentage
- Viewer users access the full tenant dashboard in read-only mode; no widgets are hidden in MVP.
- Chart.js renders the metric visualizations embedded in Django templates.

### 4.5 Data Persistence
- SQLite local DB for MVP. Schema must remain compatible with PostgreSQL for future migration.
- Use Django migrations to manage schema evolution.

### 4.6 Local Development Considerations
- Application runs via `python manage.py runserver`.
- Use local Bootstrap assets and Chart.js scripts.
- Notification placeholders (UI + console logging) are sufficient in MVP.
- Use Django admin for superusers to manage tenants and initial tenant admins; tenant-level Admin UI exists for minimal user management.

## 5. Data Model Outline
Core models for MVP:
- `Tenant`
- `TenantUser` (links Django `auth.User` to `Tenant`, contains `role` and `is_active`)
- `Project`
- `Task`
- `ResourceAllocation` (week_start, user, allocated_hours, notes)
- `AuditLog` (minimal model to store key events)

## 6. Key Decisions and Tradeoffs

### 6.1 Tenant Isolation Model
- Chosen: context-based tenant isolation via middleware and session. Simpler for MVP; scale limitations documented.

### 6.2 User Role Implementation
- Chosen: custom `role` field on `TenantUser` with helper decorators for enforcement. Simpler and faster for MVP.

### 6.3 Workload Modeling
- Chosen: explicit weekly `ResourceAllocation` records are the authoritative source for utilization. Task effort is informational.

### 6.4 Notification Handling
- Chosen: placeholder/in-app/console-only for MVP. Real delivery deferred.

### 6.5 Viewer Dashboard Scope
- Chosen: full tenant-level dashboard read-only for Viewers.

### 6.6 Audit Logging
- Chosen: minimal audit logging for login events and project/task create/update/delete/status changes. Implement `AuditLog` table plus standard Django logging to file/console.

### 6.7 Deletion Semantics
- Chosen: cascade delete for `Project` -> `Task` in MVP. Soft-delete is deferred to future work.

## 7. Architecture Finalization
The architecture decisions have been confirmed for MVP and are recorded here to guide implementation.

## 8. Session Tenant Enforcement and Flow
- Users are single-tenant in MVP.
- On successful login set `request.session['tenant_id'] = TenantUser.tenant.id`.
- `TenantMiddleware` reads `request.session['tenant_id']` and sets `request.tenant` for use by views and model managers. All tenant-scoped queries must filter by `tenant`.

## 9. Audit Logging and Deletion Semantics
- Implement a minimal `AuditLog` model with fields: `id`, `tenant`, `user`, `event_type`, `object_type`, `object_id`, `timestamp`, and `details` (JSON/text).
- Configure Django logging to write key events to console/file and optionally write structured audit rows to the `AuditLog` model.
- Deletion: deleting a `Project` cascades to its `Task` records; `ResourceAllocation` records are independent and not cascaded unless explicitly linked.

## 10. Tenant Admin UI Scope
- Tenant Admin UI supports minimal user management (username/email, `role`, `is_active`) and basic user list/filtering within tenant scope. No invite or password-reset flows in MVP.

## 11. Testing Expectations
- Add acceptance tests for critical flows: login (tenant-scoped), project create/edit/delete, task create/assign/update, resource allocation create, and dashboard rendering.
- Prefer Django unit tests for models/services and simple functional tests for key UI flows.

## 12. Next Step
Translate this architecture into implementation-level designs: Django app skeleton, model definitions (with fields and constraints), middleware, decorators, views, templates, and automated tests.
