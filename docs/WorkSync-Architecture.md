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
- The current tenant is stored in session and applied to all relevant queries.
- All shared models include a `tenant` foreign key to ensure isolation.
- Admin user creation and tenant onboarding are restricted to Admins or Django admin.

## 4. Core Architectural Components

### 4.1 Authentication & Authorization
- Use Django built-in authentication for login/logout and session management.
- Role-based access is required for Admin, Project Manager, Team Member, and Viewer.
- Decisions needed: implement access via Django Groups/Permissions, a custom `role` field on `TenantUser`, or a hybrid.

### 4.2 Project and Task Management
- Projects: name, description, start/end dates, status values, tenant association.
- Tasks: title, description, owner, status, estimated effort, actual effort, due date, project association.
- Task creation is limited to Admins and Project Managers.
- Team Members can update assigned tasks only.

### 4.3 Resource and Workload Management
- Weekly utilization is based on assigned hours vs fixed 40 hours/week available time.
- Over-allocation is defined as >100% utilization.
- Visual indicators should use green/yellow/red thresholds.
- Decisions needed: whether workload is derived from task assignments alone or also supported by explicit weekly allocation records.

### 4.4 Dashboard and Reporting
- Dashboard displays tenant-level metrics:
  - Project count by status
  - Task status distribution
  - Overdue tasks
  - Team utilization percentage
- Viewer users access the same dashboard in read-only mode.
- Chart.js renders the metric visualizations.

### 4.5 Data Persistence
- SQLite local DB for MVP.
- Schema should remain compatible with PostgreSQL later.
- Use Django migrations to manage schema evolution.

### 4.6 Local Development Considerations
- Application runs via `python manage.py runserver`.
- Use local Bootstrap assets and local Chart.js scripts.
- Use console-based or in-app notification placeholders.
- Use Django admin for tenant and user management.

## 5. Data Model Outline
The following core models are expected:
- `Tenant`
- `TenantUser` (links Django User to Tenant; role assignment)
- `Project`
- `Task`
- `ResourceAllocation` or equivalent for weekly workload tracking

## 6. Key Decisions and Tradeoffs

### 6.1 Tenant Isolation Model
- Chosen: context-based tenant isolation via middleware and session.
- Tradeoff: simpler for MVP; potential scaling concerns if tenant count grows significantly.
- Input needed: none, this is confirmed.

### 6.2 User Role Implementation
- Chosen: custom `role` field on `TenantUser`, combined with simple helper decorators for role checks.
- Tradeoff: simpler and faster for MVP than Django Groups.
- Input needed: none, this is confirmed.

### 6.3 Workload Modeling
- Chosen: explicit weekly allocation records (`ResourceAllocation`) in addition to task-based effort.
- Tradeoff: slightly more initial modeling but provides clearer workload planning and visualization.
- Input needed: none, this is confirmed.

### 6.4 Notification Handling
- Chosen: placeholder/in-app/console-only for MVP.
- Tradeoff: avoids delivery complexity; real notifications deferred.
- Input needed: none, this is confirmed.

### 6.5 Viewer Dashboard Scope
- Chosen: full tenant-level dashboard access read-only.
- Tradeoff: simplest implementation and aligns with stakeholder visibility needs.
- Input needed: none, this is confirmed.

### 6.6 Audit Logging
- Chosen: minimal audit logging for login events, project creation/update/deletion, and task creation/update/status changes.
- Tradeoff: lightweight and sufficient for MVP.
- Input needed: none, this is confirmed.

## 7. Architecture Finalization
The architecture decisions have been confirmed for MVP:
- Role enforcement uses a custom `role` field on `TenantUser` with helper decorators.
- Workload modeling includes explicit weekly `ResourceAllocation` records plus task-based effort.
- Viewer users have full tenant-level dashboard visibility in read-only mode.
- Audit logging includes login events and project/task create/update/delete/status changes.
- Django admin superusers can manage all tenants; tenant-level Admins are restricted to their tenant data in application views.

## 8. Next Step
The architecture is now ready for implementation-level design. The next phase is to translate this architecture into Django app design, data model definitions, and page/component mapping.