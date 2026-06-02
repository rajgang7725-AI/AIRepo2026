

Generic Starting Point:
/bmad-help I am working on the WorkSync website. The BRD already defines business goals, functional requirements, and high-level constraints. The first phase is an MVP, and the immediate objective is to run the application locally in development environment only (no cloud deployment yet). Please guide me on the best way to start.

Phase 1 – Analysis (Marry)
/TR Perform a technical analysis of the BRD for the WorkSync website to identify architectural needs, constraints, and decision points for the MVP phase. The BRD is in the docs folder with the filename WorkSync-BRD.docx. You might ask for the technical stacks before finalizing 

Phase 2- Planning  (John)
/PRD Create PRD - Convert BRD into a clear, MVP-focused PRD. While doing so, identify ambiguities, assumptions, and missing or unclear requirements, and ask max 5 specific clarification questions. Do not finalize the PRD until those questions are answered. You might ask for the technical stacks before finalizing 


/VP validate the PRD document

Phase 3- Solutioning
/CA Use the PRD as the source of truth to create an MVP focused system architecture. Identify all areas requiring decisions or trade offs and ask for inputs wherever clarification is needed. Do not finalize the architecture until those inputs are provided.

/CE Decompose the approved MVP architecture into epics and user stories. Keep all items strictly within MVP scope and ask for clarification where requirements or flows are unclear before finalizing.

/IR Review the PRD, architecture, and user stories together to ensure consistent MVP scope, requirements, technical decisions, and user flows. Identify any gaps, mismatches, or contradictions across these artifacts. Clearly highlight what must be corrected or clarified before development begins.


Phase 4 – Implementation
/SP Use the finalized PRD, architecture, and user stories to create a detailed MVP sprint plan. Break work into actionable tasks with clear ownership, dependencies, and sequencing. Provide a step‑by‑step implementation plan aligned strictly to MVP scope for efficient execution.


/CS  Create all user stories for Epic 1 using the PRD and architecture as the source of truth. Write each story in a spec‑driven Given/When/Then format with clear acceptance criteria that is clear, unambiguous, and independently testable. Ensure all stories align strictly with the defined MVP scope.

/DS Implement Sprint 1 user stories step by step using the finalized PRD, architecture, and sprint plan. Break each story into a clear, actionable to do list and execute tasks sequentially. Surface blockers, assumptions, or required inputs immediately, and do not introduce scope beyond the MVP. Make sure to use DRY (Don’t repeat yourself) principle.

/CR Review Sprint 1 user stories.

Additional Skills

/GPC Generate Project context for the current project
Generate Project Context skill. Scan existing codebase to generate a lean LLM-optimized project-context.md.  LLM agents (Dev Story, Code review etc) don’t need to explore the repo from scratch each session; they oad one file and immediately understand the full project. 
It can be used any time in the lifecycle. Prefer to use it before /CS skill

//CC <Prompt>
Correct Course. Use this skill when something has gone off-track or requirements shift substantially. Like situations where Major scope changed in mid project, some architecture needs to be changed, PRD needs update etc.

//PM <Prompt>
Party Mode. Use this skill when you want to make more balanced and well-considered decisions through collaborative intelligence. Like you want to brainstorm complex scenarios where different expert viewpoints are needed. (e.g., architect + PM + security expert debating a design decision)