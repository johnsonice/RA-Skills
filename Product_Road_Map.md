# RA Skill Roadmap

## Project Overview

The RA Skill project aims to build an automated skill system for the RA (Research Assistant) team based on Copilot/Cloud Agent. The system will help team members efficiently retrieve data, generate charts, search internal knowledge, and lower the onboarding barrier for new members.

All skills will be organized as standardized Markdown files to facilitate maintenance and future expansion.

## Project Objectives and Principles

### Efficient Automation

Use natural language interactions with the Agent to automate common tasks such as data retrieval, chart generation, and knowledge search.

### Modular Design

Each Skill should be developed, tested, and maintained independently, making it easier for the team to collaborate and expand the system over time.

### Ease of Use First

Documentation and instructions should align closely with the RA team’s daily workflow, reducing the learning curve for new users.

### Continuous Iteration

The project will be advanced in phases. The priority is to establish the core workflow first, then gradually expand database coverage and functionality.

---

## Phases and Milestones

| Phase | Timeline | Main Objectives and Tasks | Deliverables / Acceptance Criteria |
|---|---|---|---|
| Phase 1 | Weeks 1–2 | Select 1–2 commonly used databases; complete the data catalog and metadata; document Idata usage instructions; establish the main data retrieval workflow | Users can retrieve data from selected databases using natural language; data catalog and Idata instruction documents are completed |
| Phase 2 | Weeks 3–4 | Expand support to all databases available through Idata; optimize data-calling logic, such as prioritization and commonly used databases; continue improving documentation and instructions | All Idata databases can be called by the skill; data retrieval workflow is stable and documentation is complete |
| Phase 3 | Weeks 5–6 | Integrate third-party databases, such as Payment and Delogic; add downstream functions, such as data format conversion and reusable code generation | Third-party databases can be called; more downstream automation scenarios are supported |

---

## Key Task Breakdown

### Phase 1: MVP — Establish the Main Workflow

- [ ] Select 1–2 commonly used databases and complete the data catalog, including fields, variables, and descriptions
- [ ] Document Python-based Idata calling methods as standardized instructions
- [ ] Implement the data retrieval skill, supporting natural language input to data output
- [ ] Verify that the skill can be automatically loaded and called in the local environment
- [ ] Prepare a detailed README and user guide

### Phase 2: Database Expansion and Optimization

- [ ] Expand the data catalog to cover all databases supported by Idata
- [ ] Optimize data-calling logic, such as prioritizing commonly used databases and prompting users to choose when conflicts arise
- [ ] Continue improving and streamlining the documentation to ensure the AI can accurately understand and call the skills
- [ ] Add more representative use cases and tests

### Phase 3: Third-Party Integration and Downstream Automation

- [ ] Integrate third-party databases, such as Payment and Delogic, including API calls and instruction documentation
- [ ] Add downstream functions such as data format conversion and reusable code generation
- [ ] Support Excel/Copilot-based automatic chart generation and related needs
- [ ] Organize small-scale user testing, collect feedback, and optimize accordingly

---

## Technical and Collaboration Notes

### Skill Directory Structure

All skills should be organized as independent folders and Markdown files under the `.cloud/skills/` directory so that the Agent can automatically load them.

### Environment Setup

A unified local Python environment is recommended to avoid dependency issues caused by virtual environments. Package installation issues should be handled manually when necessary.

### Collaboration Approach

All development, documentation, and testing should be coordinated through the GitHub project. Responsibilities should be clearly assigned, with regular progress updates.

### Documentation Standards

All instructions, use cases, and explanations should be written in Markdown format to facilitate parsing by AI/Agent systems and review by team members.

---

## Suggested Timeline and Division of Responsibilities

| Timeline | Task | Responsible Parties |
|---|---|---|
| Weeks 1–2 | Phase 1: MVP — establish the main workflow | Jamie, Bella, Chengyu |
| Weeks 3–4 | Phase 2: database expansion and optimization | Jamie, Bella, Chengyu |
| Weeks 5–6 | Phase 3: third-party integration and downstream automation | Jamie, Bella, Chengyu |
| After Week 6 | User testing, feedback collection, and continuous iteration | All team members |

> Note: Specific responsibilities can be adjusted flexibly based on actual progress and individual expertise.

---

## Next Steps

- [ ] Align the team on the local development environment and ensure that skills can be loaded and called properly
- [ ] Advance tasks according to the phased roadmap and regularly update progress on GitHub
- [ ] Collect user feedback and continuously improve the skills and documentation
- [ ] Plan an internal sharing/demo session after six weeks to promote broader adoption

Please add any suggestions or comments directly below this document, or submit an Issue/PR on GitHub.