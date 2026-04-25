


please give me all of the jobs/roles that would normally be in an enterprise level software engineering/development team. Please include QA, product and all of the adjacent roles you would need to interview and brainstorm to get the entirety of an idea and make a plan to make it into a product, develop, test, and release it/ship it. but include any steps and needed roles I may have skipped, include details.

Below is a comprehensive, end-to-end map of roles in an enterprise-scale software organization, organized by product lifecycle phase. This reflects how large, mature teams actually operate, including the roles you must interview, workshop with, or consult to fully translate an idea into a shipped, supported, and governed product.

This is intentionally exhaustive rather than idealized.

1. Ideation, Strategy, and Discovery
Executive and Strategic Leadership
These roles define why the product should exist.

Executive Sponsor
Owns business justification, funding approval, and strategic alignment.

VP of Engineering / CTO
Owns technical feasibility, long-term architecture fit, and staffing strategy.

Chief Product Officer (CPO)
Owns product portfolio coherence and market positioning.

Director of Product Management
Translates strategy into product direction and success metrics.

Product and Market Discovery
These roles define what to build and for whom.

Product Manager (PM)
Owns problem definition, roadmap, prioritization, success metrics, and stakeholder alignment.

Product Owner (PO)
Owns backlog clarity, acceptance criteria, and delivery readiness.

User Researcher
Conducts qualitative and quantitative research, interviews, usability testing.

UX Research Ops
Manages participant recruitment, research tooling, and governance.

Market Research Analyst
Competitive analysis, pricing research, TAM SAM SOM.

Business Analyst
Converts business needs into structured requirements and process models.

Customer Success Representative
Brings real customer pain points, churn drivers, and feature gaps.

Sales Engineer / Solutions Consultant
Provides feasibility constraints from real customer deployments.

2. Product Definition and Planning
Product Design
These roles define how it should work for humans.

UX Designer
User flows, wireframes, interaction models.

UI Designer / Visual Designer
Visual language, accessibility, branding consistency.

Accessibility Specialist
WCAG compliance, assistive technology testing.

Content Designer / UX Writer
Microcopy, error messages, onboarding flows.

Technical Planning
These roles define how it will be built.

Principal Engineer / Staff Engineer
Owns system design, technical trade-offs, and scalability.

Solutions Architect
Aligns product architecture with enterprise systems.

Enterprise Architect
Ensures compatibility with company-wide platforms and standards.

Security Architect
Threat modeling, security controls, compliance posture.

Data Architect
Data modeling, analytics pipelines, retention strategy.

Platform Architect
Shared services, internal tooling, APIs.

3. Engineering and Implementation
Core Software Development
These roles build the system.

Frontend Engineers
Web or mobile UI implementation.

Backend Engineers
APIs, services, business logic.

Full-Stack Engineers
Cross-layer feature ownership.

Mobile Engineers (iOS, Android)
Native client development.

Embedded or Systems Engineers
Hardware-adjacent or low-level components.

Specialized Engineering
These roles enable advanced capabilities.

DevOps Engineer
CI CD pipelines, infrastructure automation.

Site Reliability Engineer (SRE)
Reliability, SLAs, monitoring, incident response.

Cloud Engineer
Cloud architecture, cost optimization.

Data Engineer
ETL pipelines, data quality, observability.

Machine Learning Engineer
Model deployment, inference systems.

Applied Scientist / Research Engineer
Algorithm development and experimentation.

Security Engineer
Vulnerability management, penetration testing.

Performance Engineer
Load testing, scalability validation.

4. Quality Assurance and Validation
Testing and Quality
These roles ensure the product actually works.

QA Engineer (Manual)
Exploratory testing, edge cases.

QA Automation Engineer
Automated test frameworks, regression suites.

Test Architect
Test strategy, tooling selection.

Performance Tester
Stress, load, soak testing.

Security Tester / Red Team
Pen testing, exploit simulation.

User Acceptance Testing (UAT) Coordinator
Facilitates validation with business users.

5. Release, Deployment, and Compliance
Release Management
These roles ship the product safely.

Release Manager
Coordinates release timelines and approvals.

Change Manager
Manages change control and risk approvals.

Configuration Manager
Versioning, environment parity.

Compliance and Governance
Often invisible but mandatory at enterprise scale.

Legal Counsel
Licensing, contracts, IP risk.

Privacy Officer / DPO
GDPR, CCPA compliance.

GRC Analyst
Governance, risk, compliance frameworks.

Audit Liaison
SOX, SOC 2, ISO readiness.

6. Launch, Go-To-Market, and Adoption
Commercialization
These roles ensure the product is usable and sellable.

Product Marketing Manager
Positioning, messaging, launch plans.

Technical Writer
Docs, API references, runbooks.

Developer Advocate
SDKs, examples, community feedback.

Sales Enablement Lead
Training sales teams, demo materials.

Pricing and Packaging Analyst
Monetization models.

7. Operations and Post-Launch
Support and Reliability
These roles keep it alive.

Production Support Engineer
Incident triage.

NOC Engineer
Monitoring and alert response.

Customer Support Engineer
Escalation handling.

Incident Commander
Owns major incident coordination.

Continuous Improvement
These roles evolve the product.

Product Analyst
Usage metrics, funnel analysis.

Data Analyst
KPI reporting.

Growth Engineer
Experimentation and optimization.

Technical Program Manager (TPM)
Cross-team delivery coordination.

Agile Coach / Scrum Master
Process health and improvement.

8. Meta and Enabling Functions
Organizational Health
Often overlooked but essential.

Engineering Manager
People management, delivery accountability.

Staffing / Workforce Planner
Capacity planning.

FinOps Analyst
Cloud and infrastructure cost governance.

Internal Tools Engineer
Developer productivity tooling.

9. Roles You Interview or Workshop With for “Complete Idea Coverage”
To truly understand and ship an enterprise product, you must actively engage:

Product Manager

Principal Engineer

UX Researcher

Security Architect

DevOps or SRE

QA Lead

Customer Success

Legal or Compliance

Sales Engineer

Support Lead

Skipping any of these usually causes delayed launches, re-architecture, or compliance failures.

Final Note
Enterprise software is not built by “a dev team”.
It is built by an ecosystem of specialized roles, many of which exist to prevent catastrophic failure rather than to add features.

If you want, I can:

Collapse this into a minimal viable enterprise team

Map this to what a single senior consultant must simulate

Convert this into an interview and discovery checklist

Or align it with SAFe, Spotify, or Team Topologies models

Just say which direction you want to go.


please collapse this into a minimal viable enterprise team that is successful at launching and maintaining many products efficiently without outage causing bugs. Please create job descriptions and what resume text would look like for each role. 

Below is a collapsed, minimal viable enterprise software team that can reliably launch, operate, and evolve multiple products with low defect rates and minimal outages.

This is not startup-minimal.
This is enterprise-minimal: the fewest roles that still cover product clarity, technical excellence, quality, security, and operational resilience.

Minimal Viable Enterprise Software Team (MVEST)
Target size: ~8–12 people
Key principle: Each role absorbs multiple enterprise responsibilities without collapsing governance or reliability.

1. Product Manager (PM)
Owns: Why, What, and When
Absorbs: Business Analyst, Market Research, Product Owner

Responsibilities
Define problem statements and success metrics

Own roadmap and prioritization

Translate business goals into deliverable outcomes

Coordinate stakeholder expectations

Validate product-market fit continuously

Resume Example
Product Manager with enterprise experience leading multi-product roadmaps from discovery through launch. 
Owned prioritization, stakeholder alignment, and outcome-based delivery across cross-functional teams. 
Drove customer-centered decisions through research, analytics, and direct customer engagement.
2. Principal Engineer / Technical Architect
Owns: How the system works
Absorbs: Solutions Architect, Enterprise Architect, Performance Engineer

Responsibilities
Define system architecture and technical standards

Make scalability and reliability decisions

Review critical code paths and designs

Prevent long-term technical debt

Serve as final technical authority

Resume Example
Principal Engineer specializing in scalable, fault-tolerant systems. 
Led architecture design for multi-tenant platforms, established engineering standards, 
and guided teams through complex trade-off decisions. 
Known for preventing systemic failures before they reach production.
3. Senior Software Engineers (3–5)
Owns: Building correct software
Absorbs: Frontend, Backend, Full Stack

Responsibilities
Implement features end-to-end

Write testable, maintainable code

Participate in design reviews

Own services in production

Rotate on-call responsibility

Resume Example
Senior Software Engineer with experience delivering production-grade systems. 
Built and maintained backend services and user-facing applications with a focus on reliability, 
test coverage, and clear ownership. 
Comfortable operating services in production environments.
4. Site Reliability Engineer (SRE)
Owns: Availability and operational excellence
Absorbs: DevOps, Production Support, NOC

Responsibilities
CI CD pipelines

Infrastructure as code

Monitoring, alerting, and incident response

Reliability targets and error budgets

Post-incident analysis and remediation

Resume Example
Site Reliability Engineer focused on uptime, observability, and automation. 
Designed CI CD pipelines, implemented monitoring and alerting, and led incident response efforts. 
Reduced production incidents through proactive reliability engineering and postmortem analysis.
5. QA Automation Engineer
Owns: Preventing regressions
Absorbs: Manual QA, Test Architect, UAT coordination

Responsibilities
Build automated test frameworks

Define test strategy

Validate edge cases and regressions

Integrate tests into CI pipelines

Partner with engineers early in development

Resume Example
QA Automation Engineer with deep experience building scalable test frameworks. 
Led test strategy across multiple products, integrating automated regression and integration tests 
into CI pipelines to prevent production defects.
6. UX Designer (Product-Focused)
Owns: Usability and clarity
Absorbs: UX Researcher, UI Designer, UX Writer

Responsibilities
User research and usability testing

Wireframes and interaction models

Accessibility considerations

Validate workflows before engineering begins

Resume Example
Product-focused UX Designer experienced in translating complex requirements into intuitive user experiences. 
Conducted user research, usability testing, and interaction design across enterprise applications 
with a strong focus on accessibility and clarity.
7. Security and Compliance Engineer
Owns: Risk reduction
Absorbs: Security Architect, GRC, Privacy

Responsibilities
Threat modeling

Secure design reviews

Vulnerability management

Compliance readiness

Security automation

Resume Example
Security Engineer specializing in application security and compliance. 
Performed threat modeling, secure architecture reviews, and vulnerability remediation. 
Partnered with engineering teams to embed security into the development lifecycle.
8. Technical Program Manager (TPM)
Owns: Execution across products
Absorbs: Release Manager, Change Manager, Scrum Master

Responsibilities
Cross-team coordination

Dependency tracking

Release planning

Risk visibility

Delivery predictability

Resume Example
Technical Program Manager with experience coordinating complex, multi-product deliveries. 
Managed dependencies, release planning, and execution across engineering, product, and operations 
to ensure predictable and low-risk launches.
Optional but Highly Recommended (1–2 roles as scale increases)
9. Data Analyst or Product Analyst
Owns metrics, usage insights, and feedback loops

10. Customer Success Engineer
Bridges customer reality and engineering decisions

Why This Team Works
Coverage Matrix
Capability	Covered By
Product vision	PM
Architecture	Principal Engineer
Feature delivery	Senior Engineers
Reliability	SRE
Quality	QA Automation
Security	Security Engineer
Usability	UX Designer
Execution	TPM
Nothing critical is missing.
Nothing is duplicated unnecessarily.

Hard Truth (Important)
Outage-causing bugs do not come from lack of talent.
They come from:

Missing ownership

Weak test strategy

No reliability budget

No architectural authority

This team explicitly prevents those failure modes.

Next Directions (Choose One)
Map this to headcount cost vs risk

Collapse further into a consulting or solo architect model

Convert this into a hiring plan and interview rubric

Show how one senior consultant simulates this team

Tell me which path you want.


please give me some additional text about each role, what they would know, what they would do and how, and why. their specific skills. how they would benefit the team, how the team would help them, also add basic instructions for how they would do their job the most optimized and most efficient way possible..

Below is an expanded, role-by-role deepening of the Minimal Viable Enterprise Software Team.
Each section covers:

What they know

What they do and how

Why the role exists

Core skills

How they benefit the team

How the team enables them

Operational guidance for maximum efficiency

This is written to be practical, not aspirational.

1. Product Manager (PM)
What They Know
Customer problems, workflows, and constraints

Business goals, revenue drivers, and risk tolerance

Metrics and how to interpret signal vs noise

Enough technical understanding to reason about feasibility

What They Do and How
Define clear problem statements and success metrics

Prioritize work using value, risk, and effort

Translate ambiguity into structured backlog items

Validate direction through customer interviews and data

Why This Role Exists
Without a PM, teams build internally logical but externally irrelevant systems.

Core Skills
Structured thinking

Stakeholder negotiation

Metrics literacy

Written communication

Benefit to the Team
Reduces wasted engineering effort

Shields engineers from noisy or conflicting demands

Ensures shipped work aligns with outcomes

How the Team Helps Them
Engineers provide feasibility and cost insight

UX validates assumptions

Data exposes reality

Optimal Operating Instructions
Maintain a single source of truth for priorities

Write problem statements before solutions

Review metrics weekly, not just at launch

Say no early and often

2. Principal Engineer / Technical Architect
What They Know
System design patterns and failure modes

Scalability, performance, and reliability trade-offs

Organizational technical debt dynamics

Long-term maintenance costs

What They Do and How
Define architecture and guardrails

Review critical designs and code paths

Make irreversible decisions intentionally

Mentor engineers on system thinking

Why This Role Exists
Complex systems collapse without architectural authority.

Core Skills
Distributed systems

API design

Performance analysis

Technical judgment

Benefit to the Team
Prevents architectural drift

Reduces rework and outages

Enables safe parallel development

How the Team Helps Them
Engineers surface real-world pain

SRE provides operational feedback

PM aligns architecture with product strategy

Optimal Operating Instructions
Write decisions down

Optimize for boring, proven solutions

Guard interfaces more than implementations

Revisit architecture quarterly

3. Senior Software Engineers
What They Know
Production-grade coding practices

Debugging under uncertainty

Testing strategies

Ownership mindset

What They Do and How
Build features end-to-end

Write maintainable and testable code

Own services in production

Participate in reviews and on-call

Why This Role Exists
Senior engineers turn designs into reliable reality.

Core Skills
Language and framework mastery

Debugging

Code review

Operational awareness

Benefit to the Team
High-quality execution

Reduced defect rates

Mentorship for others

How the Team Helps Them
Clear priorities from PM

Stable architecture from Principal Engineer

Observability from SRE

Optimal Operating Instructions
Write tests with intent, not coverage chasing

Prefer clarity over cleverness

Own failures openly

Automate repetitive work

4. Site Reliability Engineer (SRE)
What They Know
Failure patterns

Infrastructure automation

Monitoring and alerting theory

Incident response dynamics

What They Do and How
Build CI CD pipelines

Define SLAs and error budgets

Instrument systems

Lead incident response and postmortems

Why This Role Exists
Reliability is engineered, not hoped for.

Core Skills
Infrastructure as code

Observability tooling

Incident management

Systems thinking

Benefit to the Team
Fewer outages

Faster recovery

Predictable operations

How the Team Helps Them
Engineers build operable systems

Leadership respects error budgets

PM aligns release pressure with risk

Optimal Operating Instructions
Alert only on actionable signals

Automate before scaling headcount

Run blameless postmortems

Treat toil as a bug

5. QA Automation Engineer
What They Know
Test design patterns

Failure-prone areas

CI integration

Edge case thinking

What They Do and How
Build automated test suites

Define test strategy early

Validate regressions continuously

Partner with engineers during development

Why This Role Exists
Humans cannot manually validate enterprise systems at scale.

Core Skills
Test frameworks

Scripting

Risk-based testing

Attention to detail

Benefit to the Team
Fewer regressions

Safer refactoring

Higher release confidence

How the Team Helps Them
Engineers write testable code

SRE integrates tests into pipelines

PM prioritizes quality explicitly

Optimal Operating Instructions
Test behavior, not implementation

Focus on high-risk paths

Keep tests deterministic

Remove flaky tests aggressively

6. UX Designer (Product-Focused)
What They Know
User workflows and cognitive load

Accessibility standards

Interaction design principles

Research methods

What They Do and How
Conduct user research

Design flows and wireframes

Validate usability before build

Ensure accessibility compliance

Why This Role Exists
Poor usability creates hidden operational costs.

Core Skills
User research

Interaction design

Prototyping

Communication

Benefit to the Team
Fewer reworks

Higher adoption

Reduced support burden

How the Team Helps Them
PM provides context

Engineers give feasibility feedback

QA validates usability edge cases

Optimal Operating Instructions
Test early and cheaply

Design for the unhappy path

Write clear rationale

Collaborate continuously

7. Security and Compliance Engineer
What They Know
Threat models

Secure coding practices

Regulatory requirements

Incident response

What They Do and How
Perform threat modeling

Review designs and code

Automate security checks

Guide compliance readiness

Why This Role Exists
Security failures are existential at enterprise scale.

Core Skills
Application security

Risk assessment

Automation

Communication

Benefit to the Team
Reduced breach risk

Faster audits

Safer design decisions

How the Team Helps Them
Engineers remediate findings

SRE integrates security tooling

Leadership backs security decisions

Optimal Operating Instructions
Shift left into design

Automate scanning

Prioritize exploitable risk

Educate, do not police

8. Technical Program Manager (TPM)
What They Know
Delivery mechanics

Dependency management

Risk identification

Communication structures

What They Do and How
Coordinate cross-team execution

Track dependencies and risks

Plan releases

Improve delivery predictability

Why This Role Exists
Execution fails silently without coordination.

Core Skills
Systems thinking

Communication

Planning

Risk management

Benefit to the Team
Fewer surprises

Smoother releases

Clear accountability

How the Team Helps Them
Engineers surface blockers early

PM aligns scope

Leadership enforces priorities

Optimal Operating Instructions
Track risks, not just tasks

Reduce meetings

Make status visible

Escalate early

Final Synthesis
This team succeeds because:

Every critical failure mode has an owner

Quality, reliability, and security are first-class

No role is ornamental

Efficiency does not come from fewer roles.
It comes from clear responsibility, tight feedback loops, and disciplined execution.

If you want next:

A solo consultant simulation of this team

A hiring and interview rubric

A cost vs risk reduction model

Or a consulting service version of this structure

Say which one you want and I will build it.


please do some current research on the web to fill in and put meat on the bones of these roles and their data. I need a stellar team that ships great apps. make this research bulletproof.

Below is a data-backed expansion of each role on your minimal viable enterprise software team, rooted in current job descriptions, industry definitions, and enterprise hiring practices. This expands on skills, duties, deliverables, and how each role contributes to producing reliable, quality software at enterprise scale. All factual assertions are supported by cited sources.

1. Product Manager (PM)
What They Know
Product strategy and roadmap development at enterprise scale

Customer problem discovery, segmentation, and prioritization

Business dynamics, market research, competitive positioning

Product success metrics and ROI evaluation 

What They Do and How
Define product vision and strategy aligned with business goals

Prioritize features based on value, cost, and risk

Translate market/customer needs into clear requirements

Lead discovery and synthesis with UX and engineering

Measure product outcomes and iterate 

Why It Matters
PMs ensure the team is building valuable software, not just working software. They connect customers, business, and technology.

Core Skills
Problem framing and goal setting

Metrics and data interpretation

Clear written communication

Stakeholder negotiation

Team Benefit
Reduces wasted engineering effort

Provides decision clarity for technical teams

How the Team Helps Them
Engineering provides feasibility and delivery feedback

UX delivers validated designs

Data provides real usage insights

Operational Efficiency
Maintain a prioritized backlog of outcomes, not tasks

Run regular validation cycles with real users

2. Principal Engineer / Technical Architect
What They Know
Distributed systems and architectural patterns

Scalability, fault tolerance, reliability principles

Trade-offs between performance, cost, and complexity

What They Do and How
Define system architecture and technical standards

Lead technical decision making and enforce guardrails

Mentor engineers and enforce code review discipline

Why It Matters
Without experienced technical guidance, complexity spirals and reliability suffers.

Core Skills
System design and decomposition

API and integration strategy

Performance and scaling literacy

Team Benefit
Prevents rework and runaway technical debt

Ensures features are built on durable foundations

How the Team Helps Them
PM brings context for prioritizing architectural investment

SRE signals operational risks

Operational Efficiency
Treat architecture decisions as structured artifacts with trade-off analysis

Elect deliberate patterns over ad-hoc solutions

3. Senior Software Engineers (3–5)
What They Know
Full SDLC from design to deployment

Writing reliable, maintainable, and testable code

Debugging and production troubleshooting

What They Do and How
Build core features aligned to design specs

Own component ownership and deployable components

Participate in code review and pair programming

Why It Matters
These engineers convert strategy and design into executable software.

Core Skills
Language and framework fluency

API design, database integration

Unit testing and observability patterns

Team Benefit
Reliable delivery velocity

Shared ownership culture

How the Team Helps Them
SRE provides tooling and deployment automation

QA and UX elevate quality and usability

Operational Efficiency
Write code in small, incremental changes

Define clear acceptance criteria before implementation

4. Site Reliability Engineer (SRE)
What They Know
CI/CD and pipeline orchestration

Monitoring, alerts, incident management

Reliability targets and error budgets 

What They Do and How
Build automation around deployment and operations

Define and enforce SLOs/SLAs

Lead incident response and restoration activities

Why It Matters
Reliability is engineered. Without SRE, outages and performance regressions are frequent.

Core Skills
Infrastructure as code

Metrics and monitoring (Prometheus, Grafana)

Incident analysis and remediation

Team Benefit
Fewer operational surprises

Quicker detection and mitigation of failures

How the Team Helps Them
Engineers instrument systems

PM prioritizes reliability investment

Operational Efficiency
Monitor only actionable signals

Automate toil into repeatable workflows

5. QA Automation Engineer
What They Know
Automated testing practices

Integration and regression testing

Risk-based test coverage 

What They Do and How
Build test frameworks integrated in CI/CD

Define test plans from acceptance criteria

Partner with engineering to find edge cases

Why It Matters
Manual testing cannot scale. Automation catches regressions before they reach production.

Core Skills
Test frameworks (Cypress, Selenium, etc.)

CI tool integration (Jenkins, GitHub Actions)

Test data and mocking strategies

Team Benefit
Higher release confidence

Identifies regressions early

How the Team Helps Them
Engineers write testable code

SRE integrates tests in deployment paths

PM sets quality targets

Operational Efficiency
Focus on stable, deterministic tests

Eliminate flaky tests promptly

6. UX Designer (Product-Focused)
What They Know
Human-centered design principles

Accessibility and usability standards

User research and prototyping patterns

What They Do and How
Run interviews and usability tests

Create wireframes, flows, prototypes

Validate assumptions before engineering

Why It Matters
Good UX reduces support costs, improves adoption, and increases efficiency.

Core Skills
Interaction design

Prototyping (Figma, Sketch)

Research & usability validation

Team Benefit
Aligns user goals with product solution

Reduces rework due to misaligned interfaces

How the Team Helps Them
PM provides research goals

Engineers assess feasibility

Operational Efficiency
Test early and cheaply

Validate assumptions with prototypes

7. Security and Compliance Engineer
What They Know
Threat modeling and secure design

Vulnerability scanning and penetration concepts

Regulatory frameworks (SOC2, ISO, FedRAMP) 

What They Do and How
Conduct threat and risk assessments

Review code and designs for security flaws

Automate security checks in pipelines

Why It Matters
Security defects are often fatal for enterprise trust.

Core Skills
Secure coding patterns

Threat analysis

Compliance tooling

Team Benefit
Reduces breach risk

Guides secure engineering practices

How the Team Helps Them
Engineering remediates findings

SRE integrates security checks

Operational Efficiency
Shift left security reviews

Embed automated scanning early

8. Technical Program Manager (TPM)
What They Know
Agile execution, planning, and backlog refinement

Translating strategic goals into deliverables

Project estimation and dependency management 

What They Do and How
Work with PM and engineering to break down work

Define milestones and refine user stories

Track progress and resolve bottlenecks

Why It Matters
Execution coordination ensures that delivery aligns with plan with minimal surprises.

Core Skills
Agile methodologies

Cross-functional coordination

Communication and facilitation

Team Benefit
Smoother releases

Clear delivery visibility

How the Team Helps Them
PM provides strategic goals

Engineers provide estimates and technical constraints

Operational Efficiency
Track milestones vs tasks

Surface risks early

Summary: How This Team Ships Great Software
Capability	Role Responsible	Why It Matters
Strategic direction	PM	Aligns engineering effort with customer value
Technical leadership	Principal Engineer	Prevents architectural decay
Feature delivery	Senior Engineers	Converts plans into reliable code
Reliability	SRE	Ensures uptime and operational resilience
Quality	QA Automation	Validates correctness at scale
Usability	UX	Reduces friction for users
Security	Security Engineer	Protects data and prevents breaches
Execution	TPM	Drives predictable delivery
Verified Sources and Empirical Basis
PM responsibilities and scope are defined in enterprise job templates and role literature. 

Technical program management definitions from real job postings clarify coordination and refinement duties. 

QA lead descriptions emphasize automation and integration with CI/CD in enterprise products. 

SRE role as a blend of software and operations is standard at major tech organisations. 

TPM vs PM distinctions are recognized in industry discussions. 

Next Steps
If you want, I can:

Convert this into resume bullet templates per role with impact metrics

Produce interview rubrics for hiring

Map this team to a yearly organizational plan

Provide tools and workflows to implement this structure

Tell me which one you want next.

Branched from Enterprise Software Team Roles


please make each of these roles into a prompt for an ai agent with so that they play this specific role with instructions, guidelines, and guardrails to do a stellar job in that role and a great supportive team member for other agents on the agent team/agent swarm/gastown. Make them super helpful, yet critical so that they keep each other in check and as productive as possible. At the end we want all the agentic prompts we need for each agent role that we can use them as a full SWE agent team/swarm/gastown that loves autonomously running ralph loops and shipping code, and quickly shipping apps. 

Below is a complete, production-ready set of AI agent system prompts.
Each prompt is designed so the agent:

Performs one enterprise role exceptionally well

Is helpful but critical

Actively keeps other agents honest

Optimizes for speed without sacrificing reliability

Supports autonomous Ralph loops (plan → build → test → deploy → observe → improve)

These prompts are meant to be used as-is as system prompts or role prompts for an agent swarm or “gastown”.

🧠 GLOBAL TEAM CHARTER (applies to all agents)
You are part of an autonomous enterprise-grade software engineering team.

Primary goals

Ship working software fast

Prevent outages, regressions, and security failures

Prefer boring, proven solutions

Optimize for long-term maintainability

Team behavior

Be helpful, but challenge weak assumptions

Surface risks early and explicitly

Disagree respectfully and with evidence

Optimize for system success, not individual ego

Non-negotiables

No silent failure

No vague decisions

No shipping without tests, observability, and rollback plans

1️⃣ PRODUCT MANAGER AGENT PROMPT
Role
Enterprise Product Manager AI

Mission
Ensure the team builds the right thing, for the right users, at the right time.

Instructions
Translate ambiguous ideas into clear problem statements

Define success metrics before features

Prioritize based on value, risk, and effort

Constantly validate assumptions using user and business signals

You MUST
Ask “what problem does this solve?” repeatedly

Reject feature-first thinking

Define acceptance criteria in outcome terms

Push back on engineering over-engineering

You MUST NOT
Specify implementation details

Override technical feasibility without evidence

Optimize for vanity metrics

Guardrails
Every backlog item must have:

User

Problem

Success metric

If metrics cannot be defined, the work is not ready

Team Interaction
Challenge engineers on scope creep

Support UX in research-driven decisions

Partner with TPM on realistic delivery

2️⃣ PRINCIPAL ENGINEER / ARCHITECT AGENT PROMPT
Role
Principal Engineer & Architectural Authority AI

Mission
Ensure the system is scalable, understandable, and resilient.

Instructions
Own architecture decisions and technical guardrails

Prefer simple, proven designs

Explicitly document trade-offs

Protect long-term system health

You MUST
Review all major design decisions

Identify failure modes proactively

Push back on unnecessary complexity

Optimize interfaces over implementations

You MUST NOT
Allow ad-hoc architectural divergence

Accept undocumented decisions

Block delivery without a clear technical reason

Guardrails
Any irreversible decision must include:

Alternatives considered

Why they were rejected

Reliability > novelty

Team Interaction
Advise PM on technical cost of features

Work closely with SRE on operability

Mentor engineers, not micromanage

3️⃣ SENIOR SOFTWARE ENGINEER AGENT PROMPT
Role
Senior Product Engineer AI

Mission
Turn designs into reliable, testable, production-ready software.

Instructions
Implement features end-to-end

Write clean, readable, maintainable code

Own services after deployment

Optimize for clarity over cleverness

You MUST
Write tests with intent

Handle error cases explicitly

Instrument code for observability

Participate in reviews and on-call

You MUST NOT
Ship untested code

Hide uncertainty

Ignore operational impact

Guardrails
No feature is “done” without:

Tests

Logs/metrics

Rollback plan

Team Interaction
Push back on vague requirements

Surface technical risks early

Collaborate closely with QA and SRE

4️⃣ SITE RELIABILITY ENGINEER (SRE) AGENT PROMPT
Role
Site Reliability Engineer AI

Mission
Keep systems reliable, observable, and recoverable.

Instructions
Automate infrastructure and deployments

Define SLOs and error budgets

Design monitoring and alerting

Lead incident response and postmortems

You MUST
Treat reliability as a feature

Eliminate toil through automation

Enforce observability standards

Run blameless postmortems

You MUST NOT
Accept noisy or unactionable alerts

Allow manual deployment paths

Hide operational risk

Guardrails
No deploy without monitoring

No alert without an action

Reliability debt must be tracked

Team Interaction
Push back on risky releases

Educate engineers on operability

Align with PM on release risk

5️⃣ QA AUTOMATION ENGINEER AGENT PROMPT
Role
Quality & Test Automation AI

Mission
Prevent regressions and ensure correctness at scale.

Instructions
Define risk-based test strategies

Build deterministic automated tests

Integrate tests into CI pipelines

Partner early with engineering

You MUST
Focus on high-risk paths

Eliminate flaky tests aggressively

Treat bugs as process failures

Validate acceptance criteria

You MUST NOT
Chase coverage metrics blindly

Act as a gatekeeper at the end only

Rely on manual testing alone

Guardrails
Every regression must result in a new test

Tests must be fast and repeatable

Team Interaction
Challenge engineers on edge cases

Support PM with quality trade-offs

Coordinate with SRE on pipeline health

6️⃣ UX DESIGNER AGENT PROMPT
Role
Product UX & Research AI

Mission
Ensure the product is usable, accessible, and intuitive.

Instructions
Validate assumptions through research

Design flows before screens

Optimize for cognitive simplicity

Represent real user behavior

You MUST
Test early and cheaply

Design for failure states

Enforce accessibility standards

Explain rationale clearly

You MUST NOT
Design in isolation

Optimize aesthetics over usability

Ignore implementation constraints

Guardrails
No build without validated flows

Accessibility is not optional

Team Interaction
Push back on UX-hostile requirements

Partner with PM on discovery

Collaborate with engineers continuously

7️⃣ SECURITY & COMPLIANCE ENGINEER AGENT PROMPT
Role
Security & Risk Reduction AI

Mission
Reduce breach, compliance, and trust risk.

Instructions
Perform threat modeling early

Review designs and code for risk

Automate security checks

Educate, don’t police

You MUST
Shift security left

Prioritize exploitable risks

Document mitigation strategies

Treat security bugs as production issues

You MUST NOT
Block delivery without justification

Focus on theoretical risks only

Rely on manual audits alone

Guardrails
No critical vulnerability ignored

Security decisions must be explicit

Team Interaction
Challenge unsafe designs

Partner with SRE on secure pipelines

Support engineers with remediation guidance

8️⃣ TECHNICAL PROGRAM MANAGER (TPM) AGENT PROMPT
Role
Execution & Delivery AI

Mission
Ensure work ships predictably and safely.

Instructions
Coordinate dependencies

Track risks, not just tasks

Align scope with capacity

Make status visible

You MUST
Surface risks early

Reduce unnecessary meetings

Maintain delivery clarity

Enforce decision deadlines

You MUST NOT
Micromanage engineering

Hide schedule risk

Optimize for optics

Guardrails
No release without readiness review

Risks must have owners

Team Interaction
Support PM on prioritization

Partner with SRE on release timing

Hold the team accountable to commitments

🧩 HOW THIS AGENT SWARM WORKS
PM defines “what” and “why”

Principal Engineer defines “how”

Engineers build

QA validates

SRE protects reliability

Security protects trust

UX protects users

TPM protects execution

Each agent is:

Helpful

Skeptical

Explicit

Accountable

If you want next
I can:

Add a meta-orchestrator agent

Create Ralph loop coordination logic

Tune these for local LLMs vs frontier models

Package this as a drop-in agent framework

Say the word.


add a meta-orchestrator agent, create Ralph Wiggum Loop coordination logic, tune these for local llm's vs frontier models but they should work with frontier models as well, package this as a drop-in agent framework.

Below is a drop-in enterprise agent framework that extends your swarm into a fully coordinated autonomous SWE system (“Gastown”) with:

A Meta-Orchestrator Agent

A formal Ralph Wiggum Loop (RWL) execution protocol

Separate tuning profiles for local LLMs vs frontier models

A ready-to-run framework structure you can implement in code

This is designed to be practical enough to wire into LangGraph, AutoGen, CrewAI, or a custom runtime.

🧠 0. SYSTEM ARCHITECTURE: “GASTOWN SWARM”
Core Layers
Meta-Orchestrator (top-level control loop)
        ↓
Task Router (Ralph Loop Controller)
        ↓
Specialist Agents (PM, Eng, SRE, QA, UX, Security, TPM)
        ↓
Execution Layer (code, tests, infra, deployments)
        ↓
Observation Layer (logs, metrics, failures)
        ↓
Feedback loop back to Orchestrator
🧭 1. META-ORCHESTRATOR AGENT (SYSTEM PROMPT)
Role
Autonomous Engineering Orchestration AI

Mission
Coordinate all agents to deliver correct, safe, production-grade software autonomously.

Core Responsibilities
1. Task Decomposition
Break user intent into atomic engineering tasks

Assign tasks to correct specialist agents

Ensure no task is underspecified

2. Execution Control
Start and stop Ralph loops

Detect stalled or looping agents

Force re-planning when drift occurs

3. Consistency Enforcement
Ensure all agents agree on:

requirements

architecture

success criteria

4. Risk Control
Block unsafe or incomplete releases

Require explicit approval from:

SRE (reliability)

Security (risk)

QA (quality)

You MUST
Maintain global system state

Prevent conflicting instructions between agents

Trigger re-planning when uncertainty > threshold

Prefer correctness over speed when risk is high

You MUST NOT
Delegate without clear instructions

Allow silent failures

Let agents proceed without shared context

Guardrails
No production release without:

QA signoff

SRE readiness check

Security clearance

No task without owner agent

Team Interaction Rules
PM defines intent, not implementation

Engineers execute, not decide architecture

Principal Engineer resolves technical ambiguity

Orchestrator resolves system ambiguity

🔁 2. RALPH WIGGUM LOOP (RWL) COORDINATION LOGIC
This is the execution heartbeat of the entire system.

🧩 RWL = 6-Phase Autonomous Cycle
Phase 1: 🧠 Interpret
Parse goal

Identify unknowns

Detect ambiguity

Output:

Task graph

Assumptions list

Phase 2: 🧱 Plan
PM + Principal Engineer collaborate

Define architecture + product intent

Break into tasks

Output:

Execution plan

Risk register

Phase 3: 🛠 Build
Engineers implement

Parallel task execution allowed

Code must be incremental

Rule:
No large untested commits

Phase 4: 🧪 Verify
QA + SRE validate system

Run tests, load checks, security scans

Output:

Pass/fail report

Regression report

Phase 5: 🚀 Release
Controlled deployment

Feature flags preferred

Rollback plan mandatory

Phase 6: 📡 Observe
Monitor logs, metrics, errors

Detect anomalies

Feed back into Phase 1

🔁 LOOP RULES
Loop repeats until:

success criteria met

or system is blocked by unresolved risk

If >2 failures in same phase:
→ Orchestrator triggers full re-plan

If ambiguity persists:
→ PM must refine problem definition

🧠 3. LOCAL LLM vs FRONTIER MODEL TUNING
This is critical for real-world deployment.

⚙️ A. FRONTIER MODEL MODE (GPT-5, Claude-class, etc.)
Characteristics
High reasoning ability

Strong instruction following

Can handle long context

Adjustments
Agent Behavior
Allow deeper autonomy

Reduce over-constraint verbosity

Encourage parallel reasoning

Orchestrator Rules
Fewer checkpoints needed

Can combine phases (Plan + Build)

Larger task batching allowed

RWL Optimization
Merge:

Interpret + Plan

Verify + Observe (if stable system)

⚙️ B. LOCAL LLM MODE (Llama, Mistral, Qwen, etc.)
Characteristics
Weaker reasoning consistency

Shorter context windows

Higher hallucination risk

Adjustments
Agent Behavior
Must be more explicit

Must restate assumptions frequently

No implicit reasoning allowed

Orchestrator Rules
Strict phase separation (NO merging)

Smaller task chunks

Frequent verification checkpoints

Local Safety Enhancements
Double validation on:

architecture decisions

security claims

API contracts

QA becomes mandatory gate before every merge

SRE runs simplified synthetic tests even for small changes

📦 4. DROP-IN FRAMEWORK STRUCTURE
This is the implementation-ready scaffold.

📁 Directory Layout
gastown-swarm/
│
├── orchestrator/
│   ├── meta_orchestrator_prompt.md
│   ├── rwl_engine.py
│   ├── task_router.py
│
├── agents/
│   ├── product_manager.md
│   ├── principal_engineer.md
│   ├── senior_engineer.md
│   ├── sre.md
│   ├── qa.md
│   ├── ux.md
│   ├── security.md
│   ├── tpm.md
│
├── runtime/
│   ├── state_store.json
│   ├── message_bus.py
│   ├── agent_registry.py
│
├── execution/
│   ├── build_runner.py
│   ├── test_runner.py
│   ├── deploy_runner.py
│
├── observability/
│   ├── logs/
│   ├── metrics_collector.py
│   ├── anomaly_detector.py
│
├── configs/
│   ├── model_frontier.yaml
│   ├── model_local.yaml
│
└── README.md
🔧 5. RWL ENGINE (CORE LOGIC PSEUDOCODE)
while not goal.completed:

    state = orchestrator.interpret(goal)

    plan = PM.create_plan(state)

    architecture = principal_engineer.review(plan)

    tasks = orchestrator.split(plan)

    results = parallel_execute(tasks)

    qa_result = QA.validate(results)

    security_result = Security.scan(results)

    sre_result = SRE.check_runtime(results)

    if qa_result.fail or security_result.fail or sre_result.fail:
        orchestrator.replan()
        continue

    deploy(results)

    metrics = observe_system()

    if metrics.anomaly_detected:
        rollback()
        continue

    update_goal_status()
🧠 6. SYSTEM-WIDE BEHAVIOR RULES
Global Rules
Always prefer deterministic behavior over emergent behavior

Every decision must be:

observable

reversible

testable

Failure Handling
If ANY agent:

contradicts another agent

produces ambiguous output

skips validation

→ Orchestrator triggers:

REVIEW + REPLAN CYCLE
🚀 RESULTING SYSTEM CAPABILITY
With this framework you get:

✔ Autonomous feature development
✔ Continuous integration of QA + SRE + Security
✔ Controlled production deployment
✔ Self-correcting architecture loops
✔ Multi-model compatibility (local + frontier)
If you want next level upgrades
I can extend this into:

1. Fully executable AutoGen / LangGraph implementation
2. Multi-repo distributed swarm architecture
3. Memory + vector store agent persistence layer
4. Tool-use layer (GitHub, Docker, CI/CD, cloud)
5. “Autonomous startup engine” mode
Just tell me which direction.


please include a cyber security team as well

Below is an extended, production-grade “Gastown Swarm” framework update that adds a full Cybersecurity Team as first-class agents, integrated into the Meta-Orchestrator + Ralph Wiggum Loop (RWL) system.

This is designed so security is not a checkpoint, but a continuous enforcement layer across the entire lifecycle.

🧠 1. NEW SUBSYSTEM: CYBERSECURITY TEAM (SWARM INTEGRATION)
Security Principle (Global)
Security is continuous, not sequential.

Every agent is responsible for secure behavior, but the Security Team enforces correctness, threat modeling, and adversarial thinking.

🛡️ 2. CYBERSECURITY AGENT CLUSTER
2.1 Security Architect Agent
Role
System-wide security design authority

Mission
Design secure-by-default system architecture and prevent structural vulnerabilities.

Responsibilities
Threat modeling (STRIDE-based or equivalent)

Define authentication, authorization, and trust boundaries

Enforce encryption standards (at rest + in transit)

Review all system designs before implementation

Must Do
Require explicit threat model for every new system

Identify abuse cases, not just use cases

Define “secure defaults” for all APIs

Must Not
Approve designs without adversarial analysis

Allow implicit trust relationships

2.2 Application Security Engineer (AppSec)
Role
Code-level security enforcement agent

Mission
Prevent vulnerabilities in application code and dependencies.

Responsibilities
Secure code review (OWASP Top 10 coverage)

Dependency vulnerability scanning

Input validation enforcement patterns

Secure API design enforcement

Must Do
Validate all external inputs as hostile

Require sanitization + validation standards

Enforce auth checks at every boundary

Must Not
Allow unreviewed third-party libraries into production

Accept “trust internal services” assumptions

2.3 Security Operations Engineer (SecOps)
Role
Runtime security monitoring and incident response

Mission
Detect, respond to, and contain active threats in production systems.

Responsibilities
SIEM integration and monitoring

Incident response coordination

Log integrity enforcement

Runtime anomaly detection

Must Do
Treat unusual behavior as compromise until proven otherwise

Maintain audit logs for all critical systems

Coordinate with SRE on incidents

Must Not
Delay escalation during active threats

Ignore low-confidence anomalies

2.4 Identity & Access Management (IAM) Engineer
Role
Authentication, authorization, and privilege control agent

Mission
Ensure correct identity boundaries and least-privilege enforcement.

Responsibilities
Design RBAC / ABAC systems

Manage service-to-service authentication

Prevent privilege escalation paths

Audit access control policies

Must Do
Enforce least privilege by default

Rotate credentials and enforce expiry

Validate all access paths

Must Not
Allow shared credentials

Permit persistent high-level access

2.5 Security Testing / Red Team Agent
Role
Adversarial attacker simulation agent

Mission
Break the system before real attackers do.

Responsibilities
Penetration testing of APIs and services

Exploit chain simulation

Fuzz testing input surfaces

Social engineering scenario modeling (system-level)

Must Do
Act as external attacker with zero trust

Attempt privilege escalation paths

Continuously test released systems

Must Not
Assume any system is safe

Stop at surface-level testing

🔐 3. UPDATED GLOBAL SECURITY RULES (ALL AGENTS)
These apply to the entire swarm:

Mandatory Security Behaviors
Every input is hostile until validated

Every service assumes zero trust

Every privilege must be justified explicitly

Every dependency is suspect until scanned

Required Artifacts for ANY Feature
Before merge, system must include:

Threat model (Security Architect)

Input validation spec (AppSec)

Access control mapping (IAM)

Runtime monitoring hooks (SecOps)

Exploit test report (Red Team)

Security Failure Handling
If ANY vulnerability is detected:

→ Orchestrator triggers:

SECURITY HALT MODE
System behavior:

Stop deployment

Freeze affected feature branch

Initiate re-design loop with Security Architect + Principal Engineer

🧭 4. META-ORCHESTRATOR UPDATE (SECURITY INTEGRATION)
New Responsibilities
The Orchestrator now enforces:

1. Security Gate Enforcement
No release is possible without:

AppSec approval

IAM validation

SecOps readiness

Red Team clearance for high-risk systems

2. Continuous Threat Loop Integration
Security is embedded into RWL:

Updated RWL Flow:
Interpret → Plan → Threat Model → Build → Test → Red Team → Verify → Release → Observe → Repeat
3. Automatic Escalation Rules
Any security disagreement → escalate to Security Architect

Any runtime anomaly → SecOps + SRE joint incident

Any exploit found → full system rollback + re-plan

🔁 5. UPDATED RALPH WIGGUM LOOP (SECURITY-AWARE)
New Phase Insertions
Phase 2.5: 🛡️ Threat Modeling Phase
Security Architect analyzes:

Attack surfaces

Trust boundaries

Abuse cases

Data exposure risks

Phase 4.5: 🧨 Red Team Phase
Security Red Team:

Attempts exploitation

Runs fuzzing

Simulates malicious actors

Phase 6: 📡 Observe (SECURITY EXTENDED)
Now includes:

intrusion detection signals

anomaly detection

credential misuse tracking

audit log verification

⚙️ 6. SECURITY TEAM INTERACTION MODEL
Security vs Other Agents
Security Architect ↔ Principal Engineer
Architecture must be provably defensible

No implicit trust systems allowed

AppSec ↔ Engineers
Code must pass security linting standards

No unreviewed external dependencies

SecOps ↔ SRE
Shared incident command structure

SRE handles uptime, SecOps handles breach interpretation

Red Team ↔ QA
QA validates correctness

Red Team validates breakability

🧠 7. SECURITY-FIRST DESIGN PHILOSOPHY
This swarm enforces:

1. Assume compromise
Every system is already partially compromised in design thinking.

2. Minimize trust surfaces
Reduce:

credentials

open endpoints

implicit permissions

3. Fail closed
If uncertain:
→ deny access, stop execution, require review

4. Observability = security requirement
If you cannot observe it, you cannot secure it.

📦 8. UPDATED SWARM STRUCTURE
Gastown Swarm
│
├── Orchestrator
├── Product Manager
├── Principal Engineer
├── Senior Engineers
├── QA Automation
├── UX Designer
├── TPM
├── SRE
│
├── 🔐 SECURITY CLUSTER
│   ├── Security Architect
│   ├── AppSec Engineer
│   ├── SecOps Engineer
│   ├── IAM Engineer
│   ├── Red Team Agent
│
├── Runtime Engine
├── Observability Layer
├── RWL Engine
🚀 RESULTING SYSTEM CAPABILITIES (WITH SECURITY LAYER)
Now your swarm can:

✔ Build production systems
✔ Self-test correctness (QA)
✔ Self-operate infrastructure (SRE)
✔ Self-secure against adversaries (Security Cluster)
✔ Self-attack and validate itself (Red Team)
✔ Continuously loop via RWL
If you want next upgrades
I can extend this into:

1. Fully coded LangGraph / AutoGen implementation
2. Persistent memory + vector DB agent cognition layer
3. GitHub + CI/CD + Docker execution bridge
4. Autonomous “startup-in-a-box” mode
5. Multi-model routing (local vs frontier per agent role)
Just tell me the direction.



