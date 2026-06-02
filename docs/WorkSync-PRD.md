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

## 9. Assumptions and Ambiguities
### Assumptions
- Tenant isolation is handled by middleware and session-based tenant context.
- Available hours are a fixed standard of 40 hours/week per user for MVP.
- Overdue tasks are based on due date plus incomplete status.
- Notifications are MVP-light: console/in-app placeholders only, with no real email delivery.
- Tenant records are created only by Admin users or via Django admin in MVP.

### Resolved Decisions
- Tenant onboarding is Admin-only for MVP; no self-registration.
- Available hours are fixed at 40 hours/week per user.
- Task creation is limited to Admins and Project Managers.
- Viewer users see the full tenant-level dashboard in read-only mode.
- Notifications are placeholder-only; no live email delivery in MVP.

## 10. Clarification Answers
1. Tenant records are created only by Admin users or through Django admin; no self-registration in MVP.
2. Utilization uses a fixed standard of 40 hours/week per user.
3. Task creation is limited to Admins and Project Managers only.
4. Viewer users see the full tenant-level dashboard in read-only mode.
5. MVP notifications are placeholder-only, using simple in-app or console-based behavior.

## 11. Next Steps
- Finalize the PRD and use it as the basis for implementation planning.
- Define a detailed MVP implementation plan and user journey mapping based on the confirmed PRD.
- Create a local development setup checklist for Django and SQLite.

## 12. Validation Summary
- The PRD aligns with the BRD by preserving core MVP goals, tenant isolation, role-based access, and dashboard metrics.
- The selected stack is explicitly captured: Django templates, Bootstrap, Chart.js, Django auth, SQLite local dev, modular monolith.
- Ambiguities were resolved with confirmed decisions for tenant onboarding, standard weekly availability, task creation roles, read-only viewer dashboards, and placeholder notifications.
- The document is now finalized for MVP implementation planning.
