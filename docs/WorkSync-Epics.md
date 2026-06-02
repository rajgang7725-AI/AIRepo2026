# WorkSync MVP Epics and User Stories

This document decomposes the approved WorkSync MVP architecture into epics and user stories. All items remain strictly within the local MVP scope.

## Epic 1: Tenant and User Management

### Story 1.1: Tenant Admin Login
- As a tenant Admin, I want to log in to the WorkSync application so that I can manage my tenant.
- Acceptance: login page uses Django auth and establishes tenant context in session.

### Story 1.2: Tenant User Management
- As a tenant Admin, I want to create and manage tenant users so that I can assign team members and viewers.
- Acceptance: Admin can create users, assign them to the tenant, and set their `TenantUser.role`.

### Story 1.3: Tenant User Role Editing
- As a tenant Admin, I want to update a user’s role so that permissions reflect the correct responsibilities.
- Acceptance: Admin can change a user’s role between Admin, Project Manager, Team Member, and Viewer.

### Story 1.4: Superuser Tenant Administration
- As a Django superuser, I want to manage all tenants and users in Django admin so that local development and testing remain simple.
- Acceptance: superusers can view and modify all tenant data in admin; tenant-level Admin users remain scoped in application views.

## Epic 2: Authentication and Role-based Access

### Story 2.1: Login and Logout
- As any user, I want to log in and log out so that my session is secure and tenant-scoped.
- Acceptance: Django login/logout works; unauthorized users cannot access protected pages.

### Story 2.2: Tenant Context Enforcement
- As a user, I want all application queries to respect my tenant context so that I only see my tenant’s data.
- Acceptance: middleware resolves tenant from session and filters tenant-scoped queries.

### Story 2.3: Role-based Page Access
- As a user, I want page access to be restricted according to my tenant role so that I only perform allowed actions.
- Acceptance: custom role decorators enforce access for Admin, Project Manager, Team Member, and Viewer.

## Epic 3: Project Management

### Story 3.1: Create Project
- As an Admin or Project Manager, I want to create a project so that work can be tracked for the tenant.
- Acceptance: form captures project name, description, start/end dates, and status; project is tenant-scoped.

### Story 3.2: Edit Project
- As an Admin or Project Manager, I want to edit a project so that project details remain up to date.
- Acceptance: project details can be updated and saved within tenant scope.

### Story 3.3: List and View Projects
- As any authorized user, I want to see a list of tenant projects and view project details so that I can understand current work.
- Acceptance: project list is tenant-scoped; project detail page shows status and associated tasks.

### Story 3.4: Delete Project
- As an Admin, I want to delete a project so that obsolete or cancelled work can be removed.
- Acceptance: delete action removes project and associated tenant-scoped data.

## Epic 4: Task Management

### Story 4.1: Create Task
- As an Admin or Project Manager, I want to create tasks under a project so that work can be assigned.
- Acceptance: task form captures title, description, owner, status, estimated effort, actual effort, due date, and project association.

### Story 4.2: Assign Task
- As an Admin or Project Manager, I want to assign a task to a team member so they know what to work on.
- Acceptance: task owner field selects a tenant user and saves assignment.

### Story 4.3: Update Task Status and Effort
- As a Team Member, I want to update the status and actual effort of my assigned tasks so that progress is tracked.
- Acceptance: assigned users can update task status and actual effort, but cannot create tasks.

### Story 4.4: Task Visibility
- As a Team Member, I want to see tasks assigned to me and related project details so that I can focus on my work.
- Acceptance: task list shows assigned tasks; tenant users only see permitted tasks.

### Story 4.5: Overdue Task Identification
- As any authorized user, I want overdue tasks to be clearly identified so that I can prioritize them.
- Acceptance: tasks past due date and not complete are flagged as overdue.

## Epic 5: Resource and Workload Management

### Story 5.1: Create Weekly Resource Allocation
- As an Admin or Project Manager, I want to create weekly resource allocation records so that workload planning is explicit.
- Acceptance: allocations store user, week range, allocated hours, and (optionally) linked task context.

### Story 5.2: Compute Utilization
- As an Admin or Project Manager, I want utilization calculated from assigned hours and a fixed 40-hour week so that I can see workload capacity.
- Acceptance: system computes utilization = assigned hours / 40 and marks >100% as over-allocated.

### Story 5.3: View Utilization by Team Member
- As an Admin or Project Manager, I want to view team utilization percentages so that I can identify overloads.
- Acceptance: utilization view shows each team member’s weekly utilization with green/yellow/red indicators.

### Story 5.4: View Personal Utilization
- As a Team Member, I want to see my own utilization summary so that I understand my workload.
- Acceptance: personal workload view shows assigned hours, utilization percentage, and over-allocation warnings.

## Epic 6: Dashboard and Reporting

### Story 6.1: Tenant Dashboard Metrics
- As any authorized user, I want a tenant dashboard showing project counts, task distribution, overdue tasks, and utilization so that I can assess current status.
- Acceptance: dashboard displays the four core metrics and updates for the tenant.

### Story 6.2: Chart Visualization
- As any authorized user, I want charts for dashboard metrics so that information is easy to consume.
- Acceptance: Chart.js renders the dashboard charts in Django templates.

### Story 6.3: Viewer Dashboard Access
- As a Viewer, I want full read-only access to the tenant dashboard so that I can review stakeholder metrics.
- Acceptance: Viewer sees the same dashboard metrics and charts without edit controls.

## Epic 7: Non-functional MVP Support

### Story 7.1: Local Development Setup
- As a developer, I want to run the application locally with SQLite so that I can develop and test without cloud dependencies.
- Acceptance: application starts with `python manage.py runserver`, uses SQLite, and requires no cloud infrastructure.

### Story 7.2: Minimal Audit Logging
- As a tenant Admin, I want key actions logged so that I can track login and project/task changes.
- Acceptance: login events and project/task create/update/delete/status changes are recorded.

### Story 7.3: Notification Placeholders
- As a user, I want notification placeholders so that I can see where alerts would appear in the application.
- Acceptance: notification UI placeholders exist and console-based events can be logged; no email delivery is required.

## Clarifications Resolved
The following clarification items were confirmed for MVP:

1. Tenant-level Admin user management: Implement tenant-level Admin user create/edit/role assignment in the application UI for the MVP; Django admin remains available for superusers/developers during local development.

2. ResourceAllocation linkage: Weekly `ResourceAllocation` records are independent planned allocations by user/week; no explicit linkage to tasks is required for MVP (optional task context may be added later).

3. Audit logging visibility: Backend storage/logging is sufficient for MVP; no application-facing audit log view is required. Key events logged: login, project create/update/delete, and task create/update/status changes.

## Next Step
With clarifications resolved, this story breakdown is finalized for the MVP. Proceed to create the implementation plan and map stories to development tasks.
