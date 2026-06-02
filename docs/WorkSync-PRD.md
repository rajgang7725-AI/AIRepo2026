# WorkSync Product Requirements Document (PRD)

## 1. Executive Summary
WorkSync is a multi-tenant project and resource management platform. The MVP focuses on local development only and uses Django templates, Bootstrap, Chart.js, Django auth, SQLite for local data, and a modular monolith architecture. The MVP validates core tenant-based project/task management, role-based dashboards, and weekly utilization tracking.

## 2. MVP Objectives
- Provide a tenant-isolated application for multiple organizations.
- Enable role-based access for Admin, Project Manager, Team Member, and Viewer.
- Support project and task management with status tracking.
- Provide a dashboard for core metrics: project status, task distribution, overdue items, and team utilization.
- Keep deployment local and use SQLite for initial development.

## 3. Scope
### In Scope
- Tenant-aware Django application
- User authentication and role-based authorization
- Project CRUD
- Task CRUD and status updates
- Resource workload tracking on a weekly basis
- Dashboard visualizations with Chart.js
- Bootstrap-based responsive UI
- Local development support only (no cloud deployment)

### Out of Scope
- Mobile applications
- Billing, invoicing, or subscription management
- External integrations (Jira, Slack, email providers, etc.)
- Advanced analytics or AI forecasting
- Production deployment or cloud infrastructure

## 4. User Roles and Permissions
### Admin
- Manage tenant users and roles
- Create/edit/delete projects and tasks
- Manage resource allocations
- Access full tenant dashboard and reports

### Project Manager
- Create and manage projects
- Create and assign tasks to team members
- View workload and utilization reports
- Edit project/task metadata within the tenant

### Team Member
- View tasks assigned to them
- Update task status and actual effort
- View personal workload and utilization

### Viewer
- View read-only tenant dashboards
- Review project progress and utilization metrics

## 5. Core Features
### Authentication
- Django built-in authentication
- Role-based access via Groups or a custom `role` field on tenant user relationships
- Tenant context determined via middleware and stored in session

### Project Management
- Project entity with name, description, start/end dates, status values, and tenant association
- Project list and detail views
- Project forms using Bootstrap

### Task Management
- Task entity with title, description, owner, status, estimated effort, actual effort, due date, and project association
- Task assignment to users
- Task status transitions and effort updates

### Resource and Workload Management
- Weekly allocation data for team members
- Utilization calculations based on assigned hours and available hours
- Over-allocation defined as >100% utilization
- Visual indicators: green/yellow/red

### Dashboard and Reporting
- Tenant-level dashboard with:
  - Project count by status
  - Task status distribution
  - Overdue task summary
  - Team utilization percentage
- Chart.js visualizations embedded in Django templates

## 6. Architecture
- Django modular monolith with apps per domain area: tenants, users, projects, resources, dashboard
- Middleware enforces tenant context on each request
- SQLite for local development; PostgreSQL planned for future staging/production
- Use Django admin for quick data management during MVP

## 7. Data Model Summary
- Tenant
- TenantUser (links Django User to Tenant + role)
- Project
- Task
- ResourceAllocation or similar workload model

## 8. Non-functional Requirements
- Local dev ease: simple `manage.py runserver` setup
- Response times acceptable for demo-level usage
- Basic audit logging for key actions
- Minimal security for tenant isolation and auth

## 9. Confirmed Technical Decisions (MVP)
The following technical decisions are approved for the MVP and must be implemented as documented:

1. Tenant creation / onboarding
- Only superusers (developer/platform admin) create `Tenant` records via Django admin and create the initial Tenant Admin. No tenant self-registration or onboarding flows are in MVP.

2. Multi-tenant user membership
- Users are single-tenant only in MVP. Do not support multi-tenant membership or tenant selection after login.

3. Role implementation and task creation
- Role enforcement uses a custom `role` field on `TenantUser` combined with lightweight helper decorators for access checks.
- Task creation is limited to `Admin` and `Project Manager` roles. `Team Member` can only update assigned task status and actual effort.

4. Available hours
- For MVP, available hours are a global constant: `settings.DEFAULT_WEEKLY_HOURS = 40`. This is not configurable per-tenant or per-user in MVP.

5. ResourceAllocation semantics
- Utilization is computed only from `ResourceAllocation.allocated_hours`. Task effort may be displayed for reference, but is not authoritative for allocation or utilization calculations.

6. Deletion semantics
- For MVP, use cascade delete: deleting a `Project` cascades to delete its `Task` records. Soft-delete strategies are deferred for a future phase.

7. Audit logging
- Backend logging plus a minimal `AuditLog` model will record key events: login events; project create/update/delete; task create/update/status changes. No audit UI is required for MVP.

8. Session tenant enforcement
- Users are single-tenant. On login set `request.session['tenant_id'] = TenantUser.tenant.id` and middleware must use this value to filter tenant-scoped queries.

9. Tenant Admin UI scope
- Tenant Admin UI in the application will support minimal user management fields: username/email, `TenantUser.role`, and active status. No invites or password reset flows in MVP.

10. Tests and acceptance criteria
- The MVP requires acceptance tests for critical flows: login, project create, task create/assign/update, resource allocation create, and dashboard view.

## 10. Remediation and Next Steps
- Update implementation plans, data models, and middleware to reflect the confirmed decisions above.
- Add the `DEFAULT_WEEKLY_HOURS` constant to the Django settings and document how to change it in the future.
- Implement a minimal `AuditLog` model and configure Django logging to capture the specified events.

## 11. Validation Summary
- The PRD now explicitly captures the approved MVP decisions for tenant onboarding, role enforcement, allocation semantics, deletion behavior, audit logging, and testing scope.
- These clarifications remove ambiguity and align the PRD with the architecture and epics for implementation.

## 12. Final Note
- The PRD is finalized for MVP implementation planning; any future scope changes must be recorded as backlog items and approved by stakeholders.
