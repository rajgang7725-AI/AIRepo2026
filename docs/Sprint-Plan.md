# WorkSync MVP Sprint Plan

Overview
- Goal: Implement the WorkSync MVP per finalized PRD and architecture.
- Team roles (example):
  - Developer (Dev) — implements backend, views, templates
  - Frontend/UX (FE) — Bootstrap templates, Chart.js integration
  - QA / Tester (QA) — acceptance and functional tests
  - Project Lead (PL) — reviews PRD, acceptance, coordinates

Sprint cadence (recommended)
- 2-week sprints; adjust based on team size. The plan below assumes a single small team (2 developers + 1 QA).

Sprint 0 (Prep, 2-3 days)
- Tasks:
  - Create repository structure and `requirements.txt` (Dev)
  - Initialize Django project `worksync` and `apps/` folders (Dev)
  - Add `settings.DEFAULT_WEEKLY_HOURS = 40` to settings template (Dev)
  - Set up `.env.local` sample and dev instructions in README (Dev)
  - Configure logging and placeholder `AuditLog` model (Dev)
- Acceptance:
  - `python manage.py runserver` starts; SQLite DB migrated; README has setup steps.

Sprint 1 — Core Platform & Tenant (2 weeks)
- Objective: Authentication, tenant model, middleware, role enforcement, tenant admin UI baseline
- Tasks:
  1. Models: Create `Tenant`, `TenantUser` (user FK, tenant FK, `role`, `is_active`) and migrations (Dev)
  2. Auth: Configure Django auth, login/logout templates, and create superuser workflow (Dev)
  3. Middleware: Implement `TenantMiddleware` that reads `request.session['tenant_id']` and sets `request.tenant` (Dev)
  4. Session flow: On login set `request.session['tenant_id'] = TenantUser.tenant.id`; implement single-tenant enforcement (Dev)
  5. Role decorators: Implement `@role_required` and `@tenant_required` decorators (Dev)
  6. Tenant Admin UI: Minimal tenant Admin pages (create/edit user with username/email, role, is_active) (FE/Dev)
  7. Superuser: Verify Django admin allows superusers to create Tenants and initial Tenant Admins (Dev)
  8. QA: Basic tests for login, tenant middleware, and user creation (QA)
- Dependencies: Sprint 0 setup
- Acceptance Criteria:
  - Users can log in; session tenant_id set; middleware enforces tenant scope
  - Tenant Admin UI allows creating tenant-scoped users and assigning roles
  - Superuser can create Tenants via Django admin

Sprint 2 — Projects & Tasks (2 weeks)
- Objective: Implement Project and Task CRUD, task assignment, role-restricted creation
- Tasks:
  1. Models: `Project` (tenant FK, name, description, start/end, status)
  2. Models: `Task` (project FK, tenant FK, title, description, owner FK, status, estimated_hours, actual_hours, due_date)
  3. Views/Forms: Project create/edit/list/detail templates using Bootstrap (FE/Dev)
  4. Views/Forms: Task create/edit/list/detail templates; enforce task creation only for Admin and Project Manager via decorators (FE/Dev)
  5. Business rules: Task overdue flag, task visibility for assigned users (Dev)
  6. QA: Tests for project create, task create/assign/update, overdue identification (QA)
- Dependencies: Sprint 1 complete (middleware, role decorators)
- Acceptance Criteria:
  - Admin/PMs can create projects and tasks; Team Members see assigned tasks and can update status/actual hours
  - Overdue tasks are flagged on listing and detail pages

Sprint 3 — ResourceAllocation & Dashboard (2 weeks)
- Objective: Implement `ResourceAllocation`, utilization calculations, and dashboard charts
- Tasks:
  1. Model: `ResourceAllocation` (tenant FK, user FK, week_start, allocated_hours, notes)
  2. Services: Utilization calculation service (utilization = allocated_hours / DEFAULT_WEEKLY_HOURS) and over-allocation detection
  3. Views: Create allocation UI (create/list/edit) for Admin/PM (FE/Dev)
  4. Dashboard: Server-side aggregated endpoints providing JSON for Chart.js (Dev/FE)
  5. Charts: Implement Chart.js visualizations for project count by status, task distribution, overdue items, and utilization (FE)
  6. QA: Tests for allocation creation and utilization math, dashboard rendering (QA)
- Dependencies: Sprint 1 & 2 complete
- Acceptance Criteria:
  - Allocations can be created and compute utilization correctly; >100% flagged
  - Dashboard displays all four core metrics and renders charts successfully

Sprint 4 — Audit Logging, Tests, Polish, and Docs (1-2 weeks)
- Objective: Finalize audit logging, acceptance tests, styling polish, README and local deployment instructions
- Tasks:
  1. Implement `AuditLog` model and wire it to record key events (login, project create/update/delete, task create/update/status) (Dev)
  2. Wire Django logging to file/console and capture the same events (Dev)
  3. Complete automated tests: unit tests for models/services and functional tests for the critical UI flows (QA/Dev)
  4. UI polish: responsive layouts, error messages, and form validation (FE/Dev)
  5. Documentation: finalize `README.md`, `docs/` entries, and developer setup instructions (PL/Dev)
  6. Final acceptance run: smoke test the full flow end-to-end (Dev/QA)
- Acceptance Criteria:
  - Key audit events are logged; tests pass; README and setup are validated; app runs locally end-to-end

Implementation sequencing and ownership notes
- Sequence: Sprint 0 -> Sprint 1 -> Sprint 2 -> Sprint 3 -> Sprint 4
- Ownership: label tasks with (Dev), (FE), (QA), (PL). Adjust to actual team members.
- Parallelization: Frontend template work and backend services can be parallelized once models are defined in Sprint 1.

Dependencies and blockers
- Blockers: Tenant middleware and role decorators must be implemented early (Sprint 1) before tenant-scoped data objects are used.
- Database: SQLite is used for MVP; migrations must be maintained for compatibility with PostgreSQL later.

Acceptance tests (minimum)
- Login flow (tenant-scoped)
- Project create/edit/delete
- Task create/assign/update and overdue flagging
- ResourceAllocation create and utilization calculation
- Dashboard rendering of the four core metrics

Deliverables per sprint
- Sprint 0: Repo skeleton, settings, README, migrations
- Sprint 1: Auth, Tenant, middleware, tenant admin UI, role decorators, basic tests
- Sprint 2: Project & Task CRUD, assignment, permissions, overdue logic
- Sprint 3: ResourceAllocation, utilization service, dashboard charts
- Sprint 4: AuditLog, logging, automated tests, docs, polish

Rollout checklist for local demo
- Run migrations
- Create superuser
- Create Tenant + Tenant Admin via Django admin
- Create tenant users and seed data (projects, tasks, allocations)
- Run `python manage.py runserver` and verify dashboard

Estimated timeline (single small team)
- Sprint 0: 3 days
- Sprint 1: 10 working days
- Sprint 2: 10 working days
- Sprint 3: 10 working days
- Sprint 4: 5-8 working days

Optional follow-ups (post-MVP)
- PostgreSQL migration and multi-server deployment
- Per-user available hours and tenant settings
- Email/in-app notifications delivery
- Soft-delete and audit UI

# End of Sprint Plan
